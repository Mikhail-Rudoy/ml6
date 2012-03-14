import java.awt.Color;
import java.lang.IllegalArgumentException;
import java.io.PrintWriter;
import java.io.FileWriter;
import java.io.IOException;

public class screen
{
    private Color[][] arr;//r, c format
    public static int defaultW = 600;
    public static int defaultH = 600;
    
    public screen(int w, int h)
    {
	arr = new Color[h][w];
	for(int r = 0; r < h; r++)
	{
	    for(int c = 0; c < w; c++)
	    {
		arr[r][c] = new Color(0, 0, 0);
	    }
	}
    }
    public screen()
    {
	this(defaultW, defaultH);
    }
    
    public Color getPixel(int x, int y)
    {
	if(x >= 0 && x < arr[0].length && y >= 0 && y < arr.length)
	{
	    return arr[y][x];
	}
	throw new IllegalArgumentException();
    }
    
    public void setPixel(int x, int y, Color c)
    {
	if(x >= 0 && x < arr[0].length && y >= 0 && y < arr.length)
	{
	    arr[y][x] = c;
	}
	else
	{
	    throw new IllegalArgumentException();
	}
    }
    
    public void saveScreen(String filename)
    {
	PrintWriter pw = null;
	try
	{
	    pw = new PrintWriter(new FileWriter(filename));
	    pw.print("P3 \n");
	    pw.print(arr.length);
	    pw.print(" ");
	    pw.print(arr[0].length);
	    pw.print(" 256 \n");
	    for(int r = 0; r < arr.length; r++)
	    {
		for(int c = 0; c < arr[0].length; c++)
		{
		    pw.print(arr[r][c].getRed());
		    pw.print(" ");
		    pw.print(arr[r][c].getGreen());
		    pw.print(" ");
		    pw.print(arr[r][c].getBlue());
		    pw.print(" ");
		}
		pw.print("\n");
	    }
	    pw.flush();
	}
	catch(IOException e)
	{ }
	finally
	{
	    if(pw != null)
	    {
		pw.close();
	    }
	}
    }
}