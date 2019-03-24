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

    CLASS_PERSON = 1

    def __init__(self, **kwargs):
        self.err = kwargs['err']
        self.t_color = kwargs['t_color']
        self.color = kwargs['color']
        self.threshold = kwargs['threshold']
        self.width = kwargs['width'] // 2
        self.height = kwargs['height'] // 2
        self.lose = math.sqrt((self.width * self.width + self.height *self.height))
        self.path_to_ckpt = kwargs['model_path']
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
        result = list()
        for i, box in enumerate(boxes):
            if classes[i] == Detector.CLASS_PERSON and scores[i] > self.threshold:
                result.append(box)
        return result

    def getAXY(self, img, boxes):
        lose = self.lose
        x_out = self.width
        y_out = self.height
        mark = -1
        for i, box in enumerate(boxes):
            x = (box[1] + box[3]) // 2
            y = (box[0] + box[2]) // 2
            l = math.sqrt( (x - self.width)*(x - self.width) + (y - self.height)*(y - self.height) )
            if lose > l:
                mark = i
                lose = l
                x_out = x
                y_out = y
        if mark != -1 and self.draw_mid == True:
            box = boxes[mark]
            y1, x1, y2, x2 = box
            cv2.rectangle(img, (x1, y1), (x2, y2), self.t_color, 2)
        return x_out, y_out

    def direction(self, x, y):
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
            elif ver == 2:dir = 1
        return dir

    def detect(self,image):
        return DetectedResult(image, self.getBox(image), self.color)
        # x1,y1,x2,y2 = self.getBox(img)
        # x,y = self.getAXY(img,x1,y1,x2,y2)
        # dir = self.direction(x,y)
        # if output == 'box': return x1,y1,x2,y2
        # elif output == 'xy': return x,y
        # elif output == 'dir': return dir

    def close(self):
        self.sess.close()
        self.default_graph.close()


class DetectedResult:
    def __init__(self, image, boxes, color):
        self.image = image
        self.boxes = boxes
        self.color = color
        self.drawn_image = None

    def draw_boxes(self):
        if self.drawn_image is None:
            self.drawn_image = self.image.copy()
            for box in self.boxes:
                cv2.rectangle(self.drawn_image, (box[1], box[0]), (box[3],box[2]), self.color, 2)
        return self.drawn_image

    def getBoxes(self):
        return self.boxes

    def getImage(self):
        return self.image

    def getAXY(self):
        pass

    def direction(self):
        pass
