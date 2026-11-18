"""ガウス過程回帰（README 7.）。numpy / scipy だけで書いた最小実装。

scikit-learn が venv に入っていない（環境を変えないため自前で持つ）。中身は
sklearn の GaussianProcessRegressor(ConstantKernel * Matern(nu=2.5, ARD) + WhiteKernel)
と同じモデル。

    k(x, x') = sf2 * (1 + sqrt5 r + 5 r^2 / 3) exp(-sqrt5 r) + sn2 * δ(x, x')
    r^2      = Σ_k ((x_k - x'_k) / ell_k)^2          ell は変数ごと（ARD）

出力 y は学習側で平均 0・分散 1 に標準化してから扱う（predict で元に戻す）。
ハイパーパラメータ log(ell_1..ell_D, sf2, sn2) は対数周辺尤度を L-BFGS-B で最大化する。
勾配は解析的に与える。局所解を避けるため初期値を変えて複数回解く。
"""

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize

SQRT5 = np.sqrt(5.0)


def _sqdist_per_dim(A, B):
    """(n, m, D) の (a_k - b_k)^2。"""
    return (A[:, None, :] - B[None, :, :]) ** 2


def matern52(A, B, ell, sf2):
    d2 = _sqdist_per_dim(A, B) / ell ** 2
    r = np.sqrt(d2.sum(-1))
    return sf2 * (1 + SQRT5 * r + 5.0 / 3.0 * r ** 2) * np.exp(-SQRT5 * r)


class GPR:
    """探索範囲は入力が [0, 1] に正規化され、出力が標準化されている前提。"""

    def __init__(self, n_restarts=8, seed=0,
                 ell_bounds=(1e-2, 1e2), sf2_bounds=(1e-2, 1e2), sn2_bounds=(1e-10, 1e0)):
        self.n_restarts = n_restarts
        self.rng = np.random.default_rng(seed)
        self._b = (ell_bounds, sf2_bounds, sn2_bounds)

    # ---- 対数周辺尤度（の符号反転）と勾配
    def _nll(self, theta, X, y):
        D = X.shape[1]
        ell, sf2, sn2 = np.exp(theta[:D]), np.exp(theta[D]), np.exp(theta[D + 1])
        d2k = _sqdist_per_dim(X, X) / ell ** 2          # (n, n, D)
        r = np.sqrt(d2k.sum(-1))
        e = np.exp(-SQRT5 * r)
        Kf = sf2 * (1 + SQRT5 * r + 5.0 / 3.0 * r ** 2) * e
        n = len(y)
        K = Kf + sn2 * np.eye(n)
        try:
            c = cho_factor(K, lower=True)
        except np.linalg.LinAlgError:
            return 1e25, np.zeros_like(theta)
        alpha = cho_solve(c, y)
        nll = 0.5 * y @ alpha + np.log(np.diag(c[0])).sum() + 0.5 * n * np.log(2 * np.pi)
        W = np.outer(alpha, alpha) - cho_solve(c, np.eye(n))   # dNLL/dθ = -0.5 tr(W dK)
        g = np.empty_like(theta)
        common = sf2 * 5.0 / 3.0 * (1 + SQRT5 * r) * e         # dK/dlog ell_k = common * d2k[..., k]
        for k in range(D):
            g[k] = -0.5 * np.sum(W * common * d2k[..., k])
        g[D] = -0.5 * np.sum(W * Kf)
        g[D + 1] = -0.5 * np.trace(W) * sn2
        return nll, g

    def fit(self, X, y):
        X = np.asarray(X, float)
        y = np.asarray(y, float)
        self.X = X
        self.y_mean, self.y_std = y.mean(), y.std()
        ys = (y - self.y_mean) / self.y_std
        self._ys = ys
        D = X.shape[1]
        (el, eh), (fl, fh), (nl, nh) = self._b
        bounds = [(np.log(el), np.log(eh))] * D + [(np.log(fl), np.log(fh)), (np.log(nl), np.log(nh))]
        starts = [np.r_[np.zeros(D) + np.log(0.3), 0.0, np.log(1e-4)]]
        for _ in range(self.n_restarts):
            starts.append(np.array([self.rng.uniform(lo, hi) for lo, hi in bounds]))
        best = None
        for s in starts:
            res = minimize(self._nll, s, args=(X, ys), jac=True, method="L-BFGS-B", bounds=bounds)
            if best is None or res.fun < best.fun:
                best = res
        self.theta = best.x
        self.nll = float(best.fun)
        self.ell = np.exp(best.x[:D])
        self.sf2 = float(np.exp(best.x[D]))
        self.sn2 = float(np.exp(best.x[D + 1]))
        K = matern52(X, X, self.ell, self.sf2) + self.sn2 * np.eye(len(X))
        self._c = cho_factor(K, lower=True)
        self.alpha = cho_solve(self._c, ys)
        self.at_bound = [i for i, (v, (lo, hi)) in enumerate(zip(best.x, bounds))
                         if v <= lo + 1e-6 or v >= hi - 1e-6]
        return self

    def predict(self, Xs, return_std=False):
        """予測平均と、潜在関数 f の標準偏差（ノイズ項 sn2 を含まない）。

        sklearn の GaussianProcessRegressor.predict は WhiteKernel を含めた y の標準偏差を
        返すので、sqrt(std^2 + sn2 * y_std^2) が sklearn の値に一致する（2026-11-19 照合、差 1e-8 以下）。
        平均とハイパーパラメータは sklearn 1.7.1 と一致（予測差 / σ_z が 4e-5 以下）。
        """
        Ks = matern52(np.asarray(Xs, float), self.X, self.ell, self.sf2)
        mu = Ks @ self.alpha * self.y_std + self.y_mean
        if not return_std:
            return mu
        v = cho_solve(self._c, Ks.T)
        var = self.sf2 - np.einsum("ij,ji->i", Ks, v)
        return mu, np.sqrt(np.clip(var, 0, None)) * self.y_std

    def loo(self):
        """一点抜き交差検証の予測（ハイパーパラメータは全点で決めたものに固定）。

        Rasmussen & Williams (2006) 式 5.12: mu_-i = y_i - [K^-1 y]_i / [K^-1]_ii
        """
        Kinv = cho_solve(self._c, np.eye(len(self.X)))
        dinv = np.diag(Kinv)
        mu = self._ys - self.alpha / dinv
        sd = np.sqrt(1.0 / dinv)
        return mu * self.y_std + self.y_mean, sd * self.y_std

    def state(self):
        return {"ell": self.ell, "sf2": self.sf2, "sn2": self.sn2,
                "y_mean": self.y_mean, "y_std": self.y_std, "alpha": self.alpha}
