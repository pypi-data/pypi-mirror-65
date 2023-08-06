# MACRODEMOS

## Macroeconomics Demos: A Python package to teach macroeconomics and macroeconometrics

The purpose of this package is to provide tools to teach concepts of macroeconomics and macroeconometrics.

To date, the package provides only one function:

* [`ARMA_demo`](http://randall-romero.com/arma-demo/): Demo for learning about  ARMA processes. It creates a dash consisting of 7 plots to study the theoretical properties of ARMA(p, q) processes, as well as their estimated counterparts. The plots display
    1. a simulated sample
    2. autocorrelations
    3. partial autocorrelations
    4. impulse response function
    5. spectral density
    6. AR inverse roots
    7. MA inverse roots.

In a near future, I expect to add a few more demos:

* `Bellman_demo`: to illustrate the solution of a Bellman equation by value function iteration
* `Markov_demo`: to illustrate discrete Markov chain simulations and properties
* `Filters_demo`: to illustrate the use of the Hodrick-Prescott and the Baxter-King filters
 
### Instructions
To use the demos, just install this package `pip install macrodemos` and then

    from macrodemos import ARMA_demo
    ARMA_demo()
 
This will open a new tab in your default Internet browser with a Plotly dash. 
 
### Disclaimer 
This program illustrates basic concepts of time series filtering. It was developed for teaching purposes only.  If you have any suggestions, please send me an email at randall.romero@ucr.ac.cr
                          
##### Copyright 2016-2020 Randall Romero-Aguilar
