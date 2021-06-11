import tkinter as t
from tkinter import messagebox
from tkinter import ttk
import re
import mysql.connector
import os
import datetime
import time
import cv2
import pickle

root = t.Tk()
root.geometry("800x600")
root.resizable(0, 0)
root.iconbitmap("C:\\Users\\acer\\Documents\\python\\MinorProject\\images\\logo.ico")
root.title("FACE RECOGNITION")
frame1 = t.Frame(root)
frame2 = t.Frame(root)


def raise_frame(frame):
    frame.tkraise()


for f in (frame1, frame2):
    f.grid(row=0, column=1, sticky=t.N + t.W + t.E + t.S)

con = mysql.connector.connect(user="root", password="dee@123", host="localhost")
mycoursor = con.cursor()
mycoursor.execute("use minorproject")

filename1 = t.PhotoImage(file="C:\\Users\\acer\\Documents\\python\\MinorProject\\images\\DSC_0358.png")
backgroung_label = t.Label(root, image=filename1)
backgroung_label.place(x=0, y=0, relwidth=1, relheight=1)
backgroung_label.image = filename1

filename2 = t.PhotoImage(file="C:\\Users\\acer\\Documents\\python\\MinorProject\\images\\DSC_0367.png")
backgroung_label = t.Label(frame1, image=filename2)
backgroung_label.place(x=0, y=0, relwidth=1, relheight=1)
backgroung_label.image = filename2

filename3 = t.PhotoImage(file="C:\\Users\\acer\\Documents\\python\\MinorProject\\images\\DSC_0367.png")
backgroung_label = t.Label(frame2, image=filename3)
backgroung_label.place(x=0, y=0, relwidth=1, relheight=1)
backgroung_label.image = filename3

month = ["select", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]
date = ["select", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18",
        "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
year = ["select", "1995", "1996", "1997", "1998", "1999", "2000", "2001"]
monthno = {"January": "1", "February": "2", "March": "3", "April": "4", "May": "5", "June": "6", "July": "7",
           "August": "8", "September": "9", "October": "10", "November": "11", "December": "12"}


def getdob():
    d = value1.get()
    m = value2.get()
    y = value3.get()
    mno = monthno[m]
    if d == "select" or m == "select" or y == "select":
        t.messagebox.showerror("error", "please select date of birth")
    else:
        dob = y + '-' + mno + '-' + d
        return dob


def email():
    email1 = txtbox4.get()
    if not re.match(r"^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-z0-9-]*$", email1):
        t.messagebox.showerror("error", "incorrect email")
    else:
        return email1


def passwrd():
    password1 = txtbox5.get()
    password2 = txtbox6.get()
    if len(password1) < 6:
        t.messagebox.showerror("error", "weak password")
    else:
        if password2 != password1:
            t.messagebox.showerror("error", "password does not match")
        else:
            return password2


def mobile():
    m = txtbox3.get()
    if len(m) < 10 or len(m) > 10:
        t.messagebox.showerror("error", "mobile number incorrect")
    else:
        return m


def gender():
    g = v.get()
    gen = ""
    if g != "":
        if g == 0:
            gen = "M"
        elif g == 1:
            gen = "F"
    return gen


def signup():
    fname = txtbox1.get()
    lname = txtbox2.get()
    mob = txtbox3.get()
    mail = txtbox4.get()
    dateob = getdob()
    pass1 = txtbox5.get()
    pass2 = txtbox6.get()
    password = passwrd()
    gen = gender()
    if fname == "" or lname == "" or mob == "" or mail == "" or pass1 == "" or pass2 == "":
        t.messagebox.showerror("error", "fields can not be empty")
    else:
        email()
        passwrd()
        mobile()
        mycoursor.execute(
            """insert into signup values('""" + fname + """','""" + lname + """','""" + gen + """','""" + str(
                mob) + """','""" + mail + """','""" + dateob + """','""" + password + """')""")
        con.commit()
        t.messagebox.showinfo("result", "values inserted successfully")
        os.chdir("C:\\Users\\acer\\Documents\\python\\MinorProject\\id_folder\\")
        name = fname + lname
        os.mkdir(name)


def pic_capture():
    cap = cv2.VideoCapture(0)
    seconds_duration = 20
    seconds_between_shots = 1
    fname = txtbox1.get()
    lname = txtbox2.get()
    name = fname + lname
    img_dir = "C:\\Users\\acer\\Documents\\python\\MinorProject\\id_folder\\" + name + "\\"

    now = datetime.datetime.now()
    finish_time = now + datetime.timedelta(seconds=seconds_duration)
    i = 0
    while datetime.datetime.now() < finish_time:
        ret, frame = cap.read()
        filename = f"{img_dir}/{i}.jpg"
        i += 1
        cv2.imwrite(filename, frame)
        time.sleep(seconds_between_shots)

        # cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def clear():
    text1.delete(0, t.END)
    text2.delete(0, t.END)
    text3.configure(state='normal')
    text3.delete(0, t.END)
    text3.configure(state='disable')
    txtbox1.delete(0, t.END)
    txtbox2.delete(0, t.END)
    txtbox3.delete(0, t.END)
    txtbox4.delete(0, t.END)
    txtbox5.delete(0, t.END)
    txtbox6.delete(0, t.END)
    combobox1.set('select')
    combobox2.set('select')
    combobox3.set('select')


def close():
    root.destroy()


def login():
    loginid = text1.get()
    password = text2.get()
    e_id = ""
    if loginid == "" or password == "":
        t.messagebox.showerror("error", "fields can not be empty")
    else:
        mycoursor.execute("select email_id from signup where email_id = %s ", [loginid])
        resultid = mycoursor.fetchone()
        for i in resultid:
            if i == loginid:
                e_id = i
            else:
                t.messagebox.showerror("error", "invalid email id")
        mycoursor.execute("select password from signup where email_id = %s ", [e_id])
        resultpass = mycoursor.fetchone()
        for j in resultpass:
            if j == password:
                t.messagebox.showinfo("welcome", "all details are correct")
            else:
                t.messagebox.showerror("error", "password is incorrect")


face_cascade = cv2.CascadeClassifier('cascades\\data\\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades\\data\\haarcascade_eye.xml')


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}


global result


def recognize():
    global result
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)
            if 4 <= conf <= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            result = name
            color = (255, 0, 0)  # BGR 0-255
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    text3.configure(state='normal')
    text3.insert('end', '' + result + '')
    text3.configure(state='disabled')
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def match():
    a = text1.get()
    mycoursor.execute("select concat(first_name,last_name) As fullname from signup where email_id = %s ", [a])
    resultid = mycoursor.fetchone()
    for i in resultid:
        if i == result:
            t.messagebox.showinfo("welcome", "all details are correct")
        else:
            t.messagebox.showerror("Error", "no match found")


lable1 = t.Label(frame1, text=" Welcome to ABVGIET LOGIN PAGE ", font=("TIMES NEW ROMAN", 28, "bold"))
lable1.grid(row=1, columnspan=5, pady=10, padx=10, sticky=t.E + t.W + t.S + t.N)

lable2 = t.Label(frame1, text=" login id ", font=("Times New Roman", 14, "bold"))
lable2.grid(row=2, column=3, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)
text1 = t.Entry(frame1)
text1.grid(row=2, column=4, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)

lable3 = t.Label(frame1, text=" Password ", font=("Times New Roman", 14, "bold"))
lable3.grid(row=3, column=3, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)
text2 = t.Entry(frame1, show="*")
text2.grid(row=3, column=4, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)

button5 = t.Button(frame1, text=" Face  ", font=("arial", 12, "bold"), command=lambda: recognize())
button5.grid(row=5, column=3, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)
login_image = cv2.imread('C:\\Users\\acer\\Documents\\python\\MinorProject\\images\\DSC_0358.png')
text3 = t.Entry(frame1)
text3.grid(row=5, column=4, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)

lable5 = t.Label(frame1, text="If not a registered user ", font=("Harlow Solid Italic", 14, "italic"))
lable5.grid(row=7, column=3, padx=10, pady=10, sticky=t.S + t.N)

button1 = t.Button(frame1, text=" Check ", command=lambda: login(), font=("arial", 12, "bold"))
button1.grid(row=4, column=4, padx=10, pady=10, sticky=t.S + t.N)

button2 = t.Button(frame1, text=" Cancel", command=lambda: clear(), font=("arial", 12, "bold"))
button2.grid(row=6, column=4, padx=10, pady=10, sticky=t.S + t.N)

button3 = t.Button(frame1, text=" Sign in ", command=lambda: raise_frame(frame2), font=("arial", 12, "bold"))
button3.grid(row=7, column=4, padx=10, pady=10, sticky=t.S + t.N)

button4 = t.Button(frame1, text=" quit ", command=lambda: close(), font=("arial", 12, "bold"))
button4.grid(row=8, column=4, padx=10, pady=10, sticky=t.S + t.N)

button5 = t.Button(frame1, text=" login ", command=lambda: match(), font=("arial", 12, "bold"))
button5.grid(row=6, column=3, padx=10, pady=10, sticky=t.S + t.N)

lable1 = t.Label(frame2, text=" Welcome to Signup PAGE ", font=("Old English Text MT", 28, "bold"))
lable1.grid(row=0, columnspan=7, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)

lable2 = t.Label(frame2, text="First Name", font=("arial", 12,))
lable2.grid(row=1, column=0, padx=10, pady=10)
txtbox1 = t.Entry(frame2)
txtbox1.grid(row=1, column=1, padx=10, pady=10)

lable3 = t.Label(frame2, text="Last name", font=("arial", 12,))
lable3.grid(row=2, column=0)
txtbox2 = t.Entry(frame2)
txtbox2.grid(row=2, column=1, padx=10, pady=10)

lable8 = t.Label(frame2, text="Gender ", font=("arial", 12,))
lable8.grid(row=3, column=0, padx=10, pady=10)

v = t.IntVar()
r1 = t.Radiobutton(frame2, text="Male", variable=v, value=0)
r1.grid(row=3, column=1, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)
r2 = t.Radiobutton(frame2, text="Female", variable=v, value=1)
r2.grid(row=4, column=1, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)

lable4 = t.Label(frame2, text="Contact number ", font=("arial", 12,))
lable4.grid(row=5, column=0, padx=10, pady=10)
txtbox3 = t.Entry(frame2)
txtbox3.grid(row=5, column=1, padx=10, pady=10)

lable5 = t.Label(frame2, text="Email ID", font=("arial", 12,))
lable5.grid(row=6, column=0, padx=10, pady=10)
txtbox4 = t.Entry(frame2)
txtbox4.grid(row=6, column=1, padx=10, pady=10)

lable9 = t.Label(frame2, text="Date Of Birth", font=("arial", 12,))
lable9.grid(row=7, column=0, padx=10, pady=10)
value1 = t.StringVar()
value2 = t.StringVar()
value3 = t.StringVar()
combobox1 = ttk.Combobox(frame2, textvariable=value1, state="readonly")
combobox2 = ttk.Combobox(frame2, textvariable=value2, state="readonly")
combobox3 = ttk.Combobox(frame2, textvariable=value3, state="readonly")
combobox1["values"] = date
combobox2["values"] = month
combobox3["values"] = year
combobox1.current(0)
combobox2.current(0)
combobox3.current(0)
combobox1.grid(column=1, row=7, sticky=t.S + t.E + t.W + t.N, padx=5, pady=5)
combobox2.grid(column=2, row=7, sticky=t.S + t.E + t.W + t.N, padx=5, pady=5)
combobox3.grid(column=3, row=7, sticky=t.S + t.E + t.W + t.N, padx=5, pady=5)
ok = t.Button(frame2, text=" OK ", font=("arial", 12, "bold"), command=lambda: getdob())
ok.grid(row=7, column=4, padx=10, pady=10, sticky=t.E + t.W + t.S + t.N)

lable6 = t.Label(frame2, text="Create Password ", font=("arial", 12,))
lable6.grid(row=8, column=0, padx=10, pady=10)
txtbox5 = t.Entry(frame2, show="*")
txtbox5.grid(row=8, column=1, padx=10, pady=10)

lable7 = t.Label(frame2, text="Confirm Password ", font=("arial", 12,))
lable7.grid(row=9, column=0, padx=10, pady=10)
txtbox6 = t.Entry(frame2, show="*")
txtbox6.grid(row=9, column=1, padx=10, pady=10)

button1 = t.Button(frame2, text=" Create ", command=lambda: signup(), font=("arial", 12, "bold"))
button1.grid(row=10, column=0, padx=10, pady=10, sticky=t.S + t.N)

button2 = t.Button(frame2, text="Cancle  ", command=lambda: raise_frame(frame1), font=("arial", 12, "bold"))
button2.grid(row=11, column=1, padx=10, pady=10, sticky=t.S + t.N)

button3 = t.Button(frame2, text=" Face  ", font=("arial", 12, "bold"), command=lambda: pic_capture())
button3.grid(row=10, column=1, padx=10, pady=10, sticky=t.S + t.N)

button4 = t.Button(frame2, text="Clear  ", command=lambda: clear(), font=("arial", 12, "bold"))
button4.grid(row=11, column=3, padx=10, pady=10, sticky=t.S + t.N)

button5 = t.Button(frame2, text="Sign up ", command=lambda: raise_frame(frame1), font=("arial", 12, "bold"))
button5.grid(row=11, column=0, padx=10, pady=10, sticky=t.S + t.N)

raise_frame(frame1)
root.mainloop()
