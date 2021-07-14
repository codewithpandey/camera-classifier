import tkinter as tk
from tkinter import simpledialog
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
import camera
import model
import sys

sys.setrecursionlimit(3000)

class App:

    def __init__(self, window = tk.Tk(), window_title = "Recognizer"):

        self.window = window
        self.window_title = window_title

        self.counters = [1, 1]

        self.model = model.Model()

        self.autoPredict = False

        self.camera = camera.Camera()

        self.startGUI()

        self.delay = 15
        self.update()

        self.window.attributes('-topmost', True)
        self.window.mainloop()

    def startGUI(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.btn_toggleauto = tk.Button(self.window, text="Auto Prediction", width=50, command=self.autoPredictToggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.classname_one = simpledialog.askstring("Classname One", "Enter the name of the first class: ", parent=self.window)
        self.classname_two = simpledialog.askstring("Classname Two", "Enter the name of the second class: ", parent=self.window)

        self.btn_class_one = tk.Button(self.window, text=self.classname_one, width=50, command=lambda: self.saveForClass(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text=self.classname_two, width=50, command=lambda: self.saveForClass(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Train Model", width=50, command=lambda: self.model.trainModel(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window, text="Predict", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.class_label = tk.Label(self.window, text="CLASS")
        self.class_label.config(font=("Calibri", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)


    def autoPredictToggle(self):
        self.autoPredict = not self.autoPredict

    def saveForClass(self, class_num):
        ret, frame = self.camera.getFrame()
        if not os.path.exists('class1'):
            os.mkdir('class1')
        if not os.path.exists('class2'):
            os.mkdir('class2')

        cv.imwrite(f'class{class_num}/frame{self.counters[class_num - 1]}.jpg', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open(f'class{class_num}/frame{self.counters[class_num - 1]}.jpg')
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f'class{class_num}/frame{self.counters[class_num - 1]}.jpg')

        self.counters[class_num - 1] += 1

    
    def reset(self):
        for directory in ['class1', 'class2']:
            for image in os.listdir(directory):
                file_path = os.path.join(directory, image)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        self.counters = [1, 1]
        self.model = model.Model()
        self.class_label.config(text="CLASS")


    def update(self):
        if self.autoPredict:
            self.predict()
            pass

        ret, frame = self.camera.getFrame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        print("Updating...")
        self.window.after(self.delay, self.update)

    
    def predict(self):            
        frame = self.camera.getFrame()
        prediction = self.model.predict(frame)

        if prediction == 1:
            self.class_label.config(text=self.classname_one)
            return self.classname_one

        if prediction == 2:
            self.class_label.config(text=self.classname_two)
            return self.classname_two

