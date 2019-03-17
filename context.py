from collections import defaultdict

class Context:
    def __init__(self, cameras):
        self.cameras = cameras
        self.data = defaultdict(lambda: None)
        self.last_processed = defaultdict(lambda: (None, None))

    def get_cameras(self):
        return self.cameras

    def get_num_of_cameras(self):
        return len(self.cameras)

    def get_camera_config(self, key):
        return self.cameras[key]['config']

    def get_controller(self, key):
        return self.cameras[key]['controller']

    def get_image(self, key):
        return self.cameras[key]['image_fetcher'].get_newest_frame()

    def set_last_processed(self, key, frame, result):
        self.last_processed[key] = (frame, result)

    def get_last_processed(self, key):
        return self.last_processed[key]
    
    def set_value(self, key, value):
        self.data[key] = value

    def get_value(self, key):
        return self.data[key]
