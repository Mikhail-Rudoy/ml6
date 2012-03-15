/*========== Parser.java ==========

Goes through a file and performs all of the actions listed.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         l: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 i: set the transform matrix to the identity matrix - 
	 s: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 t: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 x: create an x-axis rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 1 argument (theta)
	 y: create an y-axis rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 1 argument (theta)
	 z: create an z-axis rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 1 argument (theta)
	 a: apply the current transformation matrix to the 
	    edge matrix
	 g: draw the lines of the edge matrix to the Frame
	    save the Frame to a file -
	    takes 1 argument (file name)
	 q: end parsing

See the file script for an example of the file format


IMPORTANT MATH NOTE:
the trig functions in java.Math  use radian mesure, but us normal
humans use degrees, so the file will contain degrees for rotations,
be sure to conver those degrees to radians (Math.PI is the constant
for PI)


jdyrlandweaver
=========================*/

import java.io.*;
import java.util.*;
import java.awt.*;

public class Parser {
    
    /*===========================
      transform is the master transform Matrix
      em is the master EdgeMatrix
      f is the frame used for drawing and saving
      =========================*/
    private Matrix transform;
    private EdgeMatrix em;
    private Frame f;

    public Parser()
    {
	f = new Frame();
	transform = new Matrix(4, 4);
	em = new EdgeMatrix();
	transform.ident();
    }


    /*========     public void parseFile() ==========
      Inputs:   BufferedReader in  
      Returns: 

      Goes through the input stream referred to by in,
      scans it for the commands listed above, and performs
      the required commands.
      
      03/08/12 19:20:55
      jdyrlandweaver
      ====================*/
    public void parseFile(BufferedReader in) throws IOException
    {
	String[] args;
	String line;
	for(line = in.readLine(); line != null && !line.equals("q"); line = in.readLine())
	{
	    if(line.length() != 1)
	    {
		continue;
	    }
	    switch(line.charAt(0))
	    {
	    case 'l':
		line = in.readLine();
		args = line.split(" ");
		em.addEdge(Integer.parseInt(args[0]),
			   Integer.parseInt(args[1]),
			   Integer.parseInt(args[2]),
			   Integer.parseInt(args[3]),
			   Integer.parseInt(args[4]),
			   Integer.parseInt(args[5]));
		break;
	    case 'i':
		transform.ident();
		break;
	    case 's':
		line = in.readLine();
		args = line.split(" ");
		Matrix s = new Matrix(4, 4);
		s.makeScale(Double.parseDouble(args[0]),
			    Double.parseDouble(args[1]),
			    Double.parseDouble(args[2]));
		transform.matrixMult(s);
		break;
	    case 't':
		line = in.readLine();
		args = line.split(" ");
		Matrix t = new Matrix(4, 4);
		t.makeTranslate(Double.parseDouble(args[0]),
				Double.parseDouble(args[1]),
				Double.parseDouble(args[2]));
		transform.matrixMult(t);
		break;
	    case 'x':
		line = in.readLine();
		args = line.split(" ");
		Matrix rx = new Matrix(4, 4);
		rx.makeRotX(Double.parseDouble(args[0]));
		transform.matrixMult(rx);
		break;
	    case 'y':
		line = in.readLine();
		args = line.split(" ");
		Matrix ry = new Matrix(4, 4);
		ry.makeRotY(Double.parseDouble(args[0]));
		transform.matrixMult(ry);
		break;
	    case 'z':
		line = in.readLine();
		args = line.split(" ");
		Matrix rz = new Matrix(4, 4);
		rz.makeRotZ(Double.parseDouble(args[0]));
		transform.matrixMult(rz);
		break;
	    case 'a':
		em.matrixMult(transform);
		break;
	    case 'g':
		line = in.readLine();
		args = line.split(" ");
		if(args.length == 3)
		{
		    f = new Frame(Integer.parseInt(args[1]), Integer.parseInt(args[2]));
		}
		else
		{
		    f = new Frame();
		}
		f.drawLines(em, new Color(0, 255, 0));
		f.save(args[0]);
		break;
	    }
	}
    }
}