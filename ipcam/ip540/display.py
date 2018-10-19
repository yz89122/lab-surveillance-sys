import urllib.request
import base64
import cv2
import numpy as np
import sys


def main():
    try:
        host = sys.argv[1]
        port = str(554)
    except:
        print('Usage: python3 ', sys.argv[0], ' <hostname> [port]')
        exit(1)
    try:
        port = sys.argv[2]
    except:
        pass

    video_capture = cv2.VideoCapture('rtsp://' + host + ':' + port + '/medias2')
    print(video_capture.isOpened())

    if video_capture.isOpened():
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            cv2.imshow('img', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    main()
