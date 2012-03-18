import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.awt.image.*;
import javax.imageio.*;

import java.io.*;
import java.util.*;

public class gui implements ActionListener,MouseListener, MouseMotionListener
{
    public static final Color IMAGE_BACKGROUND = Color.BLACK;
    public static final Color INTERFACE_BACKGROUND = Color.WHITE;

    JFrame frame;
    Canvas canvas;
    JPanel iface;
    JPanel sidebar;

    JButton clear;
    JButton save;
    JButton quit;
    JLabel fnamelabel;
    JLabel transformlabel;
    JTextField fnamefield;
    JComboBox transformation;
    JTextField xarg;
    JTextField yarg;
    JTextField zarg;
    JLabel xlab;
    JLabel ylab;
    JLabel zlab;
    JButton apply;

    int clickcount=0;
    int[] xes = new int[10];
    int[] ys = new int[10];

    public gui()
    {
	frame = new JFrame();
	canvas = new Canvas();
	canvas.addMouseListener(this);
	canvas.addMouseMotionListener(this);
	
	//set window defaults
	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	frame.getContentPane().setLayout(new FlowLayout());
	frame.setBackground(IMAGE_BACKGROUND);

	//add canvas
	frame.getContentPane().add(canvas);

	//set up the interface area
	iface = new JPanel();
	iface.setLayout(new GridLayout(10,1));
	iface.setBackground(INTERFACE_BACKGROUND);
	
	//add each interface element
        transformation = new JComboBox();
        transformation.addItem("translate");
        transformation.addItem("scale");
        transformation.addItem("x rotation");
        transformation.addItem("y rotation");
        transformation.addItem("z rotation");
	
	transformlabel = new JLabel("Transformation:");
        iface.add( transformlabel );
        iface.add(transformation);
	
	xlab = new JLabel("X: ");
        ylab = new JLabel("Y: ");
        zlab = new JLabel("Z: ");
        xarg = new JTextField();
        yarg = new JTextField();
        zarg = new JTextField();
	
	iface.add(xlab);
        iface.add(xarg);
        iface.add(ylab);
        iface.add(yarg);
        iface.add(zlab);
        iface.add(zarg);

        fnamelabel = new JLabel("Filename");
        fnamefield = new JTextField(4);
        iface.add(fnamelabel);
        iface.add(fnamefield);

        apply = new JButton("Apply");
        quit = new JButton("Quit");
        clear = new JButton("Clear");
        save = new JButton("Save");
	
	apply.addActionListener(this);
        quit.addActionListener(this);
        clear.addActionListener(this);
        save.addActionListener(this);
        iface.add(apply);
        iface.add(clear);
        iface.add(save);
        iface.add(quit);
	
	sidebar = new JPanel();
        sidebar.setPreferredSize(new Dimension(250, 800));
        sidebar.setBackground(INTERFACE_BACKGROUND);
        sidebar.add(iface);
	
	//add interface
	frame.getContentPane().add(iface);

	frame.pack();
	frame.setVisible(true);
    }
    
    public void mousePressed(MouseEvent e)
    {
	xes[0] = e.getX();
	ys[0] = e.getY();
    }	
    
    public void mouseDragged(MouseEvent e)
    {
	canvas.setDrawing(xes[0], ys[0], e.getX(), e.getY());
	canvas.paintComponent(canvas.getGraphics());
	canvas.clearTmp();
    }
    
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


    public void actionPerformed(ActionEvent e)
    {
	if(e.getSource() == quit)
	{
	    System.exit(0);
	}
	else if(e.getSource() == save)
	{
	    // save
	    System.out.println("Saving: " + fnamefield.getText());
	    BufferedImage bi = canvas.getBufferedImage();
	    try
	    {
		File fn = new File(fnamefield.getText());
		ImageIO.write(bi,"png",fn);
	    }
	    catch (IOException ex) { }
	}
	else if(e.getSource() == clear)
	{
	    canvas.clearPoints();
	}
	else if(e.getSource() == apply)
	{
	    switch(((String)transformation.getSelectedItem()).charAt(0))
	    {
	    case 't':
	        canvas.translate(Double.parseDouble(xarg.getText()), 
				 Double.parseDouble(yarg.getText()),
				 Double.parseDouble(zarg.getText()));
		break;
	    case 's':
	        canvas.scale(Double.parseDouble(xarg.getText()),
			     Double.parseDouble(yarg.getText()),
			     Double.parseDouble(zarg.getText()));
		break;
	    case 'x':
	        canvas.rotX(Double.parseDouble(xarg.getText()) * 0.0174532925);
		break;
	    case 'y':
	        canvas.rotY(Double.parseDouble(yarg.getText()) * 0.0174532925);
		break;
	    case 'z':
	        canvas.rotZ(Double.parseDouble(zarg.getText()) * 0.0174532925);
		break;
	    }
	}
    }

    public static void main(String[] args)
    {
	gui g = new gui();
    }
}