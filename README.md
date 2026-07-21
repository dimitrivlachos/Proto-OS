# Proto-OS

> [!WARNING]
> **This repository has been moved!**
>
> Development of Proto-OS has moved to a different account that I keep separate from my professional work. This copy is left up for historical reference only - issues and PRs here will not be reviewed, and the code will not be updated.
>
> **If you'd like the link to the active repository, or want to get in touch about the project, please reach out:**\
> _dimitri.j.vlachos@gmail.com_\
> (Otherwise, you can reach out to me on socials on my GitHub profile or LinkedIn).
>
> I'm happy to share the new location 1:1; I'd just rather not publish it here.

---

### **This project is a work in progress and is not yet ready for use.**

## What is Proto-OS?
Proto-OS is designed to be an 'operating system' for a Protogen suit head. It is designed to use computer vision and machine learning to track the user's eye position and facial expression and mimic them on the character's face display.

## What is a Protogen?
A Protogen is a type of cyborg character. They have a robotic face display that can be used to show their emotions and eye position.

For example:
![Protogen](https://i.imgur.com/wytIGhG.png)

3D models I am printing:
![3D Models](https://public-files.gumroad.com/e8p44m4j4c5kldcsdua7xrmd64kj)

## How does it work?
Proto-OS uses a Raspberry Pi 4B with a camera module to track the user's eye position and facial expression. These are mounted inside the suit head, with the camera facing the user. The Raspberry Pi is connected to the camera via a long ribbon cable and runs a Python script that uses OpenCV to track the user's eye position and Tensorflow Lite to track their facial expression. The script then sends the eye position and facial expression data to two Raspberry Pi Zeros via serial communication.

The Zeros then run my custom graphics library for the Pimoroni Unicorn HD Hat (An RGB LED Matrix) to display the eye position and facial expression on the character's face display.

Here is matrix, which would account for a single eye:
![Image of the Unicorn Hat HD](https://shop.pimoroni.com/cdn/shop/products/uhhd-1_768x768.jpg?)
