import cv2
import numpy as np
import os

path = 'Images_to_train'
matcher = cv2.BFMatcher()
images = []
classNames = []
myList = os.listdir(path=path)
orb_detector = cv2.ORB_create(nfeatures=1000)

for cl in myList:
    imgcur = cv2.imread(f'{path}/{cl}',0)
    images.append(imgcur)
    classNames.append(os.path.splitext(cl)[0])
def GetDescriptors(images):
    descl = []
    for image in images:
        kp,desc = orb_detector.detectAndCompute(image,None)
        descl.append(desc)
    return descl
def findId(image,listdes):
    kp2,desc2 = orb_detector.detectAndCompute(image,None)
    finalval = -1
    threshold = 15
    try:
        for des in listdes:
            matches = matcher.knnMatch(des,desc2,k=2)
            good = []
            for m,n in matches:
                if m.distance<0.75*n.distance:
                    good.append([m])
            matchlist = []
            matchlist.append(len(good))
    except:
        pass
    if len(matchlist) !=0:
        if max(matchlist) >= threshold:
            finalval = matchlist.index(max(matchlist))
    return finalval


listdes = GetDescriptors(images)
print(len(listdes))

cam = cv2.VideoCapture(0)

while True:
    ret,img = cam.read()
    imgoriginal = img.copy()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Capture device",img)
    imgid = findId(img,listdes)
    if imgid!=0:
        cv2.putText(imgoriginal,classNames[id],(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0))

    if cv2.waitKey(0) == ord('q'):
        break
