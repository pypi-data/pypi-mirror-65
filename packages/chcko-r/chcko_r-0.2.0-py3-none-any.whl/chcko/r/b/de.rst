.. raw:: html

    %path = "Mathematik/Vektoren"
    %kind = kinda["Texte"]
    %level = 11
    <!-- html -->

Vektoren
--------

Was ist ein Vektor?
...................

    Einen **mehrdimensionalen Vektor** kann man als unabhängige Auswahl (Wert) von
    mehreren Variablen (Kategorien, Größen, Dimensionen) verstehen.

    Die Werte (Zahl+Einheit) müssen unabhängig **addierbar** sein.

    Die jeweiligen Einheiten sind die **Einheitsvektoren**.  Sie bilden
    zusammen die **Basis** und werden deshalb auch **Basisvektoren** genannt.

    Auch eine Auswahl aus einer Variable ist ein Vektor, ein **eindimensionaler** Vektor.

    Der gesamte Vektor kann mit einer Zahl, dem **Skalar**, multipliziert
    werden und ergibt wieder ein Vektor.

Beispiel

    - Wenn ich in einen Laden gehe, dann sind die Produkte darin mein
      Vektorraum (Koordinatensystem, KS) und mein Einkaufskorb ist ein Vektor,
      d.h. eine Fixierung der Werte (wieviel?) von jeder Variable (hier Produkt).
    - Wenn meine Frau auch einkaufen gegangen ist, addieren sich unsere Einkäufe zu hause unabhängig,
      d.h. Milch + Milch, Butter + Butter, ...

Koordinatentransformation
.........................

Eine Matrix transformiert eine Vektor in einem Vektorraum zu einem Vektor in einem anderen Vektorraum.
Deshalb lernen wir zuerst den Vektor kennen. Eine Matrix ergibt sich, wenn wir
von einem KS zu einem anderen wechseln wollen.

Beispiel :inline:`r.a0`


Wie schreibt man Vektoren?
..........................

- Als Spalte von Zahlen `\vec{x}=\begin{pmatrix}x_1\\x_2\end{pmatrix}`
  Die Einheitsvektoren, d.h. was die Zeilen bedeuten, gibt man separat an.
- Explizit mit Einheiten ausgeschrieben. `\vec{x}=x_1\vec{e_1}+x_2\vec{e_2}` (3
  Milchpackungen + 5 Butter) Wenn ohne Pfeil ist mit Index oben die Zahl
  gemeint und mit Index unten die Einheit (Dimension,Richtung):
  `x=x^1e_1+x^2e_2`.

Notation is nicht der Vektor selbst.

Vektorverknüpfungen
-------------------

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


Es gibt neben der Addition zwei weitere wichtige Vektorverknüpfungen.

- **Skalarprodukt (dot-product)**. Es ergibt eine Zahl (Skalar), welche die
  Abhängigkeit darstellt oder inwiewenig man unabhängig Werte auswählen kann.

  .. math:: \vec{x}\vec{y}=x_yy=y_xx=x_1y_1+x_2y_2

  - Orthogonale Vektoren ergeben 0 (keine Abhängigkeit).

  - Bei parallelen Vektoren ist es das Produkt der Längen.
    Die Länge eines Vektors `\vec{x}` ist damit `\sqrt{\vec{x}\vec{x}}`.
    Länge wird als `|\vec{x}|` oder einfach nur `x` notiert.

  - `\vec{x_o}=\frac{\vec{x}}{x}` ist der Einheitsvektor (Länge 1, Richtung von `\vec{x}`)

  - Das skalare Produkt definiert den Winkel zwischen 2 Vektoren: `\cos\alpha = \frac{\vec{x}\vec{y}}{xy}`


- **Vektorprodukt oder Kreuzprodukt (cross-product)**. Für Dimension `= 3`.
  Es ergibt einen Vektor der orthogonal zu `\vec{x}` und `\vec{y}` ist
  und die Länge ist die Fläche des von `\vec{x}` und `\vec{y}` aufgespannten Parallelogramms.

  .. math::
        \vec{x}\times\vec{y}=x_{\perp y}y=y_{\perp x}x=
        \begin{vmatrix}
        \vec{e_1} & \vec{e_2} & \vec{e_3} \\
        x_1 & x_2 & x_3 \\
        y_1 & y_2 & y_3
        \end{vmatrix}

  Wenn `\vec{x}` und `\vec{y}` zweidimensional sind, ist nur die `\vec{e_3}` Komponente von
  `\vec{x}\times\vec{y}` ungleich 0, die dann gleich
  `\begin{vmatrix}
  x_1 & x_2 \\
  y_1 & y_2
  \end{vmatrix}=
  \begin{vmatrix}
  x_1 & y_1 \\
  x_2 & y_2
  \end{vmatrix}`
  ist. Zum Vergleich: Die Determinante von 3 Vektoren im 3D Raum ist das
  Volumen des aufgespannten Parallelepipeds.


