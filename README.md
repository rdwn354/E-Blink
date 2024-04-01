# **E-Blink**
E-blink is a program to track eye blinks using a camera, it uses a CNN algorithm to classify between closed and open eyes.

## Spesification and Os
1. Raspberry Pi 3 Model b+
2. 7inch Capacitive Touch Screen LCD (H) with Case, 1024×600, HDMI, IPS, Various Systems Support
3. Os Raspbian GNU/Linux 11 (bullseye)
   
## Install Package and Dependencies
- pyhton 3.9.2
- opencv 4.6.0
- matplotlib 3.3.4
- tflite-runtime

### Install OpenCV Raspberry
1. sudo git clone https://github.com/freedomwebtech/rpi-bullseye-opencv4.5.5.git
2. cd rpi-bullseye-opencv4.5.5
3. sudo chmod 775 install.sh
4. sudo ./install.sh
this step will be take at least 2 hours

### Install Matplotlib
1. sudo apt-get update && sudo apt-get upgrade
2. sudo apt install python3-matplotlib

### Install tflite-runtime
1. sudo apt-get update && sudo apt-get upgrade
2. pip install tflite-runtime


