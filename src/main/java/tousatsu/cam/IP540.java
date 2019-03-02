package tousatsu.cam;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;

public class IP540 implements IWebCamController {

    public IP540(boolean isHttps, String ip, String username, String password) {
        this.isHttps = isHttps;
        this.ip = ip;
        this.username = username;
        this.password = password;
    }

    private boolean isHttps;
    private String ip;
    private String username;
    private String password;

    public static String UP = "up";
    public static String LEFT_UP = "leftup";
    public static String LEFT = "left";
    public static String LEFT_DOWN = "leftdown";
    public static String DOWN = "down";
    public static String RIGHT_DOWN = "rightdown";
    public static String RIGHT = "right";
    public static String RIGHT_UP = "rightup";
    public static String HOME = "home";

    private String moveUrl(String direction) {
        return String.format("http%s://%s/cgi-bin/view/cammove.cgi?move=%s",
                this.isHttps ? "s" : "", this.ip, direction);
    }

    private String setSpeedUrl(int speed) {
        return String.format("http%s://%s/cgi-bin/view/ptzspeed.cgi?speed=%d",
                this.isHttps ? "s" : "", this.ip, speed);
    }

    private void sendRequest(String url) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
        connection.setRequestMethod("GET");
        connection.setRequestProperty("Authorization", "Basic " + Base64.getEncoder()
                .encodeToString((this.username  + ":" + this.password).getBytes()));
        int code = connection.getResponseCode();
        connection.disconnect();
        if (code != 200) throw new IOException("response code not equal to 200");
    }

    public void setSpeed(int speed) throws IOException {
        this.sendRequest(this.setSpeedUrl(speed));
    }

    public void move(String direction) throws IOException {
        this.sendRequest(this.moveUrl(direction));
    }

    @Override
    public void moveUp() throws IOException {
        this.move(UP);
    }

    @Override
    public void moveDown() throws IOException {
        this.move(DOWN);
    }

    @Override
    public void moveLeft() throws IOException {
        this.move(LEFT);
    }

    @Override
    public void moveRight() throws IOException {
        this.move(RIGHT);
    }

}
