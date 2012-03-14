import java.awt.Color;
import java.util.Random;

public class main
{
    public static void main(String[] args)
    {
	screen s = new screen();
	/*for(int x = 0; x < 600; x++)
	{
	    for(int y = 0; y < 600; y++)
	    {
		int r = (int)((Math.sqrt(Math.pow(x - 300, 2) + Math.pow(y - 300, 2)))/1.655);
		int g = 2 * 256-(int)((Math.sqrt(Math.pow(x - 100, 2) + Math.pow(y - 100, 2)) + Math.sqrt(Math.pow(x - 500, 2) + Math.pow(y - 500, 2)))/2.0);
		int b = (int)((Math.sqrt(Math.pow(x - 100, 2) + Math.pow(y - 500, 2)) + Math.sqrt(Math.pow(x - 500, 2) + Math.pow(y - 100, 2)))/2.0);
		s.setPixel(x, y, new Color(r%256, g%256, b%256));
	    }
	}*/
	Random R = new Random();
	for(int x0 = 50; x0 < 600; x0 = x0 + 100)
	{
	    for(int y0 = 50; y0 < 600; y0 = y0 + 100)
	    {
		for(int x1 = 50; x1 < 600; x1 = x1 + 100)
		{
		    for(int y1 = 50; y1 < 600; y1 = y1 + 100)
		    {
			int r = R.nextInt(256);
			int g = R.nextInt(256);
			int b = R.nextInt(256);
			s.drawLine(x0, y0, x1, y1, new Color(r, g, b));
		    }
		}   
	    }   
	}
	s.saveScreen("pic.ppm");
    }
}