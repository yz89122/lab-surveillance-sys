package tousatsu.cam;

import java.io.IOException;

public interface IWebCamController {
    public void moveUp() throws IOException;
    public void moveDown() throws IOException;
    public void moveLeft() throws IOException;
    public void moveRight() throws IOException;
    public void setSpeed(int speed) throws IOException;
}
