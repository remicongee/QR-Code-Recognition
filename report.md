---
title: "Report for QR Code Recognition"
author: "Yuefu ZHOU"
output:
  pdf_document: default
  html_document: default
---

## 1. Overview

In this text, we report the main technique detail concerning the projct QR Code Recognition, where QR code in a photo is transferred to a matrix.
The core challenge is extracting the QR code of $N\times N$ size from the photo and then aligning it to a $N\times N$ matrix.
To target this challenge, we conduct *perspective transform* based on a transform matrix solved approximately from a linear group, which aligns the feature points of the photo and matrix. The source code ([*link*](https://github.com/remicongee/QR-Code-Recognition)) is published on GitHub.

## 2. Data Preprocessing

Given a photo taken manually and in RGB form, we firstly transfer it to be grey-scaled, so that each pixel value is between 0 and 255. Then the pixels
are classified to be of QR pattern or not, via a thresholding. Note $P$ the photo and $T$ the threshold. The pixel value is hence reset as
$$
P_{ij}\leftarrow\left\{\;
\begin{aligned}
    &0,\;\;P_{ij}\le T, \\
    &255,\;\;\text{otherwise}  
\end{aligned}
\right.
$$

## 3. Perspective Transform

Suppose the QR code is of $N\times N$ size and there exists a perspective transform $H$ between it and a matrix $M\in \mathcal{M}_{N,N}$.
To ease the expression, we assume points are distributed continuously in the photo and matrix, where the continuous field is denoted as $\tilde{P}$ and $\tilde{M}$ in 3D. Then
$$
\forall \tilde{m} \in \tilde{M}, \exists \tilde{p}\in \tilde{P},
\tilde{p}^T = H \tilde{m}^T.
$$
With $\tilde{m}\equiv\left(x, y, 1\right)$ and $\tilde{p}\equiv\left(u,v,w\right)$, we shall have
$$
\left(
    \begin{matrix}
        u\\v\\w
    \end{matrix}\right)
    = \left(
\begin{matrix}
    H_{11}\;\;H_{12}\;\;H_{13}\\
    H_{21}\;\;H_{22}\;\;H_{23}\\
    H_{31}\;\;H_{32}\;\;H_{33}
\end{matrix}\right)
\left(
\begin{matrix}
    x\\y\\1
\end{matrix}\right).
$$
Develop this equation by noting $u'=u/w$ and $v'=v/w$,
$$
\left\{
\begin{aligned}
    &u'\left(H_{31}x+H_{32}y+H_{33} \right) = H_{11}x+H_{12}y+H_{13} \\
    &v'\left(H_{31}x+H_{32}y+H_{33} \right) = H_{21}x+H_{22}y+H_{23}
\end{aligned}.
\right.
$$
Given that, the original equation can be reformed as a linear group $w.r.t.$ the element of $H$:
$$
\left(
\begin{matrix}
    x\;\;y\;\;1\;\;0\;\;0\;\;0\;\;-u'x\;\;-u'y\;\;-u' \\
    0\;\;0\;\;0\;\;x\;\;y\;\;1\;\;-v'x\;\;-v'y\;\;-v'
\end{matrix}\right)
\left(
\begin{matrix}
    H_{11}\\H_{12}\\H_{13}\\
    H_{21}\\H_{22}\\H_{23}\\
    H_{31}\\H_{32}\\H_{33}
\end{matrix}\right)
=0.
$$

To simplify the expression, note $\bold{0}=\left(0\;0\;0\right)$ and
$h=\left(H_{r1}\;H_{r2}\;H_{r3}\right)^T$, where $H_{ri}$ denotes the $i$-th row of $H$, then
$$
\left(
\begin{matrix}
    \tilde{m}\;\;\bold{0}\;\;-u'\tilde{m} \\
    \bold{0}\;\;\tilde{m}\;\;-v'\tilde{m}
\end{matrix}\right)
h = 0.
$$
It can be observed that if $h^*$ is the solution, so will be $\alpha h^*$ for all $\alpha\in\mathbb{R}$. In this case, to avoid ambiguity, we assume that $h$ is normalized, i.e. $\|h \|=1$. Therefore, once eight elements of $h$ is known, the last one is computable as well, which means eight equation should be included in the very group. Because for each pair of point $(\tilde{m},\tilde{p})$, we are able to list two equations, as described above, four pair of points is in need.

Note $\left(\tilde{m}_i,\tilde{p}_i\right)_{i\in[1,4]}$ the pair four points, we further reform the linear group to attack as
$$
\left(
\begin{matrix}
    \tilde{m}_1\;\;\bold{0}\;\;-u'_1\tilde{m}_1 \\
    \bold{0}\;\;\tilde{m}_1\;\;-v'_1\tilde{m}_1 \\
    ... \\
    \tilde{m}_4\;\;\bold{0}\;\;-u'_4\tilde{m}_4 \\
    \bold{0}\;\;\tilde{m}_4\;\;-v'_4\tilde{m}_4
\end{matrix}\right)
h = 0,
$$
$$
s.t.\;\; \|h \| = 1.
$$

However, this group is not necessarily solvable, bacause the validity of perspective transform may be completely accurate in practice. Fortunately, we can achieve an approximate solution by supposing $h$ is the normalized eigenvector of $L^TL$ with the smallest eigenvalue, where
$$
L = \left(
\begin{matrix}
    \tilde{m}_1\;\;\bold{0}\;\;-u'_1\tilde{m}_1 \\
    \bold{0}\;\;\tilde{m}_1\;\;-v'_1\tilde{m}_1 \\
    ... \\
    \tilde{m}_4\;\;\bold{0}\;\;-u'_4\tilde{m}_4 \\
    \bold{0}\;\;\tilde{m}_4\;\;-v'_4\tilde{m}_4
\end{matrix}\right).
$$

In fact, $L^TL$ is semi-definite positive, so the smallest eigenvalue is the one the closest to 0, leading to an approximate solution for the original problem. Additionally, to ensure the solution is unique, rank of $L^TL$ should be 8, which means so will be $L$ (see in proof). Given that, the points selected should be linearly independent in their own coordinate system.

> Demonstrate $rank(L^TL)=rank(L)$. \
> $Proof$: \
> Note $N(L^TL)$ and $N(L)$ the kernel space of $L^TL$ and $L$. \
> a) Suppose $x\in N(L^TL)$, then 
> $$L^TLx = 0.$$
> Multiply $x^T$ on both sides:
> $$(Lx)^TLx = 0.$$
> Given $\|Lx\|\ge 0$, we have $Lx=0$, i.e. $x\in N(L)$. Therefore,
> $$N(L^TL)\subset N(L).$$
> b) Suppose $x\in N(L)$, then
> $$Lx=0.$$
> Multiply $L^T$ on both sides, which gives
> $$L^TLx=0.$$
> Hence, $x\in N(L^TL)$. Thus
> $$N(L)\subset N(L^TL).$$
> In conclusion, 
> $$N(L^TL)=N(L).$$ 
> Further more, 
> $$rank(L^TL)=rank(L).$$

![Corners of QR patterns.](image\points.png)

## 4. Feature Points

To select four pair of points, we extract the corners of QR code and the matrix. It is suggested in the course to use RANSAC to detect the corners from the edges obtained via dilation and erosion. In this text, we simply achieve these cornsers' coordinates manually (see in Figure 1), with the help of $\texttt{MATLAB}$.

## 5. Alignment

### 5.1 Embedding Matrix

Once the $h^*$ is obtained, the perspective transform matrix $H^*$ can be also reformed. Now to embed QR code to the matrix $M$, we compute,  for each element of $M$, the point projected from the QR code, i.e.
$$
\forall \left(i,\,j\right)\le N, M_{ij} = g\left(P_{u'(i,j),v'(i,j)} \right),
$$
where $g(.)$ is decision function, and
$$
\left(
\begin{matrix}
    u(i,\,j) \\
    v(i,\,j) \\
    w(i,\,j)
\end{matrix}\right)
= H^*\left(
\begin{matrix}
    i \\
    j \\
    1
\end{matrix}\right),\;
u'(i,\,j) = r\left(\frac{u(i,\,j)}{w(i,\,j)}\right),\;
v'(i,\,j) = r\left(\frac{v(i,\,j)}{w(i,\,j)}\right),
$$
with $r(.)$ outputs the nearest integer.

The decision function $g(.)$ can be simply identity. But to achieve a more robust performance, we consider the influence of the neighbouring pixels by forming a voting strategy:
$$
E(x) = \left\{y|y\in V(x),\,P_y = 0\right\},\;\;
g(x) = \left\{
\begin{aligned}
    &0,\;\;\|E(x)\| > \sigma \|V(x)\| \\
    &255,\;\;\text{otherwise}
\end{aligned}
\right.
$$
where $V(x)$ is a neighbourhood of $x$, $\|.\|$ counts the elements of set and $\sigma\in]0, 1[$ a tunable coefficient. Intuitively, the element of $M$ will take 0 if certain ratio of pixels around the corresponding point in $P$ are 0. The ratio is controlled by $\sigma$. In this text, we find that $\sigma=0.2$ achieves the best performance.

![Different QR Patterns.](image\Types.jpeg)

### 5.2 Standard Pattern

It is not enough to only embed the QR code to the matrix. The pattern of the QR code embedded should be further standardized, i.e., the three "$\boxdot$" features locate respectively on the South-West, North-West and North-East corner of the matrix.

To this end, we search these "$\boxdot$" features by assuming that the pixel value will all take 0 along this shape. In this text, we traverse each square routes starting from the corners until a square compeletly black is found. Once these "$\boxdot$"s are found, certain rotation operation should be then conducted.

We conclude that there are four types of situations where "$\boxdot$"s may be distributed, as seen in Figure 2, where rotation angle is reported in parenthesis.

## 6. Results

We conduct experiments on two types of QR codes (1 and 2). The results are shown as follow:

![Result of standard QR code.](image\result1.png)

![Result of rotated QR code.](image\result2.png)