import tkinter as tk
import math

WIDTH = 640
HEIGHT = 480
angle = 0

def btcmd():
    print("hello world")
   

def updateScan():
    global angle
    #clear canvas
    canvas.delete('all')
    angle = angle + 1
    if angle> 359 :
        angle = 0
    x = 320 + math.cos(angle * math.pi / 180) * 200
    y = 240 - math.sin(angle * math.pi / 180) * 200
    canvas.create_line(320,240,x,y,fill='red',width=2)
    canvas.after(50,updateScan)



#개체 call
root = tk.Tk()
root.title("Ultrasonic Radar")
canvas = tk.Canvas(root, width=WIDTH, height = HEIGHT, bg="black")
button = tk.Button(root, text='종료',command = btcmd)
button.pack()
canvas.pack()


#canvas drawing
##canvas.create_line(10,10,100,100,fill='red',width=2)


#display
updateScan()
root.mainloop()

