### 11.2.4 混合重みの更新（Updating the Mixture Weights）

**定理 11.3（GMMの混合重みの更新）。** GMMの混合重み $\pi_{k} (k=1, \ldots, K)$ は次のように更新されます。

$$
\pi_{k}^{\text {new }}=\frac{N_{k}}{N}, \quad k=1, \ldots, K,
$$

ここで、$N$ はデータポイントの数であり、$N_{k}$ は(11.24)で定義されています。

**証明：** 重みパラメータ $\pi_{k} (k=1, \ldots, K)$ に関する対数尤度の偏微分を求める際、制約条件 $\sum_{k} \pi_{k}=1$ を考慮するためにラグランジュの未定乗数法（7.2節参照）を使用します。ラグランジュ関数は次のようになります。

$$
\mathfrak{L}=\mathcal{L}+\lambda\left(\sum_{k=1}^{K} \pi_{k}-1\right)
$$

$$
=\sum_{n=1}^{N} \log \sum_{k=1}^{K} \pi_{k} \mathcal{N}\left(\boldsymbol{x}_{n} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)+\lambda\left(\sum_{k=1}^{K} \pi_{k}-1\right),
$$

ここで、$\mathcal{L}$ は(11.10)の対数尤度であり、第2項はすべての混合重みの和が1にならなければならないという等式制約をコード化したものです。$\pi_{k}$ に関する偏微分を次のように得ます。

$$
\begin{aligned}
\frac{\partial \mathfrak{L}}{\partial \pi_{k}} & =\sum_{n=1}^{N} \frac{\mathcal{N}\left(\boldsymbol{x}_{n} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)}{\sum_{j=1}^{K} \pi_{j} \mathcal{N}\left(\boldsymbol{x}_{n} \mid \boldsymbol{\mu}_{j}, \boldsymbol{\Sigma}_{j}\right)}+\lambda \\
& =\frac{1}{\pi_{k}} \underbrace{\sum_{n=1}^{N} \frac{\pi_{k} \mathcal{N}\left(\boldsymbol{x}_{n} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)}{\sum_{j=1}^{K} \pi_{j} \mathcal{N}\left(\boldsymbol{x}_{n} \mid \boldsymbol{\mu}_{j}, \boldsymbol{\Sigma}_{j}\right)}}_{=N_{k}}+\lambda = \frac{N_{k}}{\pi_{k}}+\lambda
\end{aligned}
$$

また、ラグランジュ乗数 $\lambda$ に関する偏微分を次のように得ます。

$$
\frac{\partial \mathfrak{L}}{\partial \lambda}=\sum_{k=1}^{K} \pi_{k}-1
$$

両方の偏微分を $\mathbf{0}$ と置く（最適解の必要条件）ことにより、次の方程式系が得られます。

$$
\begin{aligned}
\pi_{k} & =-\frac{N_{k}}{\lambda}, \\
1 & =\sum_{k=1}^{K} \pi_{k}
\end{aligned}
$$

(11.46)を(11.47)に代入して $\pi_{k}$ について解くと、次が得られます。

$$
\sum_{k=1}^{K} \pi_{k}=1 \Longleftrightarrow -\sum_{k=1}^{K} \frac{N_{k}}{\lambda}=1 \Longleftrightarrow -\frac{N}{\lambda}=1 \Longleftrightarrow \lambda=-N .
$$

これにより、(11.46)の $\lambda$ を $-N$ で置き換えることができ、次を得ます。

$$
\pi_{k}^{\mathrm{new}}=\frac{N_{k}}{N}
$$

これが重みパラメータ $\pi_{k}$ の更新式となり、定理11.3が証明されました。

(11.42)の混合重みは、$k$ 番目のクラスターの総負担率とデータポイントの数の比として識別できます。$N=\sum_{k} N_{k}$ であるため、データポイントの数はすべての混合成分の総負担率の合計としても解釈でき、$\pi_{k}$ はデータセットに対する $k$ 番目の混合成分の相対的な重要度となります。

**備考：** $N_{k}=\sum_{i=1}^{N} r_{n k}$ であるため、混合重み $\pi_{k}$ の更新式(11.42)も、負担率 $r_{n k}$ を介してすべての $\pi_{j}, \boldsymbol{\mu}_{j}, \boldsymbol{\Sigma}_{j} (j=1, \ldots, K)$ に依存します。

## 例 11.5（重みパラメータの更新）

図 11.7 GMMにおける混合重み更新の効果。(a) 混合重みを更新する前のGMM、(b) 平均と分散を維持したまま混合重みを更新した後のGMM。垂直軸のスケールが異なることに注意。

### 11.3 EMアルゴリズム（EM Algorithm）

期待値最大化（EM: Expectation Maximization）アルゴリズムは、Dempsterら(1977)によって提案されたもので、混合モデルやより一般的には潜在変数モデルにおけるパラメータ学習（最尤推定またはMAP推定）のための一般的な反復スキームです。

ガウス混合モデルの例では、$\boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}, \pi_{k}$ の初期値を選択し、収束するまで以下のステップを交互に繰り返します。

- **Eステップ：** 負担率 $r_{n k}$（データポイント $n$ が混合成分 $k$ に属する事後確率）を評価する。
- **Mステップ：** 更新された負担率を使用して、パラメータ $\boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}, \pi_{k}$ を再推定する。

EMアルゴリズムのすべてのステップは、対数尤度関数を増加させます(Neal and Hinton, 1999)。収束については、対数尤度またはパラメータを直接チェックできます。GMMのパラメータを推定するためのEMアルゴリズムの具体的なインスタンス化は以下の通りです。

1. $\boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}, \pi_{k}$ を初期化する。
2. **Eステップ：** 現在のパラメータ $\pi_{k}, \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}$ を使用して、すべてのデータポイント $\boldsymbol{x}_{n}$ について負担率 $r_{n k}$ を評価する。

$$
r_{n k}=\frac{\pi_{k} \mathcal{N}\left(\boldsymbol{x}_{n} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)}{\sum_{j} \pi_{j} \mathcal{N}\left(\boldsymbol{x}_{n} \mid \boldsymbol{\mu}_{j}, \boldsymbol{\Sigma}_{j}\right)} .
$$

3. **Mステップ：** 現在の（Eステップからの）負担率 $r_{n k}$ を使用して、パラメータ $\pi_{k}, \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}$ を再推定する。

$$
\begin{aligned}
\boldsymbol{\mu}_{k} & =\frac{1}{N_{k}} \sum_{n=1}^{N} r_{n k} \boldsymbol{x}_{n}, \\
\boldsymbol{\Sigma}_{k} & =\frac{1}{N_{k}} \sum_{n=1}^{N} r_{n k}\left(\boldsymbol{x}_{n}-\boldsymbol{\mu}_{k}\right)\left(\boldsymbol{x}_{n}-\boldsymbol{\mu}_{k}\right)^{\top}, \\
\pi_{k} & =\frac{N_{k}}{N} .
\end{aligned}
$$

(11.54)で平均 $\boldsymbol{\mu}_{k}$ を更新した後、それらは続いて(11.55)で対応する共分散を更新するために使用されます。

## 例 11.6（GMMのフィッティング）

図11.3の例でEMを実行すると、5回の反復の後に図11.8(a)に示す最終結果が得られます。図11.8(b)は、負の対数尤度がEMの反復回数の関数としてどのように推移するかを示しています。最終的なGMMは次のように与えられます。

$$
\begin{aligned}
p(x)= & 0.29 \mathcal{N}(x \mid -2.75, 0.06) + 0.28 \mathcal{N}(x \mid -0.50, 0.25) \\
& + 0.43 \mathcal{N}(x \mid 3.64, 1.63)
\end{aligned}
$$

図 11.8 図11.2のGMMに適用されたEMアルゴリズム。(a) 最終的なGMMの適合、(b) EM反復の関数としての負の対数尤度。

図11.1に示した二次元データセットに $K=3$ の混合成分でEMアルゴリズムを適用しました。図11.9はEMアルゴリズムのいくつかのステップを説明し、EM反復の関数としての負の対数尤度を示しています（図11.9(b)）。図11.10(a)は、対応する最終的なGMMの適合を示しています。

図 11.9 二次元データセットに3つの成分を持つガウス混合モデルを適合させるためのEMアルゴリズムの図解。(a) データセット、(b) EM反復の関数としての負の対数尤度（低いほど良い）。赤点は、(c)から(f)に示されている対応するGMM適合の混合成分の反復を示している。黄色の円盤はガウス混合成分の平均を示している。

図11.10(a)は最終的なGMMの適合を示しています。図11.10(b)は、データポイントに対する混合成分の最終的な負担率を視覚化したものです。EMが収束したときの混合成分の負担率に従ってデータセットが色付けされています。左側のデータについては単一の混合成分が明らかに責任を負っていますが、右側の2つのデータクラスターの重なり部分は、2つの混合成分のいずれによっても生成された可能性があります。単一のコンポーネント（青または黄色のいずれか）に一意に割り当てることができないデータポイントが存在することが明らかになり、それらのポイントに対するこれら2つのクラスターの負担率は0.5付近になります。

図 11.10 EM収束時のGMM適合と負担率。(a) EM収束時のGMM適合、(b) 各データポイントは混合成分の負担率に従って色付けされている。
