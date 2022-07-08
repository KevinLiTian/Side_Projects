/* Filename: roomAssignByNames
Written by KL
Oct.15th, 2021
Notes:
Hey guys you can try to use this code to see which room you are in for the ECE244 midterm.
I'm just kinda bored and want to do something so I wrote this program. This is for ECE244 midterm
only. I'm not sure if this code works perfectly so always double check, I don't want to get you to sit
in a wrong room LOL. You almighty programmers can point out where is wrong and what can be improved.
This is just half an hour work so I only wrote a little.
*/

#include <iostream>
using namespace std;

void assignRoom(string);

int main()
{
    string input;         //User input
    char confirmInput;    //Just to confirm
    bool confirm = false; //Just to confirm

    while (confirm == false)
    { //If not confirmed, re-enter name
        cout << "Please enter your last name(uppercase first letter), followed by a ','" << endl;
        cout << "followed by your first name(uppercase first letter): ";
        cin >> input;
        cout << "You have entered " << input << ", if this is correct, please enter 'Y', otherwise, enter 'N': ";
        cin >> confirmInput;

        if (confirmInput == 'Y' || confirmInput == 'y')
        { //If confirmed, call assignRoom function to assign room
            confirm = true;
            assignRoom(input);
        }
        else
        { //If not confirmed, re-enter name
            confirm = false;
        }
    }
}

void assignRoom(string a)
{
    string roomName[6] = {"Hugh,Ethan", "Liang,Anna", "Nauman,Mustafa", "Son,Roy", "Xiao,Yufeng", "Zuo,Yixian"}; //Could be modified for other exams
    string room[6] = {"BA1160", "BA1180", "BA1190", "GB304", "MC252", "MC254"};                                  //Could be modified for other exams

    for (int i = 0; i < 6; i++)
    {
        if (a.compare(roomName[i]) <= 0)
        {                                                         //If the name is within the range of the room
            cout << "Your assigned room is: " << room[i] << endl; //Assign to that room
            system("pause");
            return;
        } //Otherwise keep comparing
    }
    cout << "TBH, you have quite a strange name." << endl; //Who are you alien, you don't belong here.
    system("pause");
}
