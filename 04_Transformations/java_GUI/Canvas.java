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
    public static final Color REG_COLOR = Color.CYAN;
    public static final Color TMP_COLOR = Color.RED;
    
    private EdgeMatrix edges;
    private Matrix transform;
    private BufferedImage bi;
    private EdgeMatrix tmpline;
    private Color c;
    boolean drawing=false; 
    
    public Canvas()
    {
	edges = new EdgeMatrix();
	tmpline = new EdgeMatrix(2);
	transform = new Matrix(4, 4);
	transform.ident();
	c = REG_COLOR;
    }
    
    public void setColor(Color n)
    {
	c = n;
    }
    
    /*======== public void apply()) ==========
      Inputs:
      Returns:

      Apply the master transform matrix to the
      edge matrix
      Reset the master transform matrix after
      Update the drawing area

      03/09/12 09:10:15
      jdyrlandweaver
      ====================*/
    public void apply()
    {
	edges.matrixMult(transform);
	transform.ident();
	this.update(this.getGraphics());
    }
    
    /*======== public void scale() ==========
      Inputs:  double x
               double y
               double z
      Returns:

      Turn the transform matrix into the appropriate
      scale matrix

      Apply the transformation

      03/09/12 09:12:31
      jdyrlandweaver
      ====================*/
    public void scale(double x, double y, double z)
    {
	transform.makeScale(x, y, z);
	apply();
    }
    
    /*======== public void translate() ==========
      Inputs:  double x
               double y
               double z
      Returns:

      Turn the transform matrix into the appropriate
      translation matrix

      Apply the transformation

      03/09/12 09:13:39
      jdyrlandweaver
      ====================*/
    public void translate(double x, double y, double z)
    {
	transform.makeTranslate(x, y, z);
	apply();
    }
    
    /*======== public void rotX() ==========
      Inputs:   double theta
      Returns:

      Turn the transform matrix into the appropriate
      rotation (x-axis)  matrix

      Users shoud be able to enter angles in degrees,
      but they need to be translated into radians
      in order to work with java's math methods

      Apply the transformation

      03/09/12 09:14:53
      jdyrlandweaver
      ====================*/
    public void rotX(double theta)
    {
	transform.makeRotX(theta);
	apply();
    }
    
    /*======== public void rotY() ==========
      Inputs:   double theta
      Returns:

      Turn the transform matrix into the appropriate
      rotation (y-axis)  matrix

      Users shoud be able to enter angles in degrees,
      but they need to be translated into radians
      in order to work with java's math methods

      Apply the transformation

      03/09/12 09:15:02
      jdyrlandweaver
      ====================*/
    public void rotY(double theta)
    {
	transform.makeRotY(theta);
	apply();
    }
    
    /*======== public void rotZ() ==========
      Inputs:   double theta
      Returns:

      Turn the transform matrix into the appropriate
      rotation (x-axis)  matrix

      Users shoud be able to enter angles in degrees,
      but they need to be translated into radians
      in order to work with java's math methods

      Apply the transformation


      03/09/12 09:15:12
      jdyrlandweaver

      ====================*/
    public void rotZ(double theta)
    {
	transform.makeRotZ(theta);
	apply();
    }
    
    public void setDrawing(int x0, int y0, int x1, int y1)
    {
	drawing = true;
	clearTmp();
	tmpline.addEdge(x0, y0, 0, x1, y1, 0);
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
    
    public void addLine(int x0, int y0, int z0, int x1, int y1, int z1)
    {
	edges.addEdge(x0, y0, z0, x1, y1, z1);
	this.update(this.getGraphics());
    }
    
    public void addPoint(int x0, int y0, int z0)
    {
	edges.addPoint(x0, y0, z0);
	this.update(this.getGraphics());
    }
    
    public void clearTmp()
    {
	tmpline.clear();
    }
    
    public void clearPoints()
    {
	edges.clear();
	this.update(this.getGraphics());
    }
    
    public void paintComponent(Graphics g)
    {

	super.paintComponent(g);
	bi = (BufferedImage)this.createImage(XRES, YRES);
	Graphics2D g2 = bi.createGraphics();

	if (drawing)
	{
	    g2.setColor(TMP_COLOR);
	    g2.drawLine((int)tmpline.getX(0), (int)tmpline.getY(0),
			(int)tmpline.getX(1), (int)tmpline.getY(1));
	}
	
	g2.setColor(c);

	int col = edges.getLastCol();
	for(int i = 0; i < col - 1; i=i+2)
	{
	    g2.drawLine((int)edges.getX(i), (int)edges.getY(i),
			(int)edges.getX(i+1), (int)edges.getY(i+1));
	}

	((Graphics2D)g).drawImage(bi,null,0,0);
    }
}