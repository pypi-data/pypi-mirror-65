.. raw:: html

    %path = "maths/vectors"
    %kind = kinda["texts"]
    %level = 11
    <!-- html -->

Vectors
-------

What is a Vector?
.................

    A **multidimensional vector** can be seen as independently choosing (value)
    from more variables (categories, quantities, dimensions).

    The values (number+unit) must be **addable** independently.

    The units are the **unit vectors**. Together they form the **basis**
    and are therefore also called **basis vectors**.

    The choice from one variable is a vector, too, a **one-dimensional** vector.

    The whole vector can be multiplied by a number, the **scalar**, and yields a vector again.

Example:

    - If I go into a shop, then the products there are my vector space
      (coordinate system, CS) and my shopping basket is a vector, i.e. a fixing
      of the value (how much?) of each variable (here product).
    - If my wife went shopping, too, then the baskets add up independently at home,
      i.e. milk + milk, butter + butter, ...

Coordinate Transformation
.........................

A matrix transforms a vector from one coordinate system to a vector of another
coordinate system.  Therefore we learn first about vectors. The matrix comes
into play, when we want to change from one coordinate system to another.

Example :inline:`r.a0`

How do we notate vectors?
..........................

- As column of numbers `\vec{x}=\begin{pmatrix}x_1\\x_2\end{pmatrix}`.
  The unit vectors, i.e. what the rows mean, one specifies separately.
- Written explicitly with units: `\vec{x}=x_1\vec{e_1}+x_2\vec{e_2}`
  (3 milk + 5 butter). If without arrow, then the superscript index
  normally mean the scalar (number) and the subscript index the unit
  (dimension, direction): `x=x^1e_1+x^2e_2`.

Notation is not the vector itself.

Vector Operations
-----------------

.. .. texfigure:: vector_dot_cross.tex
..       :align: center

.. tikz:: \coordinate (0) at (0,0);
    \coordinate (A) at (1,3);
    \coordinate (B) at (4,2);
    \coordinate (C) at (2,1);
    \tikzset{->}
    \draw[black,very thick] (0) -- (A) node [midway,left]{$\vec{x}$};
    \draw[black,very thick] (0) -- (B) node [near end,right,below]{$\vec{y}$};
    \draw[black,very thin]  (0) -- (C) node [midway,right,below]{$x_y$};
    \draw[-,thin] (A) -- (C) node [midway,right]{$x_{\perp y}$};


Apart from addition there are two other important vector operations.

- **dot-product (scalar product)**. It yields a number (scalar) that represents the dependence
  or with how little independence one can choose values.

  .. math:: \vec{x}\vec{y}=x_yy=y_xx=x_1y_1+x_2y_2

  - Orthogonal vectors result in 0 (no dependence).

  - For parallel vectors it is the product of the lengths.
    The length of a vector `\vec{x}` is thus `\sqrt{\vec{x}\vec{x}}`
    The length is denoted as `|\vec{x}|` or simply `x`.

  - `\vec{x_o}=\frac{\vec{x}}{x}` is the unit vector (length 1 in the direction of `\vec{x}`)

  - The dot-product defines an angle between two vectors: `\cos\alpha = \frac{\vec{x}\vec{y}}{xy}`


- **Vector product or cross product**. For a dimension `= 3` it produces
  a vector orthogonal to `\vec{x}` and `\vec{y}` and of length equal to the area
  of the parallelogram created by the two vectors.

  .. math::
        \vec{x}\times\vec{y}=x_{\perp y}y=y_{\perp x}x=
        \begin{vmatrix}
        \vec{e_1} & \vec{e_2} & \vec{e_3} \\
        x_1 & x_2 & x_3 \\
        y_1 & y_2 & y_3
        \end{vmatrix}

  If `\vec{x}` and `\vec{y}` are two-dimensional, then only the `\vec{e_3}` component of
  `\vec{x}\times\vec{y}` is different from 0. It is
  `\begin{vmatrix}
  x_1 & x_2 \\
  y_1 & y_2
  \end{vmatrix}=
  \begin{vmatrix}
  x_1 & y_1 \\
  x_2 & y_2
  \end{vmatrix}`.
  Compare this to: Determinant of 3 vectors in the 3D space are the volume of the parallelepiped
  created by the three vectors.


