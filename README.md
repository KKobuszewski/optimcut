# optimcut
Simple library to optimize leftovers from cutting slices from longer material pieces (single dimension).

<br>

# Annealing

Currently used, however may be not precise (gives 'locally' optimal solution and can never reach 'global' optimum).

## Advantages and drawbacks

simpler algorithm -> less code storage requirements

better memory efficiency


## Algorithm

We assume that slices are cut in certain order and while material piece is too small for the next cut slice is moved to the next material piece.

![](https://github.com/KKobuszewski/optimcut/blob/main/figs/visualization0.gif)

Annealing algorithm randomly swaps two slices and decides if swap is accepted with acceptance probability depending on the amount of leftovers.

Swaps are repeated many times sampling different configurations of cutting the slices. This kind of 'random walk' in the space of configuration is concentrated 'near' the points with locally smallest cost function (this function could be simply length of leftovers) and gives high probability of visiting best configurations.

**Acceptance probability** is given by

$$P_{acceptance} = \exp\left[ \frac{f_i - f_{i+1}}{T} \right]$$

$f_i$     - cost function value for configuration in $i$-th step of algorithm

$f_{i+1}$ - cost function value for configuration in the next step

$T$       - parameter regulating acceptance probablity (usually called 'temperature')




<br>



# Cutting 

https://youtu.be/O918V86Grhc?si=vMTUiuFVCakP0Cmd

https://youtu.be/FVZA28XZ7Mg?si=hUYZQ3ddfakdklXg

https://youtu.be/vx2LNKx48vY?si=OeyYkN4I4hfOtcos
