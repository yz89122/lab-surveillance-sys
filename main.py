from time import sleep

from config import ConfigReader
from ipcam import loader
from context import Context
from detector import Detector
from daemon import Daemon, ClockedRunner
from control_logic import Controller


def start_image_fetchers_daemons(cameras):
    for camera in cameras.values():
        camera['image_fetcher_daemon'].start()


def detect_loop(context: Context, camera, detector: Detector):
    frame = camera['image_fetcher'].get_newest_frame()
    x1,y1,x2,y2 = detector.getBox(frame)
    result = [x1,y1,x2,y2]
    context.set_last_processed(camera['key'], frame, result)


def main():
    config = ConfigReader('config.json')
    cameras = dict()

    for index, camera in enumerate(config.get_config()['cameras']):
        camera_controller_configurer, camera_image_fetcher_configurer = loader.load(camera['model'])

        controller = camera_controller_configurer(**camera)
        image_fetcher = camera_image_fetcher_configurer(**camera)
        daemon = Daemon(target=image_fetcher.start_capturing)

        cameras[index] = {
            'key': index,
            'config': camera,
            'controller': controller,
            'image_fetcher': image_fetcher,
            'image_fetcher_daemon': daemon,
        }

    start_image_fetchers_daemons(cameras)
    context = Context(cameras)

    model_path = './model/frozen_inference_graph.pb'
    width = 1280
    height = 720
    threshold = 0.7

    for camera in cameras.values():
        detector = Detector(model_path,width,height,30,threshold,(255,0,0),(255,255,48),True,True)
        runner = ClockedRunner(detect_loop, camera['config']['detect_rate'], kwargs={
            'context': context,
            'camera': camera,
            'detector': detector
        })
        runner.start()

    main_controller = Controller()
    while True:
        main_controller.loop(context)
        sleep(1 / config.get_config()['main_loop_per_second'])


if __name__ == '__main__':
    main()
