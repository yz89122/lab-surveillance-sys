import cv2

class StreamingFetcher:
    def __init__(self, streaming_address):
        self.url = 'rtsp://' + streaming_address + '/medias1'
        self.frame = None
        self.updated = False

    def is_frame_updated(self):
        return self.updated

    def get_newest_frame(self):
        self.updated = False
        return self.frame
    
    def start_capturing(self):
        self.__video_capture = cv2.VideoCapture(self.url)
        while True:
            if self.__video_capture.isOpened():
                retval, frame = self.__video_capture.read()
                if retval:
                    self.frame = frame
                    self.updated = True
            else:
                self.__video_capture.open(self.url)
