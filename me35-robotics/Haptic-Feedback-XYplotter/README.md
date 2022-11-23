# Haptic-Feedback-XYplotter

This project utilized haptic feedback in order for the controller to detect a letter. We utilized a joystick controlled xy plotter to accomplish this goal. The system worked by 
sending haptic feedback signals over UART between two EV3 bricks. Below are the write and read main codes for control.

## ```write.py```

This is the write code for operation. It reads in the control data from the joystick and then writes if a color other than white was detected over UART.

## ```read.py```

This is the read code for operation. It reads in color state and writes out the controller data over UART

## Complete Project Documentation: 

If you would like to check out the complete documentation for this project, click [this](https://owengervais.myportfolio.com/xyplotter-and-joystick) to be sent to my project portfolio.
