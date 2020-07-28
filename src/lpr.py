from object_detect import *
from plate_detection import *
from object_track import *
from automatic_email import *

def vid_detect(vid = None):
    cap=None
    if vid == None :
        cap=cv2.VideoCapture(0)
    else :
        cap=cv2.VideoCapture(vid)
    frame_no=0
    multi_tracker = Tracker()
    
    while True:
        ret , img = cap.read()
        img1 = img.copy()
        objects = extract_object(img = img)
        
        if len(objects) > 0 : 
            
            if frame_no==0:
                multi_tracker.new_boxes(img, objects)
            else :
                multi_tracker.update_objects(img, objects)
            frame_no += 1
        
            for i,object in enumerate(multi_tracker.objects):
                box  = object.box            
                if box is not None and 0 not in tuple(map(int, box)):
                    box = np.array(box , dtype = 'int64')
                    object.image = img1[box[1]:box[1]+box[3],box[0]:box[0]+box[2]]
                    try:
                        #cv2.imshow(str(object.name),object.image)
                        text = plate_detection(None , img = object.image)
                        object.update_text(text)
                    except:
                        continue
                    #print(object.name , object.text)
                    # if object.foul :(foul for detection at red light )
                    # if object.entered :( entered for some parking facility ))
                    #     email_vehicle_user(object.text)
        
        cv2.imshow("lpr" , img)
        
        if cv2.waitKey(33) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def pic_detect(path):
    
    img = cv2.imread("images/licensed_car10.jpg")
    cv2.imshow("img",img)
    objects = extract_object(path = path)
    
    for i,object in enumerate(objects):
        
        image = img[int(object[1]):int(object[1] + object[3]) , int(object[0]):int(object[0]+object[2])]
        cv2.imshow(str(i) , image)
        text = plate_detection(None , img = image)
        
        print(str(i+1) , text)
        # if ob.foul :(foul for detection at red light )
        # if ob.entered :( entered for some parking facility ))
        #     email_vehicle_user(ob.text)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def detect(mode = "video" , path=None):
    if mode == 'pic':
        if path == None:
            print("Wrong Path")
        else :
            pic_detect(path)
    if mode == 'video':
        if path == None:
            vid_detect(None)
        else :
            vid_detect(path)

#detect("video" , "Images_and_videos/Videos/Vehicles.mp4")
# detect("pic" , "Images_and_videos/Images/licensed_car10.jpg")