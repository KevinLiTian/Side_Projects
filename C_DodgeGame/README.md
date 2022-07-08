# Overview & Demonstration
In the second year of Electrical & Computer Engineering at the University of Toronto St.George campus, ECE243 is a course aims for students to learn the connection between software and hardware. This course teaches programming in ARM Assembly, C and Verilog. The final project of the course is either a software project in C or a processor project in Verilog. My teammate Hongyu Chen <francois.chen@mail.utoronto.ca> and I chose to do a software project. <br/>

This project is a embedded C program/game working on the DE1-SOC board, also can be simulated on the CPUlator web software https://cpulator.01xz.net/?sys=arm-de1soc. This game used the VGA display double buffer, text display buffer and also interrupt in the DE1-SOC board. Here's a quick overview of what the game looks like.<br/>

## Start Screen  
The start screen is coded by telling the VGA display which pixels should light up using their address. <br/>

![StartScreen](https://user-images.githubusercontent.com/99038613/169934786-826bcaec-eac0-4300-a56f-57b4a96131ee.png)
  
## Help Screen
When the users hit the 'H' key on the keyboard, the program will switch to a help screen which is also coded by lighting up certain pixels on the VGA display. The small words are displayed using the text display buffer of the DE1-SOC board. <br/>

![Help](https://user-images.githubusercontent.com/99038613/169934848-093d159e-af15-4a48-8d22-ab58424429d2.png)
  
## Game Screen
The game starts when the users hit the 'Enter' key on the keyboard. The users can control the blue box on the bottom of the screen to move in four directions using either 'W', 'A', 'S', 'D' keys or the arrow keys on the keyboard. If the blue box hit the obstacles (obstacles are moving in random directions), the player loses. If the blue box hit the top of the screen, the player wins. <br/>

https://user-images.githubusercontent.com/99038613/169935436-91a11c36-d9c3-4741-b1d8-4e8ba6e40415.mp4

## Restart Screen
The restart screen appears either when the player loses or wins. If the player wins, the 'Restart' word will be in green and if the player loses, this word will be in red. <br/>

![Restart](https://user-images.githubusercontent.com/99038613/169934880-37310858-05c6-418f-8ad9-d01712803228.png)

## Contact ME
If you are interested in the source code or the original documentations, please do contact me through my email kevintian.li@mail.utoronto.ca or kevin.li20021106@gmail.com. You have to prove that you are not a current ECE243 student since this will be an academic integrity issue. If you are, try to think and code it yourself as it will be a great practice to improve your software engineering skills; though if you have any questions, feel free to share it with me!
