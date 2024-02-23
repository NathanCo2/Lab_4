# Lab_4: One Task is (almost) Never Enough

ME 405-04 with Dr. Ridgely

Members: Jacquelyn Banh, Nathan Chapman, Jessica Perez

Tub: mecha06

Lab 04 Program Description:

The objective of this lab is to develop a real-time scheduler and test its performance. The scheduler allows the program to perform multitasking between various components of our system. Utilizing the code developed in previous labs, our team created a code that contains two tasks capable of running two motors under closed-loop control simultaneously. To test the code we examined the motors through different distances and held them at the desired positions. 

Before testing both of the motors, the motor task was created and tested with a flywheel, printing the results and plotting the step response plots. The objective was to run the task at a slower rate until the controller's performance worsened, which can be seen in Figure 1. To obtain the slowest rate at which the performance is not significantly worsened, the period was adjusted until an oscillation occurred. 

[IMAGE HERE]

Figure 1: Plot of Time, s, and Position, volts, for Controlled Performance using Flywheel. The left image shows the optimal response rate and the image to the right shows the poor response rate. The slowest rate at which the performance is not significantly worse is _.  

To compare the positions between the two motors, both positions were captured and plotted in Figure 2 and Figure 3. [FINISH]

![image0](https://github.com/NathanCo2/Lab_4/assets/156122419/4ae39982-bd4c-48e7-91cb-c5445c1f4d76)

Figure 2: Plot of Time, s, and Position, volts, for Motor 1 and Motor 2

![image1](https://github.com/NathanCo2/Lab_4/assets/156122419/ad1a4b9d-0043-488f-a7cb-f872176cb579)

Figure 3: Zoomed-in Plot of Time, s, and Position, volts, for Motor 1 and Motor 2 from Figure 1

Before 
