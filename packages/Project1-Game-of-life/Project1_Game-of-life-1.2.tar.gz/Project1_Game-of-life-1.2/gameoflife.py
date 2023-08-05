#gameoflife.py

'''In this module I wrote several function that generate Conway's Game of life:

https://en.wikipedia.org/wiki/Conway's_Game_of_Life

This was a project for the course "Advanced Scientific Programming in Python", 23-27 March 2020, Uppsala University.

Note: When running in Jupyter Notebook, one should add "%matplotlib notebook".

KNOWN BUGS:
- Matrix that has all entries 1 is drawn all in blue. This is the same as the matrix with all entries 0. This is a problem in "matplotlib.pyplot", and I should check color setting there. It does not affect Game of life much, since such a matrix would die anyway, just one step later.'''


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os # Needed to create directory.


def submatrix(matrix,i,j):
    '''Returns the neigbourhood of (i,j) in matrix, as a submatrix.'''

    N = matrix.shape[0]
    
    a = max(0,i-1)    # Corners.
    b = min(i+1,N)
    c = max(0,j-1)
    d = min(j+1,N)
    
    sub = matrix[a:b+1, c:d+1]
    return sub


def nr_neighbors_locally(matrix,i,j):
    '''Returns the number of neighbors of (i,j) in matrix.'''
    
    nr = sum(sum(submatrix(matrix,i,j) )) - matrix[i][j]
    return nr


def next_generation_locally(cell, neighbors):
    '''Returns 0 or 1 according to survival rules.
    Rules of the game are here.'''
    
    if cell==1:
        if neighbors<2 or neighbors>3:
            return 0
        # Here we can assume cell==1 and neigbors==2 or 3.
        return 1
    
    # Here we can assume cell==0.   
    if neighbors==3:
        return 1
    
    return 0


def next_generation(matrix):
    '''Returns the matrix of the next generation.'''
    
    N = matrix.shape[0]
    next_gen = np.array([[ next_generation_locally(
        
        cell = matrix[i][j],
        neighbors = nr_neighbors_locally(matrix,i,j)
        
    ) for j in range(N)] for i in range(N)])    # This should be improved, maybe using fromfunction and lambda...
    
    return next_gen
   
    
def evolution(matrix, T):
    '''Returns all generations 0 to T-1, starting from matrix.
    Input: matrix = np.array of shape (N,N) with entries 0 or 1, T = non-negative integer.
	
    The result is np.array of shape TxNxN, , i.e. a numpy list of T numpy NxN matrices.'''
    
    N = matrix.shape[0]
    evol = np.zeros((T,N,N), dtype=int)
    evol[0] = matrix
    
    for i in range(T-1):       # Again "for" which should be replaced by sth more efficient.
        evol[i+1] = next_generation(evol[i])
        
        if np.all(evol[i+1]==0) == True:   # Stationary
            break
            
        if np.all(evol[i+1]==evol[i]) == True:   # Stationary, but need to copy the current state to all future times.
            for k in range(i+1,T):
                evol[k] = evol[i]
            break 

    return evol


def evolution_animation_finite(matrix, T):
    '''Produces animation of all generations from 0 to T, starting from matrix.
    Input: matrix = np.array of shape (N,N) with entries 0 or 1, T = non-negative integer.
	
    Note: Since it calculates all T generation in advance, it can take some time for the animation to start.'''
    
    evol = evolution(matrix,T)

    fig = plt.figure()
    im = plt.imshow(evol[0], animated=True)
    
    plt.axis('off') # Do not print the axes on the images.
    
    def animate(i):
        im.set_array(evol[i])
        return

    anim = animation.FuncAnimation(fig, animate, blit=True)
    return anim


def evolution_animation(matrix):
    '''Produces animation of all generations starting from matrix, forever.
    Input: matrix = np.array of shape (N,N) with entries 0 or 1.

    The function uses nonlocal variables.'''

    fig = plt.figure()
    im = plt.imshow(matrix, animated=True)

    plt.axis('off') # Do not print the axes on the images.

    def animate(i):
        nonlocal matrix
        matrix = next_generation(matrix)
        im.set_array(matrix)
        return

    anim = animation.FuncAnimation(fig, animate, blit=True)
    return anim


def evolution_graphics(matrix,T):
    '''Produces images of all generations from 0 to T, starting from matrix.
    The images are stored in folder "graphics_export" under the names "game_of_life%d.png".
	
    Input: matrix = np.array of shape (N,N) with entries 0 or 1, T = non-negative integer.'''
    
    ############## Some adjustable variables here:
    folder_name = "graphics_export"
    file_name = "game_of_life_"
    image_size = 10   # Unit not clear rigth now.
    # Colors... ?
    ##############
    
    if not os.path.isdir(folder_name):  # Is there a folder already?
        os.mkdir(folder_name)        # If not, create one.
        
    plt.axis('off') # Do not print the axes on the images.
    
    N = matrix.shape[0]
    evol = evolution(matrix,T)
    
    for i in range (T):
        data = evol[i]

        # Need to rescale: https://stackoverflow.com/questions/16755147/set-the-size-of-imsave-image-output
        new_data = np.zeros(np.array(data.shape) * image_size)

        for j in range(data.shape[0]):
            for k in range(data.shape[1]):
                new_data[j * image_size: (j+1) * image_size, k * image_size: (k+1) * image_size] = data[j, k]    

        plt.imsave("./%s/%s%s.png"%(folder_name,file_name,i), new_data, format="png")
            
    print('The images are stored in folder "./graphics_export" under the names "game_of_life_%d.png".')


def cross_shaped_matrix(N):
    '''Returns the matrix with 1 on both diagonals, as np.array of shape (N,N).
    Input: N = non-negative integer.'''
    
    matrix = np.zeros((N,N), dtype=int)
    
    for i in range(N):
        matrix[i][i] = 1
        matrix[i][N-1-i] = 1    
    
    return matrix