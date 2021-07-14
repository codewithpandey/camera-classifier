from sklearn.svm import LinearSVC
import numpy as np
import cv2 as cv
import PIL
# from tensorflow.keras import layers, models

class Model:

    def __init__(self):
        self.model = LinearSVC()

    def trainModel(self, counters):
        img_list = np.array([])
        class_list = np.array([])

        for i in range(1, counters[0]):
            img = cv.imread(f'class1/frame{i}.jpg')[:,:,0]
            img = img.reshape(150, 113) # product of your resolutions
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 1)
        
        for j in range(1, counters[0]):
            img = cv.imread(f'class2/frame{j}.jpg')[:,:,0]
            img = img.reshape(150, 113) # product of your resolutions
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 2)

        img_list = img_list.reshape(counters[0] - 1 + counters[1] - 1, 16950)
        self.model.fit(img_list, class_list)
        print("Model Successfully Trained")

    def predict(self, frame):
        frame = frame[1]
        cv.imwrite('frame.jpg', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open('frame.jpg')
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save('frame.jpg')

        img = cv.imread('frame.jpg')[:,:,0]
        img = img.reshape(16950)
        prediction = self.model.predict([img])

        return prediction[0]