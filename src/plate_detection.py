import cv2
import numpy as np
import pytesseract
import math
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"


config = ('-l eng --oem 1 --psm 6')

def distance(p1 , p2):
    dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)
    return dist

def getcoord(cnt):
    approx = cv2.approxPolyDP(cnt, (0.02) * cv2.arcLength(cnt, True), True)
    n=approx.ravel()
    x=[]
    y=[]
    plus=[]
    minus=[]
    for i in range(len(n)):
        if i%2==0 :
            x.append(n[i])
            y.append(n[i+1])
            plus.append(x[int(i/2)] + y[int(i/2)])
            minus.append(y[int(i/2)] - x[int(i/2)])
    br=(x[plus.index(max(plus))] , y[plus.index(max(plus))])
    tl=(x[plus.index(min(plus))] , y[plus.index(min(plus))])
    bl=(x[minus.index(max(minus))] , y[minus.index(max(minus))])
    tr=(x[minus.index(min(minus))] , y[minus.index(min(minus))])
    return tl,tr,br,bl

def ptrans(img,tl,tr,br,bl):
    
    src = np.array([tl, tr, br, bl], dtype='float32')
    side = max([ distance(tl, tr), 
     distance(tr, br),
     distance(br, bl), 
     distance(bl, tl) ])
    dst = np.array([[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]], dtype='float32')
    m = cv2.getPerspectiveTransform(src, dst)
    plate = cv2.warpPerspective(img, m, (int(side), int(side)))
    plate=cv2.resize(plate , (300,100) , interpolation = cv2.INTER_AREA)
    #cv2.imshow('plate',plate)
    return plate

def plate_detection(path,img=None):
    if img is None:
        img=cv2.imread(path)
    
    cv2.imshow('orig',img)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray=cv2.bilateralFilter(gray,11,17,17)
    edged=cv2.Canny(gray,50,50)

    cnts, new=cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    img1=img.copy()
    #cv2.drawContours(img1,cnts,-1,(0,255,0),3)

    cnts=sorted(cnts, key =cv2.contourArea,reverse=True)[:50]

    img2=img.copy()
    #cv2.drawContours(img2,cnts,-1,(0,255,0),3)
    #cv2.imshow("reduced contours",img2)

    plate=None
    for c in cnts:
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,(0.02)*peri,True)
        if len(approx)==4:
            tl,tr,br,bl = getcoord(c)
            plate = ptrans(img,tl,tr,br,bl)
            cv2.imshow('plate',plate)
            break

    if plate !=[] and plate is not None:
        text = pytesseract.image_to_string(plate, config=config)
        print(text)

    return text


plate_detection("objects/0_licensed_car10.jpg")
cv2.waitKey(0)

# plate_detection("objects/0_licensed_car15.jpg")
# cv2.waitKey(0)
# plate_detection("objects/0_licensed_car25.jpg")
# cv2.waitKey(0)
# plate_detection("objects/0_licensed_car86.jpg")
# cv2.waitKey(0)
# plate_detection("objects/0_licensed_car91.jpg")
# cv2.waitKey(0)
# plate_detection("objects/0_licensed_car139.jpg")
# cv2.waitKey(0)
# plate_detection("objects/0_licensed_car142.jpg")
# cv2.waitKey(0)
# plate_detection("objects/1_licensed_car75.jpg")
        
cv2.waitKey(0)
cv2.destroyAllWindows()