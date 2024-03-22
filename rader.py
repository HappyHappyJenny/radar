import tkinter as tk
import math
import serial
import time


WIDTH = 640
HEIGHT = 480
angle = 0
direction = 0
sendingAngle = 0

#[angle,distance] #2 dimension list
objects = [[0,0],[10,0],[20,0],[30,0],[40,0],[50,0],[60,0],
           [70,0],[80,0],[90,00],[100,0],[110,0],[120,0],
           [130,0],[140,0],[150,0],[160,0],[170,0],[180,0]] 

ser = serial.Serial("COM6",115200)


def btcmd():
    print("hello world")

def drawObject(angle, distance):
    radius = WIDTH / 2
    x = radius + math.cos(angle * math.pi / 180) * distance
    y = radius - math.sin(angle * math.pi / 180) * distance
    canvas.create_oval(x-5, y-5, x+5, y+5, fill='green')
    

def updateScan():
    global angle
    global direction
    global objects
    global sendingAngle
    receiveDistance = 0
    #transmit angle
    if angle % 10 == 0 :
        sendingAngle = angle
        mask = b'\x7f' #bite
        ser.write(bytes(bytearray([0x02, 0x52])))
        angleH  =  (angle >> 7) + 128
        angleL = (angle & mask[0]) + 128
        crc = (0x02 + 0x52 + angleH + angleL) % 256
        ser.write(bytes(bytearray([angleH,  angleL, crc, 0x03])))
    #recieve distance
    if ser.in_waiting > 0 :
        data = ser.read()
        if data == b'\x02' :
            #wait for second byte
            timeout = time.time() + 0.002
            lostData = False
            while ser.in_waiting < 5 :
                #make timeout
                if time.time() > timeout :
                    lostData = True
                    break
            if lostData == False :
                data = ser.read(5) #if read success, read 5 at once
                if data[0] == 65  : #'A'
                    #checking CRC
                    crc = (2 + data[0] + data[1] + data[2]) % 256
                    if crc == data[3]:
                        if data[4] == 3:
                            #pasing data
                            mask = b'\x7f' #means byte ary
                            data_one = bytes([data[1] & mask[0]])
                            receiveDistance = int.from_bytes(data_one) <<7
                            data_one = bytes([data[2] & mask[0]])
                            receiveDistance += int.from_bytes(data_one)
                            #update object
                            for obj in objects :
                                if obj[0] == sendingAngle :
                                    obj[1] =  receiveDistance
                             
    #clear canvas
    canvas.delete('all')
    #drawing line
    radius = WIDTH / 2
    length = radius #length of line
    x = radius + math.cos(angle * math.pi / 180) * length
    y = radius - math.sin(angle * math.pi / 180) * length
    canvas.create_line(x, y, radius, radius, fill='green', width=4)
    #drawing object
    for obj in objects :
        drawObject(obj[0], obj[1])
    #update angle
    if direction == 0 :
        angle +=1
        if angle == 181 :
            direction = 1
    else :
        angle -= 1
        if angle == -1 :
            direction = 0

    #self call 
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

