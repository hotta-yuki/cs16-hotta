"""ガウス過程回帰（README 7.）。scikit-learn の GaussianProcessRegressor を薄く包む。

    k(x, x') = sf2 * Matern_{5/2}(r) + sn2 * δ(x, x')
    r^2      = Σ_k ((x_k - x'_k) / ell_k)^2          ell は変数ごと（ARD）

sklearn では ConstantKernel(sf2) * Matern(ell, nu=2.5) + WhiteKernel(sn2)。
出力 y は自分で平均 0・分散 1 に標準化してから渡す（normalize_y=False）。こうすると
sklearn の L_（K のコレスキー分解）と alpha_ = K^-1 y がそのまま標準化後の空間の量になり、
LOO を閉形式で計算できる。ハイパーパラメータは対数周辺尤度の最大化（L-BFGS-B、
初期値を n_restarts + 1 個）で sklearn が決める。

経緯: 2026-11-17 に numpy/scipy の自前実装で書き、2026-11-19 に sklearn 1.7.1 と照合した
（対数周辺尤度・長さスケールが小数 3 桁まで一致、予測平均の差は σ_z の 4e-5 以下）うえで、
sklearn に切り替えた。
"""

import warnings

import numpy as np
from scipy.linalg import cho_solve
from sklearn.exceptions import ConvergenceWarning
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel

# 入力が [0, 1] に正規化され、出力が標準化されている前提での探索範囲
ELL_BOUNDS = (1e-2, 1e2)
SF2_BOUNDS = (1e-2, 1e2)
SN2_BOUNDS = (1e-10, 1e0)


def make_kernel(n_dim):
    return (ConstantKernel(1.0, SF2_BOUNDS)
            * Matern(length_scale=np.full(n_dim, 0.3), length_scale_bounds=ELL_BOUNDS, nu=2.5)
            + WhiteKernel(1e-4, SN2_BOUNDS))


class GPR:
    def __init__(self, n_restarts=8, seed=0):
        self.n_restarts = n_restarts
        self.seed = seed

    def fit(self, X, y):
        X = np.asarray(X, float)
        y = np.asarray(y, float)
        self.y_mean, self.y_std = float(y.mean()), float(y.std())
        ys = (y - self.y_mean) / self.y_std
        self.model = GaussianProcessRegressor(
            make_kernel(X.shape[1]), normalize_y=False,
            n_restarts_optimizer=self.n_restarts, random_state=self.seed)
        # 探索範囲の端に張り付くと sklearn は ConvergenceWarning を出す。止めずに記録する
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", ConvergenceWarning)
            self.model.fit(X, ys)
        self.at_bound = [str(x.message) for x in w if issubclass(x.category, ConvergenceWarning)]
        k = self.model.kernel_
        self.sf2 = float(k.k1.k1.constant_value)
        self.ell = np.atleast_1d(k.k1.k2.length_scale).astype(float)
        self.sn2 = float(k.k2.noise_level)
        self.nll = float(-self.model.log_marginal_likelihood_value_)
        self.alpha = self.model.alpha_
        self._ys = ys
        return self

    def predict(self, Xs, return_std=False, include_noise=True):
        """予測平均と標準偏差（元のスケール）。

        include_noise=True（sklearn の既定）は WhiteKernel の sn2 を含む y の標準偏差。
        False にすると潜在関数 f の標準偏差（sqrt(std^2 - sn2)）を返す。
        """
        if not return_std:
            return self.model.predict(np.asarray(Xs, float)) * self.y_std + self.y_mean
        mu, sd = self.model.predict(np.asarray(Xs, float), return_std=True)
        if not include_noise:
            sd = np.sqrt(np.clip(sd ** 2 - self.sn2, 0, None))
        return mu * self.y_std + self.y_mean, sd * self.y_std

    def loo(self):
        """一点抜き交差検証の予測（ハイパーパラメータは全点で決めたものに固定）。

        Rasmussen & Williams (2006) 式 5.12: mu_-i = y_i - [K^-1 y]_i / [K^-1]_ii、
        var_-i = 1 / [K^-1]_ii（ノイズ込み）。K = L_ L_^T は sklearn が持っている。
        """
        Kinv = cho_solve((self.model.L_, True), np.eye(len(self._ys)))
        dinv = np.diag(Kinv)
        mu = self._ys - self.alpha / dinv
        sd = np.sqrt(1.0 / dinv)
        return mu * self.y_std + self.y_mean, sd * self.y_std
