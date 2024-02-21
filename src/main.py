"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
from motor_driver import MotorDriver
from encoder_reader import Encoder
from motor_controller_Nathan import MotorController
import utime


def task1_fun(setpoint, gain):
    """!
    Task which runs motor 1. Initiliazes then calls run()
    @param setpoint Defines the desired setpoint of the controller
    @param gain Defines the proportional gain of the controller
    """
    
    # Initialize motor drivers and encoders
    # set up timer 8 for encoder 2
    TIM8 = pyb.Timer(8, prescaler=1, period=0xFFFF) # Timer 8, no prescalar, frequency 100kHz
    #Define pin assignments for encoder 2
    pinc6 = pyb.Pin(pyb.Pin.board.PC6)
    pinc7 = pyb.Pin(pyb.Pin.board.PC7)
    # Create encoder object
    Jerry = Encoder(pinc6, pinc7, TIM8)
    
    # setup motor
    TIM5 = pyb.Timer(5, freq=2000) # Timer 5, frequency 2000Hz
    # Define pin assignments for motor 2
    pinc1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    pina0= pyb.Pin(pyb.Pin.board.PA0)
    pina1 = pyb.Pin(pyb.Pin.board.PA1)    
    # Create motor driver
    Tom = MotorDriver(pinc1, pina0, pina1, TIM5)
    Jerry.zero()
    # Create motor controller
    Deitch = MotorController(gain, setpoint, Tom.set_duty_cycle, Jerry.read)
    
    while True:
        Deitch.run()
        yield

def task2_fun(setpoint, gain):
    """!
    Task which runs motor 2. Initializes then calls run()
    @param setpoint Defines the desired setpoint of the controller
    @param gain Defines the proportional gain of the controller
    """
    # Get references to the share and queue which have been passed to this task
    the_share, the_queue = shares
    
    # Initialize motor drivers and encoders
    # Set up timer 4 for encoder 1
    TIM4 = pyb.Timer(4, prescaler=1, period=0xFFFF) # Timer 4, no prescalar, frequency 100kHz
    # Define pin assignments for encoder 1
    pinb6 = pyb.Pin(pyb.Pin.board.PB6)
    pinb7 = pyb.Pin(pyb.Pin.board.PB7)
    # Create encoder object
    Jess = Encoder(pinb6, pinb7, TIM4)
    
    # setup motor
    TIM3 = pyb.Timer(3, freq=2000) # Timer 3, frequency 2000Hz
    # Define pin assignments for motor 1
    pina10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinb4= pyb.Pin(pyb.Pin.board.PB4)
    pinb5 = pyb.Pin(pyb.Pin.board.PB5)
    # Create motor driver
    Jackie = MotorDriver(pina10, pinb4, pinb5, TIM3)
    Jess.zero()
    # Create motor controller
    AA = MotorController(gain, setpoint, Jackie.set_duty_cycle, Jess.read)
    
    while True:
        AA.run()
        yield

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing two motor at once"
          "Press Ctrl-C to stop and show diagnostics.")
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    gain1 = 0.2
    setpoint1 = 36000
    my_share.put(gain1, setpoint1)
    
    gain2 = 0.2
    setpoint2 = -36000
    my_share.put(gain2, setpoint2)
    
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=400,
                        profile=True, trace=False, gain1, setpoint1)
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=1500,
                        profile=True, trace=False, gain2, setpoint2)
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break
    
    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
