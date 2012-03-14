import java.awt.Color;

public class main
{
    public static void main(String[] args)
    {
	screen s = new screen();
	for(int x = 0; x < 600; x++)
	{
	    for(int y = 0; y < 600; y++)
	    {
		int r = (int)Math.sqrt(Math.pow(x - 300, 2) + Math.pow(y - 300, 2));
		int g = (int)(Math.sqrt(Math.pow(x - 100, 2) + Math.pow(y - 100, 2)) + Math.sqrt(Math.pow(x - 500, 2) + Math.pow(y - 500, 2)));
		int b = (int)(Math.sqrt(Math.pow(x - 100, 2) + Math.pow(y - 500, 2)) + Math.sqrt(Math.pow(x - 500, 2) + Math.pow(y - 100, 2)));
		s.setPixel(x, y, new Color(r%256, g%256, b%256));
	    }
	}
	s.saveScreen("pic.ppm");
    }
}