import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.awt.image.*;
import javax.imageio.*;

import java.io.*;
import java.util.*;

public class guiBasic implements ActionListener,MouseListener, MouseMotionListener {
    JFrame frame;
    Canvas canvas;
    JPanel iface;

    JButton clear;
    JButton save;
    JButton quit;
    JLabel fnamelabel;
    JTextField fnamefield;

    int clickcount=0;
    int[] xes = new int[10];
    int[] ys = new int[10];

    public guiBasic() {

	frame = new JFrame();
	canvas = new Canvas();
	canvas.addMouseListener(this);
	canvas.addMouseMotionListener(this);

	//set window defaults
	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	frame.getContentPane().setLayout(new FlowLayout());

	//add canvas
	frame.getContentPane().add(canvas);

	//set up the interface area
	iface = new JPanel();
	iface.setLayout(new GridLayout(10,1));

	fnamelabel = new JLabel("Filename");
	fnamefield = new JTextField(4);
	iface.add(fnamelabel);
	iface.add(fnamefield);

	quit = new JButton("Quit");
	clear = new JButton("Clear");
	save = new JButton("Save");

	quit.addActionListener(this);
	clear.addActionListener(this);
	save.addActionListener(this);
	iface.add(clear);
	iface.add(save);
	iface.add(quit);

	//add interface
	frame.getContentPane().add(iface);

	frame.pack();
	frame.setVisible(true);
    }

    /*======== public void mousePressed() ==========
      
      mousePressed is triggered when the left mouse button 
      is initially pressed down. 

      The current x and y coordiantes of the mouse should
      be stored in the first index of xes and ys, respectively.
      
      No drawing occurs when the mouse is initially pressed.

      e.getX() and e.getY() will return the current x and
      y coordinates.
      ====================*/
    public void mousePressed(MouseEvent e)
    {
	xes[0] = e.getX();
	ys[0] = e.getY();
    }	

    
    /*======== public void mouseDragged() ==========

      mouseDragged is triggered when the left mouse button
      is being held down and the mouse is moving.
      
      When the mouse is being dragged, the temporary line in 
      canvas should be updated to draw the line from the (x, y)
      position when the mouse was initially clicked (stored in 
      xes and ys) and the current (x,y) position

      You should use the setDrawing() method in canvas
      Make sure that you only draw one temporary line at
      a time.
      ====================*/
    public void mouseDragged(MouseEvent e)
    {
	canvas.setDrawing(xes[0], ys[0], e.getX(), e.getY());
    }
    
    /*======== public void mouseReleased() ==========

      mouseReleased is triggered when the left mouse button
      is released. This should signal the end of the temporary
      line drawing and add the line to the canvas' permanant
      edge matrix.

      You should use addLine and stopDrawing
      ====================*/
    public void mouseReleased(MouseEvent e)
    {
	canvas.addLine(xes[0], ys[0], 0, e.getX(), e.getY(), 0);
	canvas.stopDrawing();
    }

    //needed to implement MouseListener and MouseMotionListener
    //but not needed for this project
    public void mouseMoved(MouseEvent e) {}  
    public void mouseEntered(MouseEvent e) {}
    public void mouseExited(MouseEvent e) {}
    public void mouseClicked(MouseEvent e) {}


    public void actionPerformed(ActionEvent e) {
	if (e.getSource()==quit) {
	    System.exit(0);
	}
	
	else if (e.getSource()==save) {
	    // save
	    System.out.println("Saving: "+ fnamefield.getText() );
	    BufferedImage bi = canvas.getBufferedImage();
	    try {
		File fn = new File(fnamefield.getText());
		ImageIO.write(bi,"png",fn);
	    }
	    catch (IOException ex) { }
	}
	else if (e.getSource()==clear) {
	    canvas.clearPoints();
	}
    }

    public static void main(String[] args)
    {
	
        Matrix A = new Matrix(4, 4);
        Matrix B = new Matrix(4, 4);
        Matrix C = new Matrix(4, 4);
        Matrix D = new Matrix(4, 4);
        Matrix E = new Matrix(4, 4);
        for(int i = 0; i < 4; i++)
	    {
		for(int j = 0; j < 4; j++)
		    {
			B.m[i][j] = (i - 2.5) * (i - 2.5) * (3 * j * j * j - 1);
			C.m[i][j] = i + j + 3;
			D.m[i][j] = 100 - i * j / 0.3;
			E.m[i][j] = 4 * i + j;
		    }
	    }
        A.ident();
        System.out.println("Matrix A set by ident method");
        System.out.println(A);
        System.out.println("Matrix B set by hand");
        System.out.println(B);
        B.matrixMult(A);
        System.out.println("A*B=");
        System.out.println(B);
        A.matrixMult(B);
        System.out.println("B*A=");
        System.out.println(A);
        System.out.println("Matrix C set by hand");
        System.out.println(C);
        System.out.println("Matrix D set by hand");
        System.out.println(D);
        D.matrixMult(C);
        System.out.println("C*D=");
        System.out.println(D);
        System.out.println("Matrix E set by hand");
        System.out.println(E);
        E.scalarMult(2);
        System.out.println("2*E=");
        System.out.println(E);
	
	guiBasic g = new guiBasic();
    }
}