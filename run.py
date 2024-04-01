import os
import sys

print("E-Blink".center(50,"-"))

print()
print("command")
print("1 ==> Start program")
print("2 ==> Data Visualize")
print("3 ==> Review")
print("4 ==> exit")
command = input(str("Please insert command : "))
print()

if command == "1":
    os.system("python3 calculate.py")
elif command == "2":
    os.system("python3 visualize.py")
elif command == "3":
    os.system("python3 review.py")
elif command == "4":
    sys.exit()
else :
    print("Command not found :v")

