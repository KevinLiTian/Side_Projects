# Overview
In the second year of Electrical & Computer Engineering at the University of Toronto St.George campus, ECE243 is a course aims for students to learn the connection between software and hardware. This course teaches programming in ARM Assembly, C and Verilog. This project is one of the labs of this course.

This project is in C, working on the DE1-SOC board, also can be simulated on the CPUlator web software https://cpulator.01xz.net/?sys=arm-de1soc. There are three independent programs: the "draw_lines.c", the "moving_line.c" and the "bouncing_boxes.c".

## Draw Lines
This program uses the "Bresenham's Line Algorithm" to draw lines on the VGA display of the DE1-SOC board. First determine which pixels should be lighted up using the algorithm and then use the address of the pixels to light them up. <br/>

![Lines](https://user-images.githubusercontent.com/99038613/169946923-cde67371-e975-4f04-b58b-5791806bf652.png)

## Moving Line
This program uses the VGA double buffer of the DE1-SOC board to animate a line moving between the top of the screen and the bottom of the screen, bouncing back when it hits either side.

##### Video Demo
https://user-images.githubusercontent.com/99038613/169947352-ee7707ad-9525-4b3c-bc47-aa6afad18665.mp4

## Bouncing Boxes
This program uses the VGA double buffer of the DE1-SOC board to animate 8 randomly located boxes travelling in random directions and the colours of the boxes are also random. There are random coloured lines connecting each of the two boxes, lines are calculated real-time using the "Bresenham's Line Algorithm". The boxes bounces off the side of the screens. 

##### Video Demo
https://user-images.githubusercontent.com/99038613/169947674-71fbc1f7-e68a-4b64-95a4-d5e0785daa39.mp4


## Contact ME
If you are interested in the source code or the original documentations, please do contact me through my email kevintian.li@mail.utoronto.ca or kevin.li20021106@gmail.com. You have to prove that you are not a current ECE243 student since this will be an academic integrity issue. If you are, try to think and code it yourself as it will be a great practice to improve your skills; though if you have any questions, feel free to share it with me!
