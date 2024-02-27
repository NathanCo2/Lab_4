"""!
@file motor_controller.py

This program demonstrates the development of a class called MotorController to that
perform closed-loop proportional control. This code was tested an ranwith the Motor
Driver class and Encoder class developed in the previous labs to examine if the code
was running correctly. 

@author Jessica Perez, Jacquelyn Banh, and Nathan Chapman
@date   2024-02-13 Original program, based on example from above listed source
@copyright (c) 2024 by Jessica Perez, Jacquelyn Banh, and Nathan Chapman and released under the GNU Public Licenes V3
"""

import pyb
import utime
import cqueue
from encoder_reader import Encoder

class MotorController:
    """! 
    This class implements the Motor Controller for an ME405 kit. 
    """

    def __init__ (self, Pgain, Igain, setpoint, setdutycycle_f, getactual_f, timequeue, valqueue):
        """! 
        Creates an encoder object that can be used to measure
        the position of a motor
        @param Pgain = Kp, percent duty cycle/encoder count
        @param Igain = Ki
        @param setpoint = desired angle of motor
        @param setdutycycle_f = function to set duty cycle output
        @param getactual_f = function to read actual value
        """
        self.setpoint = setpoint
        self.Pgain = Pgain
        self.Igain = Igain
        self.actual = 0
        self.err = 0
        self.setdutycycle = setdutycycle_f
        self.getactual = getactual_f
        self.timequeue = timequeue # queue for time
        self.valqueue = valqueue # queue for values
        self.esum = 0 #error sum to be used for I control
        self.oldt = utime.ticks_ms() # delta t to be used for I control
        
    def run(self):
        """!
        This method will run one pass of the control algorithm
        """
        self.actual = self.getactual() # call read encoder function and get delta total
        #print(f'actual encoder position {self.actual}')
        self.err = self.actual - self.setpoint
        #print(f'err {self.err}')
        self.esum += (utime.ticks_ms()-self.oldt)/1000*self.err
        #self.esum += self.err
        self.PWM = self.err*self.Pgain + self.esum*self.Igain
        self.PWM = max(min(self.PWM, 100), -100)
        #print(f'PWM {self.PWM}')
        self.setdutycycle(self.PWM)
        self.oldt = utime.ticks_ms()
        self.timequeue.put(utime.ticks_ms()) # puts time in queue
        self.valqueue.put(self.actual) # puts PWM in queue
        
    def set_setpoint(self,setpoint):
        """!
        This method sets up the setpoint for proportional control
        @param setpoint = desired angle of motor
        """
        self.setpoint = setpoint
        
    def set_Kp(self,Pgain):
        """!
        This method sets up the gain for proportional control
        @param gain = Kp, percent duty cycle/encoder count
        """
        self.Pgain = Pgain
        
    def set_Ki(self, Igain):
        """!
        This method sets up the gain for Integral control
        @param gain = Ki
        """
        self.Igain = Igain    
        
    def controller_response(self):
        """!
        This method will print the results obtained of the step
        response and print when the step response is done running
        """  
        self.time = []
        self.val = []
        while self.timequeue.any():#Checks if anything is the Queue and emptying it
            self.time.append(self.timequeue.get()) #Gets single value from queue
            self.val.append(self.valqueue.get())
        self.firsttime = self.time[0]
        self.time_offset = [t - self.firsttime for t in self.time]
        for i in range(len(self.time_offset)):
            print(f"{self.time_offset[i]}, {self.val[i]}")

# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program           
if __name__ == "__main__":

    from motor_driver import MotorDriver
    from encoder_reader import Encoder
    import utime

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

    # setup motor controller
    Jerry.zero()
    time1 = cqueue.FloatQueue(500)
    val1 = cqueue.FloatQueue(500)
    setpoint = 15000
    KP = 0.9
    KI = 0.2
    Deitch = MotorController(KP, KI, setpoint, Tom.set_duty_cycle, Jerry.read, time1, val1)

    for i in range(500):
        Deitch.run()
        utime.sleep_ms(1)

    Deitch.controller_response()
    Tom.set_duty_cycle(0)
