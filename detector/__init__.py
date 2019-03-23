import numpy as np
import tensorflow as tf
import cv2
import time
import math

'''
detector = Detector(model_path,width,height,30,threshold,(255,0,0),(255,255,48),True,False)
Detector(model　路徑,傳入圖片寛,傳入圖片高,轉動誤差值,判斷誤差值(小於１小數　建義0.7),框的顏色(255,0,0),目標框的顏色(255,255,48),是否要框人(True / False),是否要框目標(True / False))
Detector.detect(img,'dir')
Detector.detect(傳入圖片,回傳值)
dir = Detector.detect(img,'dir')  回傳轉動方向
x , y = Detector.detect(img,'xy')  回傳目標xy
x1,y1,x2,y2 = Detector.detect(img,'box') 回傳所有人的x1,y1,x2,y2

'''

class Detector:
    def __init__(self, path_to_ckpt,width,height,err,threshold,color,t_color,draw_box,draw_mid):
        self.err = err
        self.draw_mid = draw_mid
        self.draw_box = draw_box
        self.t_color = t_color
        self.color = color
        self.threshold = threshold
        self.width = width // 2
        self.height = height // 2
        self.lose = math.sqrt((self.width * self.width + self.height *self.height))
        self.path_to_ckpt = path_to_ckpt
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        #start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        #end_time = time.time()

        #print("Elapsed Time:", end_time-start_time)

        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])
    
    def getBox(self,img):
        boxes, scores, classes, num = self.processFrame(img)
        x1 = list()
        x2 = list()
        y1 = list()
        y2 = list()
        for i in range(len(boxes)):
            if classes[i] == 1 and scores[i] > self.threshold:
                box = boxes[i]
                if(self.draw_box == True):
                    cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),self.color,2)
                try:
                    x1.append(box[1])
                    x2.append(box[3])
                    y1.append(box[0])
                    y2.append(box[2])
                except:
                    print("empty")
        return x1,y1,x2,y2

    def getAXY(self,img,x1,y1,x2,y2):
        lose = self.lose
        x = self.width
        y = self.height
        x_out = self.width
        y_out = self.height
        mark = -1
        for i in range(len(x1)):
            x = ((x1[i]+x2[i])//2)
            y = ((y1[i]+y2[i])//2)
            l = math.sqrt( (x - self.width)*(x - self.width) + (y - self.height)*(y - self.height) )
            if lose > l:
                mark = i
                lose = l
                x_out = x
                y_out = y
        if mark != -1 and self.draw_mid == True :
            cv2.rectangle(img,(x1[mark],y1[mark]),(x2[mark],y2[mark]),self.t_color,2)
        return x_out,y_out

    def direction (self,x,y):
        err = self.err
        hor = 5
        ver = 5
        dir = 5
        if abs(x - 640) > err:
            if x > 640 :hor = 6
            else:hor = 4
        if abs(y - 360) > err:
            if y > 360 :ver = 2
            else :ver = 8
        if hor == 5:dir = ver
        elif hor == 6:
            if ver == 5:dir = hor
            elif ver == 8:dir = 9
            elif ver == 2:dir = 3
        elif hor == 4:
            if ver == 5:dir = hor
            elif ver == 8:dir = 7
            elif ver == 2:dir =1
        return dir

    def detect(self,img,output):
        x1,y1,x2,y2 = self.getBox(img)
        x,y = self.getAXY(img,x1,y1,x2,y2)
        dir = self.direction(x,y)
        if output == 'box': return x1,y1,x2,y2
        elif output == 'xy': return x,y
        elif output == 'dir': return dir
        


    def close(self):
        self.sess.close()
        self.default_graph.close()

'''
if __name__ == "__main__":
    name = '1.mp4'
    model_path = './model/frozen_inference_graph.pb'
    width = 1280
    height = 720
    threshold = 0.7
    odapi = Detector(model_path,width,height,30,threshold,(255,0,0),(255,255,48),True,True)
    
    cap = cv2.VideoCapture('./'+name)
    #cap = cv2.VideoCapture('rtsp://1.161.143.19:554/medias1')
    while True:
        r, img = cap.read()
        img = cv2.resize(img, (width, height))
        #x1,y2,x1,y2 = odapi.getBox(img)
        x,y = odapi.detect(img,'xy')
        #dir = odapi.detect(img,'dir')
        print(x,y)
        #print(dir)
        cv2.imshow("preview", img)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

'''