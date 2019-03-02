package tousatsu.cam;

import java.io.IOException;

public class IP540Example {

    public static void main(String[] args) throws IOException {
        IWebCamController cam = new IP540(false, "1.161.133.207", "admin", "admin");
        cam.setSpeed(10);
        cam.moveUp();
        cam.moveDown();
        cam.moveLeft();
        cam.moveRight();

        castToIP540(cam);
    }

    private static void castToIP540(IWebCamController cam) throws IOException {
        IP540 ip540 = (IP540) cam;
        ip540.move(IP540.LEFT_DOWN);
        ip540.move(IP540.LEFT_UP);
        ip540.move(IP540.RIGHT_DOWN);
        ip540.move(IP540.RIGHT_UP);
        ip540.move(IP540.HOME);
    }

}
