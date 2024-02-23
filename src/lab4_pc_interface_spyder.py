"""!
@file lab3_pc_interface.py

Run real or simulated dynamic response tests and plot the results. This program
demonstrates a way to make a simple GUI with a plot in it. It uses Tkinter, an
old-fashioned and ugly but useful GUI library which is included in Python by
default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Jessica Perez, Jacquelyn Banh, and Nathan Chapman
@date   2024-02-13 Original program, based on example from above listed source
@copyright (c) 2024 by Jessica Perez, Jacquelyn Banh, and Nathan Chapman and released under the GNU Public Licenes V3
"""

# import math
# import time
import tkinter 
import serial

#from time import sleep
# from random import random
# from matplotlib import pyplot 
#from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    Make an example plot to show a simple(ish) way to embed a plot into a GUI.
    The data is just a nonsense simulation of a diving board from which a
    typically energetic otter has just jumped.
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    """
    #Clearing the array
    xaxis_times.clear()
    yaxis_motor_positions.clear() 
    go1 = False
    go2 = False
    
    # Importing data (time, voltage) from the mircontroller
    with serial.Serial(port='COM5', baudrate=115200, timeout=1) as ser:
        ser.write(b'\x03')
        ser.write(b'\x04')
        #ser.write(b'import main\n')
        while not go1 or not go2:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            if line == 'done 1':
                go1 = True
            if line == 'done 2':
                go2 = True

        # Read and discard any data in the input buffer
        while ser.in_waiting > 0:
            print(ser.readline().decode('utf-8'))
        print("Serial input buffer cleared.")    
        ser.write(b'\x03')
        while ser.in_waiting == 0:
            continue
        
        #read output from microcontroller
        for line in ser:
            data = ser.readline().decode('utf-8').strip()
            
            try:
                # Split the received data into time and voltage
                time, voltage = map(float, data.split(','))
                xaxis_times.append(time)
                yaxis_motor_positions.append(voltage)
                
            except ValueError:
                print("Error parsing data:", data)
                continue
        
        #Checking Array
        print(xaxis_times)
        print(yaxis_motor_positions)
       
        # plotting the experimental curves
        plot_axes.plot(xaxis_times, yaxis_motor_positions)
        plot_axes.set_xlabel(xlabel)
        plot_axes.set_ylabel(ylabel)
        plot_axes.grid(True)
                     
        ser.close()

def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title('Step Response Plot')

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    #Creates an empty array
    xaxis_times = []
    yaxis_motor_positions = []
    
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Voltage (V)",
               title="Step Response Plot")



