.. raw:: html

    %path = "maths/vectors"
    %kind = kinda["texts"]
    %level = 11
    <!-- html -->

If we see the ingredients of a set of cake recipes as vector space, then
every cake `z` is a vector of the *ingredient vector space*, i.e. we
independently choose (value `z_i`) from each ingredient (variable `i`) (0
for not used at all).

If we only look at the cakes, then a choice from them is a vector `k`
in the *cake vector space*. Every `k_j` is the number of cakes of kind `j`.

When going from the cakes to the ingredients, mathematically one does a
coordinate transformation. To get the total amount of ingredient `z_i` one
needs to multiply the number of every cake `k_j` with the amount of
ingredient `i` for that cake. This is a matrix multiplication.

`z = ZK \cdot k = \sum_j ZK_{ij}k_j`

In `ZK` every column is a recipe, i.e. the ingredients (**components**) for cake `j`.

To obtain the price `p` in the *price vector space*, i.e. what is the cost
of all ingredients for a set of cakes, we multiply again

`p = PZ \cdot z = PZ_{1i} z_i`

`PZ` is a matrix with one row. The number of rows is the dimension of the
target vector space.

