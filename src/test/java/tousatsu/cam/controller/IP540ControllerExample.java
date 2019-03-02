package tousatsu.cam.controller;

import java.io.IOException;

public class IP540ControllerExample {

    public static void main(String[] args) throws IOException {
        IWebCamController cam = new IP540Controller(false, "1.161.133.207", "admin", "admin");
        cam.setSpeed(10);
        cam.moveUp();
        cam.moveDown();
        cam.moveLeft();
        cam.moveRight();

        castToIP540(cam);
    }

    private static void castToIP540(IWebCamController cam) throws IOException {
        IP540Controller ip540 = (IP540Controller) cam;
        ip540.move(IP540Controller.LEFT_DOWN);
        ip540.move(IP540Controller.LEFT_UP);
        ip540.move(IP540Controller.RIGHT_DOWN);
        ip540.move(IP540Controller.RIGHT_UP);
        ip540.move(IP540Controller.HOME);
    }

}
