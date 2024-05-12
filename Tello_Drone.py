from tkinter import *
from PIL import Image, ImageTk
from djitellopy import tello
import time
import cv2


window = Tk()
window.geometry('1300x700')
program_icon = PhotoImage(file="resource/tello_drone.png")
window.iconphoto(True, program_icon)
window.title("Tello Drone")

drone = tello.Tello()
speed = 10
color = "lightGray"

global cap
ret = True


def dark_theme_state():
    global color
    color = "Black"


dark_theme = Button(window, text="dark Theme", command=dark_theme_state)
dark_theme.place(x=20, y=200)


def connect():
    global cap
    drone.connect()
    drone.streamon()
    cap = drone.get_frame_read()
    info()
    tello_camera()


def tello_camera():
    global cap, ret
    if cap is not None:
        frame = cap.frame
        if ret is True:
            frame = cv2.resize(frame, (500, 300))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            ed.configure(image=img)
            ed.image = img
            ed.after(10, tello_camera)
        else:
            ed.image = ""
            drone.streamoff()


def info():
    hg.config(text=f"Height: {drone.get_distance_tof()}")
    bt.config(text=f"Element: {drone.get_battery()}")
    tm.config(text=f"Drone temperature: {drone.get_temperature()}")
    hg.after(100, info)


def take_photo():
    img = drone.get_frame_read().frame
    cv2.imwrite(f'resource/tello_photo/{time.time()}.jpg', img)
    time.sleep(0.3)


def move_forward():
    drone.send_rc_control(0, speed, 0, 0)


def move_back(event):
    drone.send_rc_control(0, -speed, 0, 0)


def move_left(event):
    drone.send_rc_control(-speed, 0, 0, 0)


def move_right(event):
    drone.send_rc_control(speed, 0, 0, 0)


def move_up(event):
    drone.send_rc_control(0, 0, speed, 0)


def move_down(event):
    drone.send_rc_control(0, 0, -speed, 0)


def move_rotate_right(event):
    drone.send_rc_control(0, 0, 0, speed)


def move_rotate_left(event):
    drone.send_rc_control(0, 0, 0, -speed)


def move_left_and_forward(event):
    drone.send_rc_control(-speed, speed, 0, 0)


def move_right_and_forward(event):
    drone.send_rc_control(speed, speed, 0, 0)


def move_left_and_back(event):
    drone.send_rc_control(-speed, -speed, 0, 0)


def move_right_and_back(event):
    drone.send_rc_control(speed, -speed, 0, 0)


def speed_control(event):
    global speed
    speed = sp.get()


tf = Button(window, text="Takeoff", bg=color, activebackground="green", width=20, command=lambda: drone.takeoff())
tf.place(x=20, y=20)

ld = Button(window, text="Land", bg=color, activebackground="green", width=20, command=lambda: drone.land())
ld.place(x=20, y=60)

taf = Button(window, text="Throw and Fly", bg=color, activebackground="green", width=20, command=lambda: drone.send_control_command("throwfly"))
taf.place(x=20, y=100)

fr = Button(window, text="Forward", bg=color, activebackground="green", width=7, height=3, command=lambda: drone.send_rc_control(0, 0, 0, 0))
fr.bind('<Button-1>', move_forward)
fr.place(x=120, y=410)

bc = Button(window, text="Back", bg=color, activebackground="green", width=7, height=3, command=lambda: drone.send_rc_control(0, 0, 0, 0))
bc.bind('<Button-1>', move_back)
bc.place(x=120, y=620)

UP = Button(window, text="Up", bg=color, activebackground="green", width=7, height=3, command=lambda: drone.send_rc_control(0, 0, 0, 0))
UP.bind('<Button-1>', move_up)
UP.place(x=1120, y=410)

dn = Button(window, text="Down", bg=color, activebackground="green", width=7, height=3, command=lambda: drone.send_rc_control(0, 0, 0, 0))
dn.bind('<Button-1>', move_down)
dn.place(x=1125, y=620)

icon = PhotoImage(file='resource/left_rotation.png')
icon1 = PhotoImage(file='resource/right_rotation.png')
icon2 = PhotoImage(file='resource/right.png')
icon3 = PhotoImage(file='resource/left.png')
icon4 = PhotoImage(file='resource/front_flip.png')
icon5 = PhotoImage(file='resource/back_flip.png')
icon6 = PhotoImage(file='resource/left_flip.png')
icon7 = PhotoImage(file='resource/right_flip.png')
icon8 = PhotoImage(file='resource/up_right.png')
icon9 = PhotoImage(file='resource/up_left.png')
icon10 = PhotoImage(file='resource/back_right.png')
icon11 = PhotoImage(file='resource/back_left.png')
icon12 = PhotoImage(file='resource/camera.png')


rl = Button(window, image=icon, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.send_rc_control(0, 0, 0, 0))
rl.bind('<Button-1>', move_rotate_left)
rl.place(x=10, y=510)

rr = Button(window, image=icon1, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.send_rc_control(0, 0, 0, 0))
rr.bind('<Button-1>', move_rotate_right)
rr.place(x=230, y=510)

mr = Button(window, image=icon2, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.send_rc_control(0, 0, 0, 0))
mr.bind('<Button-1>', move_right)
mr.place(x=1225, y=510)

ml = Button(window, image=icon3, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.send_rc_control(0, 0, 0, 0))
ml.bind('<Button-1>', move_left)
ml.place(x=1010, y=510)

ff = Button(window, image=icon4, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.flip_forward())
ff.place(x=500, y=400)

bf = Button(window, image=icon5, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.flip_back())
bf.place(x=580, y=400)

lf = Button(window, image=icon6, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.flip_left())
lf.place(x=660, y=400)

rf = Button(window, image=icon7, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.flip_right())
rf.place(x=740, y=400)

raf = Button(window, image=icon8, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.send_rc_control(0, 0, 0, 0))
raf.bind('<Button-1>', move_right_and_forward)
raf.place(x=200, y=440)

laf = Button(window, image=icon9, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.send_rc_control(0, 0, 0, 0))
laf.bind('<Button-1>', move_left_and_forward)
laf.place(x=45, y=440)

rab = Button(window, image=icon10, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.send_rc_control(0, 0, 0, 0))
rab.bind('<Button-1>', move_right_and_back)
rab.place(x=200, y=590)

lab = Button(window, image=icon11, bg=color, activebackground="green", width=50, height=50, command=lambda: drone.send_rc_control(0, 0, 0, 0))
lab.bind('<Button-1>', move_left_and_back)
lab.place(x=45, y=590)

tp = Button(window, image=icon12, bg=color, activebackground="green", width=50, height=50, command=take_photo)
tp.place(x=1100, y=60)

cn = Button(window, text="Connect", activebackground="green", bg="blue", width=12, height=3, command=connect)
cn.place(x=1100, y=150)

sp = Scale(window, label="Speed", from_=10, to=100, orient=HORIZONTAL, length=300, tickinterval=10, command=speed_control)
sp.set(50)
sp.bind('<Button-1>', speed_control)
sp.place(x=500, y=520)

ed = Label(window)
ed.place(x=400, y=40)

hg = Label(window, font=("Helvetica", 12))
hg.place(x=300, y=10)

bt = Label(window, font=("Helvetica", 12))
bt.place(x=500, y=10)

tm = Label(window, font=("Helvetica", 12))
tm.place(x=700, y=10)


def light_theme_state():
    window.config(background="white")


light_theme = Button(window, text="Light Theme", command=light_theme_state)
light_theme.place(x=20, y=160)


window.mainloop()
