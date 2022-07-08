# Overview
In the second year of Electrical & Computer Engineering at the University of Toronto St.George campus, ECE243 is a course aims for students to learn the connection between software and hardware. This course teaches programming in ARM Assembly, C and Verilog. This project is one of the labs of this course.

This project is in ARM Assembly, working on the DE1-SOC board, also can be simulated on the CPUlator web software https://cpulator.01xz.net/?sys=arm-de1soc. There are two independent programs: the "HEX.s" and the "Counter.s".

## HEX
HEX is a program that detects interrupt from the push buttons on the DE1-SOC board, the corresponding HEX display will show numbers 1, 2 or 3 depending on which bottons has been pressed.

##### Video Demo
https://user-images.githubusercontent.com/99038613/169944576-71e4a2c2-713e-4cae-92f9-632fdbde0b19.mp4

## Counter
Counter is a program that displays using both the LEDs and the HEX display. 
- The LEDs works as a binary counter that can be controlled by the push buttons.
  - Button 0 controls the start/stop of the binary counter
  - Button 1 speeds up the binary counter by 2x
  - Button 2 slows down the binary counter by 2x
- The HEX display works as a real-time clock, shows seconds from 00:00 to 59:99. 
  - Button 3 controls the start/stop of the clock
##### Video Demo
https://user-images.githubusercontent.com/99038613/169944923-21f760a2-561f-46a5-bde8-c3aefb69439c.mp4

## Contact ME
If you are interested in the source code or the original documentations, please do contact me through my email kevintian.li@mail.utoronto.ca or kevin.li20021106@gmail.com. You have to prove that you are not a current ECE243 student since this will be an academic integrity issue. If you are, try to think and code it yourself as it will be a great practice to improve your skills; though if you have any questions, feel free to share it with me!
