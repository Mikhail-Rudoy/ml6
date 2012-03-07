import java.io.*;
import java.util.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.awt.image.*;
import javax.imageio.*;

public class Canvas extends JPanel {

    public static final int XRES = 500;
    public static final int YRES = 500;

    private EdgeMatrix edges;
    private BufferedImage bi;
    private EdgeMatrix tmpline;
    private Color c;
    boolean drawing=false;    
    
    public Canvas() {
	edges = new EdgeMatrix();
	tmpline = new EdgeMatrix(2);	
	c = Color.blue;
    }
    

    /*======== public void setDrawing() ==========
      Inputs:  int x0
               int y0
	       int x1
	       int y1 
      Returns: 
      sets drawing to true and adds a line to the tmpLine EdgeMatrix

      ====================*/
    public void setDrawing(int x0, int y0, int x1, int y1)
    {
	drawing = true;
	tmpline.clear();
	tmpline.addEdge(x0, y0, 0, x1, y1, 0);
	this.update(this.getGraphics());
    }

    
    public void stopDrawing()
    {
	drawing=false;
    }
  
    public BufferedImage getBufferedImage()
    {
	return bi;
    }

    public Dimension getPreferredSize()
    {
	return new Dimension(XRES, YRES);
    }


    /*======== public void addLine() ==========
      Inputs:  int x0
               int y0
	       int z0
	       int x1
	       int y1
	       int z1 
      Returns: 
      Adds the specified line to the edges EdgeMatrix
      ====================*/
    public void addLine(int x0, int y0, int z0, int x1, int y1, int z1)
    {
	edges.addEdge(x0, y0, z0, x1, y1, z1);
    }


    /*======== public void addPoint() ==========
      Inputs:  int x0
         int y0
         int z0 
      Returns: 
      add a single point to the edges EdgeMatrix
      ====================*/
    public void addPoint(int x0, int y0, int z0)
    {
	edges.addPoint(x0, y0, z0);
    }


    public void clearTmp()
    {
	tmpline.clear();
    }

    /*======== public void clearPoints()) ==========
      Inputs:   
      Returns: 

      Clear the edge matrix and redraw the canvas

      03/05/12 11:17:10
      jdyrlandweaver
      ====================*/
    public void clearPoints()
    {
	edges.clear();
	this.update(this.getGraphics());
    }


    /*======== public void paintComponent() ==========
      Inputs:  Graphics g 
      Returns: 
      draws the edges stored in tmpLine or edges to the canvas
      you must update this to work with matricies instead of an 
      array of Line objects   
      ====================*/
    public void paintComponent(Graphics g)
    {

	super.paintComponent(g);
	bi = (BufferedImage)this.createImage(XRES, YRES);
	Graphics2D g2 = bi.createGraphics();

	if (drawing)
	{
	    g2.setColor(c.red);
	    g2.drawLine((int)tmpline.getX(0), (int)tmpline.getY(0), (int)tmpline.getX(1), (int)tmpline.getY(1));
	}
	
	g2.setColor(c);
	
	for(int i = 0; i < edges.getLastCol() / 2; i++)
	{
	    g2.drawLine((int)edges.getX(2*i), (int)edges.getY(2*i), (int)edges.getX(2*i+1), (int)edges.getY(2*i+1));
	}

	((Graphics2D)g).drawImage(bi,null,0,0);
    }
}
