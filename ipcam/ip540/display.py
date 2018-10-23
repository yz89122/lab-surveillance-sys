import urllib.request
import base64
import cv2
import numpy as np
import sys


def main():
    try:
        host = sys.argv[1]
    except:
        print('Usage: python3 ', sys.argv[0], ' <hostname> [port] [s1/s2]')
        exit(1)
    port = str(554)
    stream = 's1'
    try:
        port = sys.argv[2]
        stream = sys.argv[3]
        if stream != 's1' or stream != 's2':
            print('option stream should be s1 or s2')
    except:
        pass

    video_capture = cv2.VideoCapture('rtsp://' + host + ':' + port + '/medias1')

    if not video_capture.isOpened():
        video_capture.open()
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        cv2.imshow('img', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
