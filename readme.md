# Formify

## 💫 Inspiration
Several of our teammates have seen loved ones go through physical therapy (PT) for up to a year due to injury, or for well past a decade for disability management. We recognize that getting to PT appointments in person can be inaccessible not only due to cost, but because the same injuries that must be treated can prevent you from even walking out the door without a caregiver to carry you. Unfortunately, only 35% of patients adhere to their prescribed at-home programs (Argent et al., 2018) and telehealth appointments in the field are not feasible with video calls alone. Informed by interviews with people directly affected by this problem, we've designed a system to make at-home physical rehabilitation a viable option.

## 🦾 What it Does
Formify is a web-accessible program that can monitor a users motion in real time and provide haptic feedback to guide them through prescribed exercises. Let's take a step-by-step look at the appointment process:

Step One: Access the Formify web server. You'll be greeted by the first exercise that your physical therapist has assigned you.

Step Two: Put on your Formify haptic glove. Instead of multiple attachments or a full body suit, we can map feedback for your entire body onto one wearable in the palm of your hand. The motor homonuculus map shows us that our hands are our most sensitive body parts to touch, meaning the brain can differentiate between two vibrations mere nanometers away from each other. In the palm of the glove lies a complete diagram of the body, where precise vibrations can alert you to which joint needs your attention. Since we didn't have small precise vibrating modules during the hackathon, we've provided two example vibration points.

Step Three: Watch and repeat. Your PT has provided us with a demonstration video for this exercise. See how it's done and continue when you're ready. Now, you can see yourself next to the video; try to follow along with it. Movement points have also been placed on top of your livestream to help guide you. If you fall out of line with the pose, your glove will show you which body part to move back into place. Most importantly, don't stress if you can't reach! Your doctor has told us how far along you are in your recovery, and we've adjusted your margin of error accordingly.

### How we Built It
Hardware: We use a compression glove to embed the hardware. A nano esp32 controls the circuit, powered by a portable battery via usb-c. The board sends voltage out to pins that govern each vibrating motor. It hosts its own wifi server that listens for AJAX http requests from our main web server to control which vibrators are triggered.

Backend: We utilized OpenCV and MediaPipe's landmark pose detection framework to extract and track key data points from video footage and real-time camera feeds, generating data sets for each input type. We then created a program to read from the datasets, continuously comparing the landmarks from the real-time footage as it updates against the landmarks extracted from the video footage.

Frontend: The frontend serves as our user interface, facilitating seamless connections between users and the backend. We utilized HTML, CSS, and JavaScript to develop an interactive and responsive interface that enhances user experience.

## 📊 Challenges we Ran Into
Wireless connectivity took multiple iterations as bluetooth libraries were not supported, then several devices could not produce wifi hotspots with the right specifications for the esp32. Connecting wires robustly was difficult as pieces sliped, broke or lost contact many times in practice. We had to try multiple options of both things. On the software side, implementing and properly adding the specific variables required for the datasets was difficult as it required a deeper knowledge of understanding data structures and the process of working with the AI driven libraries we might not be fully familiar with. Another difficulty was comparing the datasets between the demonstration video, and the live stream capturing the patient on camera. It led to many moments of trial and error as one dataset wouldn't match with the other in some way shape or form.

## 🥇 Accomplishments that We're Proud of
75% of this team are first time hackers, one of those three is not a CECS major. The final person has only attended one hackathon. Because of this, we are extremely proud to have completed a project that feels close to and end-to-end product. This team began as two duos: one pair looking to do real-time computer vision, and one looking to create a haptic feedback system. Instead of splitting off because we were going in different directions, we decided to put our heads together to attack a problem from multiple angles. We are so proud of how we were able to communicate, split responsibilities between members, and get our parts done. Having a glove as opposed to wristband, having multiple separate vibration points instead of just on/off, and having more than one exercise were all originally moonshot ideas that we were able to implement.

## 🗣️ What we Learned
How to connect to hardware wirelessly, and how to control it via web server. How to send and receive AJAX http requests. How to intergrate and use computer vision and AI object detection frameworks as well as coordinate tracking, generating, reading from, and comparing datasets and landmarks using multiple libraries, frameworks, and languages. Implemented libraries like OpenCV to help process images and record the data using Excel spreadsheets, Google Mediapipe to detect the pose landmark sections, and Flask to design a minimalistic web app for the purpose of helping online physical rehabilitation.

## 💨 What's Next for Formify
Most importantly, more interviews with PT patients. We believe that communities design for their own needs best. The next iteration of our current system would work towards fully implementing the body diagram with precision motors, including more exercise videos (or linking to a physical therapy stock library as those softwares exist), and allowing more intensity levels for better control over margin of error.

## 🔨 Built With
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)

## 📖 Notes
start a virtual environment: run this in the terminal .\venv\Scripts\activate
then start the server by running flask 

columns of the csv: n, m, x, ab_pose_x where a is seconds, b is frame, pose is either hand or pose, x is the coordinate, either x, y or z

### Thank You.
