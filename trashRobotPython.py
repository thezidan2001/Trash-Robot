import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import serial

# Menghubungkan dengan port arduino
arduino = serial.Serial(port='COM6', baudrate=115200)

# Mendefinisikan kamera yang digunakan
cap = cv2.VideoCapture(1)
# Mendefinisikan berapa banyak tangan yang ingin dideteksi
detector = HandDetector(maxHands=1)
# classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

# Batas tepi
offset = 20
# Ukuran gambar untuk window
imgSize = 500

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    # Exception untuk mengeksekusi hanya jika tidak terdapat error
    try:
        # Kondisi jika tangan terdeteksi
        if hands:
            hand = hands[0]
            # Membuat kotak penanda
            x, y, w, h = hand['bbox']
            
            # Mengcrop tangan
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            # Kondisi untuk membuat kotak penanda yang adaptif terhadap panjang dan lebar tangan
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                # prediction, index = classifier.getPrediction(imgWhite, draw=False)
                # print(prediction, index)

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                # prediction, index = classifier.getPrediction(imgWhite, draw=False)

            # Mendefinisikan jari yang naik maupun yang turun
            fingers=detector.fingersUp(hand)
            print(fingers)

            label=""

            # Kondisi label yang akan dicetak
            if(fingers==[1, 1, 1, 1, 1]):
                label="Move"
            elif(fingers==[0, 1, 1, 0, 0]):
                label="Open"
            elif(fingers==[1, 1, 0, 0, 1]):
                label="Back"
            elif(fingers==[0, 0, 0, 0, 0]):
                label="Stop"
            else:
                label="Error"

            # Kotak background tulisan
            cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                        (x - offset+200, y - offset-50+50), (255, 0, 255), cv2.FILLED)
            # Tulisan yang akan dicetak
            cv2.putText(imgOutput, label, (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            # Kotak yang mengelilingi tangan
            cv2.rectangle(imgOutput, (x-offset, y-offset),
                        (x + w+offset, y + h+offset), (255, 0, 255), 4)

            # print(labels[index])
            # Kondisi yang akan dikirim ke arduino
            if(label=="Move"):
                arduino.write(b'1')
            elif(label=="Open"):
                arduino.write(b'2')
            elif(label=="Back"):
                arduino.write(b'3')
            elif(label=="Error"):
                arduino.write(b'4')
            elif(label=="Stop"):
                arduino.write(b'4')

        # Kondisi jika tangan tidak terdeteksi
        elif not hands:
            arduino.write(b'4')
            
        # cv2.imshow("ImageCrop", imgCrop)
        # cv2.imshow("ImageWhite", imgWhite)

        cv2.imshow("Image", imgOutput)

    # Jika kode error, maka akan diberi tahu detail dari error
    except Exception as e:
        print(f'exc: {e}')
        pass
    key = cv2.waitKey(1)
    # Window akan ditutup jika menekan key "q"
    if key == ord('q'):
        break

# Mengclose semua window
cap.release()
cv2.destroyAllWindows()

    