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
    
    public void drawLine(int x0, int y0, int x1, int y1, Color c)
    {
	int x;
	int y;
	int d = 0;
	int dx = x1 - x0;
	int dy = y1 - y0;
	
	if(dx == 0)//vertical line
	{
	    for(y = (dy > 0) ? y0 : y1; y <= y1 || y <= y0; y++)
	    {
		setPixel(x0, y, c);
	    }
	}
	else if(dy == 0)//horizontal line
	{
	    for(x = (dx > 0) ? x0 : x1; x <= x1 || x <= x0; x++)
	    {
		setPixel(x, y0, c);
	    }
	}
	else if(dy == dx)//diagonal top-left/bottom-right
	{
	    for(x = (dx > 0) ? x0 : x1, y = (dy > 0) ? y0 : y1; x <= x1 || x <= x0; x++, y++)
	    {
		setPixel(x, y, c);
	    }
	}
	else if(dy + dx == 0)//diagonal top-right/bottom-left
	{
	    for(x = (dx > 0) ? x0 : x1, y = (dy < 0) ? y0 : y1; x <= x1 || x <= x0; x++, y--)
	    {
		setPixel(x, y, c);
	    }
	}
	else
	{
	    if(dx + dy < 0)//octants 4-7
	    {
		dx = -dx;
		dy = -dy;
		
		x = x0;
		y = y0;
		
		x0 = x1;
		y0 = y1;
		
		x1 = x;
		y1 = y;
	    }
	    
	    if(dy < 0)//octant 8
	    {
		for(x = x0, y = y0; x <= x1; x++)
		{
		    setPixel(x, y, c);
		    if(d > 0)
		    {
			y--;
			d = d - dx;
		    }
		    d = d - dy;
		}
	    }
	    else if(dx < 0)//octant 3
	    {
		for(y = y0, x = x0; y <= y1; y++)
		{
		    setPixel(x, y, c);
		    if(d > 0)
		    {
			x--;
			d = d - dy;
		    }
		    d = d - dx;
		}
	    }
	    else if(dx > dy)//octant 1
	    {
		for(x = x0, y = y0; x <= x1; x++)
		{
		    setPixel(x, y, c);
		    if(d < 0)
		    {
			y++;
			d = d + dx;
		    }
		    d = d - dy;
		}
	    }
	    else//octant 2
	    {
		for(x = x0, y = y0; y <= y1; y++)
		{
		    setPixel(x, y, c);
		    if(d < 0)
		    {
			x++;
			d = d + dy;
		    }
		    d = d - dx;
		}
	    }
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
	{
	    System.out.println(e);
	}
	finally
	{
	    if(pw != null)
	    {
		pw.close();
	    }
	}
    }
}