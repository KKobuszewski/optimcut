# optimcut
Simple library to optimize leftovers from cutting slices from longer material pieces (single dimension).

# Annealing

Currently used, May be not precise 

simpler algorithm -> less code storage requirements

better memory efficiency

<br>

This algorithm randomly swaps two slices and decides if swap is accepted with acceptance probability given by

$$
P_{acceptance} = Exp\left[ \frac{f_i - f_{i+1}}{T} \right]
$$

$f_i$     - cost function value for configuration in $i$-th step of algorithm

$f_{i+1}$ - cost function value for configuration in the next step

$T$       - parameter regulating acceptance probablity (usually called 'temperature')





# Cutting 

https://youtu.be/O918V86Grhc?si=vMTUiuFVCakP0Cmd

https://youtu.be/FVZA28XZ7Mg?si=hUYZQ3ddfakdklXg

https://youtu.be/vx2LNKx48vY?si=OeyYkN4I4hfOtcos