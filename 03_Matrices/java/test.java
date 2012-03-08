import java.io.*;
import java.util.*;

import java.awt.*;

public class test {
    public static void main(String[] args) {

	Frame f = new Frame(500, 500);
	Color c = new Color(255, 0, 0);

	EdgeMatrix em = new EdgeMatrix();
	em.addEdge(100, 200, 0, 200, 200, 0);
	em.addEdge(200, 200, 0, 200, 100, 0);
	em.addEdge(200, 100, 0, 100, 100, 0);
	em.addEdge(100, 100, 0, 100, 200, 0);
	em.addEdge(500, 500, 0, 400, 400, 0);
	em.addEdge(500, 400, 0, 400, 500, 0);
	f.drawLines(em, c);
	f.save("pic.png");
	
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
    }
}
