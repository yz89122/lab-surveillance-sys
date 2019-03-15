import cv2

class StreamingFetcher:
    def __init__(self, streaming_address):
        self.url = 'rtsp://' + streaming_address + '/medias1'
        self.frame = None
        self.__video_capture = cv2.VideoCapture(self.url)

    def get_newest_frame(self):
        return self.frame
    
    def start_capturing(self):
        if not self.__video_capture.isOpened():
            self.__video_capture.open(self.url)
        while self.__video_capture.isOpened():
            _, self.frame = self.__video_capture.read()
