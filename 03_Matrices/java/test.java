import java.io.*;
import java.util.*;

import java.awt.*;

public class test {
    public static void main(String[] args) {

	Frame f = new Frame();
	Color c = new Color(255, 0, 255);

	f.drawLine(0, 0, Frame.XRES, Frame.YRES, c);
	f.drawLine(0, 200, Frame.XRES, 200, c);
	f.save("pic.png");
    }
}
