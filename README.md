# optimcut
Simple library to optimize leftovers from cutting slices from longer material pieces in one dimension - so called **Cutting Stock Problem**.

<br>

# Annealing

Currently used, however may be not precise (gives 'locally' optimal solution and can never reach 'global' optimum).

## Advantages and drawbacks

simpler algorithm -> less code storage requirements (could be the case while working with microcontrollers)

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


The form of acceptance means that in every case while new configuration is better than before swapping slices we accept new configuration ( $`f_{i+1} \leq f_i ~\implies~ P_{acc} \geq 1`$ ), however while new configuration is worse we accept it with some probability ( $`f_{i+1} > f_i ~\implies~ P_{acc} \in (0,1)`$ ).

<br>



# Classical solution to Cutting Stock Problem 

Column generation method

https://en.wikipedia.org/wiki/Cutting_stock_problem

https://jump.dev/JuMP.jl/stable/tutorials/algorithms/cutting_stock_column_generation/

<br>


https://en.wikipedia.org/wiki/Column_generation

https://youtu.be/O918V86Grhc?si=vMTUiuFVCakP0Cmd

https://youtu.be/FVZA28XZ7Mg?si=hUYZQ3ddfakdklXg

https://youtu.be/vx2LNKx48vY?si=OeyYkN4I4hfOtcos










# Building distribution

## Create python package


## Runnig pyinstaller

Before you attempt to bundle to one file,
make sure your app works correctly when bundled to one folder.

It is is much easier to diagnose problems in one-folder mode.

building with folder distribution
```
--workpath build --distpath dist
```

building with one file distribution
```
--onefile
```

enabling gui
```
--windowed
```

https://pyinstaller.org/en/stable/operating-mode.html