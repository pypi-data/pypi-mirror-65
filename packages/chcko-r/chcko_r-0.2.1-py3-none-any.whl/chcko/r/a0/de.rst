.. raw:: html

    %path = "Mathematik/Vektoren"
    %kind = kinda["Texte"]
    %level = 11
    <!-- html -->

Wenn man die Zutaten von einer Auswahl von Kuchenrezepten
als Vektorraum auffasst, dann ist jeder Kuchen `z` ein Vektor im *Zutatenvektorraum*,
d.h. wir wählen unabhängige (Wert `z_i`) aus jeder Zutat (Variable `i`) (0 für nicht verwendet).

Wenn man nur die Kuchen betrachtet, dann ist eine Auswahl daraus ein Vektor `y`
im *Kuchenvektorraum*. Jedes `y_j` ist die Anzahl der Kuchensorte `j`.

Will man von einer Auswahl von Kuchen auf die Zutaten kommen, dann ist das
mathematisch eine **Koordinatentransformation**.  Um die Gesamtmenge `z_i`
zu erhalten muss man die Anzahl von jeder Kuchensorte `y_j` mit der
jeweiligen Zutatmenge multiplizieren. Das läuft auf eine
Matrixmultiplikation hinaus.

`z = ZK \cdot y = \sum_j ZY_{ij}y_j`

In `ZK` ist jede Spalte ein Rezept, d.h. Zutaten (**Komponenten**) für den Kuchen `j`.

Um auf den Preis `p` im *Preisvektorraum* zu kommen (d.h. was kosten alle
Zutaten für eine Auswahl von Torten) multiplizieren wir wieder

`p = PZ \cdot z = PZ_{1i} z_i`

`PZ` ist eine Matrix mit einer Zeile. Die Anzahl von Zeilen ist die
Dimension des Zielvektorraumes.

