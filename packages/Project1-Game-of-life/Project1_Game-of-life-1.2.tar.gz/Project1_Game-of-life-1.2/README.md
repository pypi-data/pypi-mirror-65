# Project1_Game-of-life

https://en.wikipedia.org/wiki/Conway's_Game_of_Life

Project for the course "Advanced Scientific Programming in Python", 23-27 March 2020, Uppsala University.

See "Demonstration.ipynb".

I run it on Anaconda on Windows 10.
It does not work in JupyterLab, but it should work in Jupyter Notebook.

TODO: "Add CI using Travis, and running one game of 1000 iterations checking that it matches a pre known pattern."


KNOWN BUGS:
- Matrix that has all entries 1 is drawn all in blue. This is the same as the matrix with all entries 0. This is a problem in "matplotlib.pyplot", and I should check color setting there. It does not affect Game of life much, since such a matrix would die anyway, just one step later.
 
