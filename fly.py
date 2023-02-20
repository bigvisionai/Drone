import cv2
from time import sleep 
import keyboard as key 
from djitellopy import tello 
from detection import *
from ultralytics import YOLO 

def controls():
    lr, fb, ud, rot = 0, 0, 0, 0
    speed = 50 

    if key.getKey("LEFT"): lr = -speed
    if key.getKey("RIGHT"): lr = speed

    if key.getKey("UP"): fb = speed 
    if key.getKey("DOWN"): fb = -speed 

    if key.getKey("w"): ud = speed 
    if key.getKey("s"): ud = -speed

    if key.getKey("a"): rot = -speed 
    if key.getKey("d"): rot = speed

    if key.getKey("t"): drone.takeoff()
    if key.getKey("l"): drone.land()

    return [lr, fb, ud, rot]


# Initializations.
key.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()

# Create the video writer.
out = cv2.VideoWriter('rec.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (960, 720))
model = YOLO('yolov8n.pt')


while True:
    vals = controls()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = drone.get_frame_read().frame
    det_img = draw_predictions(img.copy(), model)
    print(img.shape)
    cv2.imshow('Stream', det_img)
    out.write(det_img)
    wait = cv2.waitKey(1)
    if wait == ord('q'):
        break

    if key.getKey("c"):
        print('Program Terminated')
        print('\n Thanks for flying Tello.')
        break

# Release the video writer.
out.release()
