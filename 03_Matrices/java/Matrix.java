/*========== Matrix.java ==========
  Matrix will hold a 2-d array of doubles and have a default size of 4x4.
  Handles basic matrix maintenence and math.
  Creates transformation matricies for tralation, scale and rotate
=========================*/

import java.io.*;
import java.util.*;

public class Matrix {

    public static final int DEFAULT_SIZE = 4;
    protected double[][] m;

    /*===========Constructors================
      Default constructor creates a 4x4 matrix
      Second constructor creates a 4xN matrix
    */
    public Matrix()
    {
	m = new double[DEFAULT_SIZE][DEFAULT_SIZE];
    }
    
    public Matrix(int c)
    {
	m = new double[DEFAULT_SIZE][c];
    }
    
    public Matrix(int r, int c);
    {
	m = new double[r][c];
    }
    
    /*===========grow================
      Increase the number of columns in a matrix by 10
      You can change the growth factor as you see fit
    */
    public void grow()
    {
	double[][] n = new double[m.length][m[0].length + 10];
	for (int r = 0; r < m.length; r++)
	{
	    for (int c = 0; c < m[r].length; c++)
	    {
		n[r][c] = m[r][c];
	    }
	}
	m = n;
    }

    /*======== public void clear() ==========
      Inputs:  
      Returns: 
      Sets every entry in the matrix to 0
      ====================*/
    public void clear()
    {
	for (int i = 0; i < m.length; i++)
	{
	    for (int j = 0; j < m[i].length; j++)
	    {
		m[i][j] = 0;
	    }
	}
    }

    /*===========ident================
      Turns this matrix into the indentity matrix
      You may assume the calling Matrix is square
    */
    public void ident()
    {
	for (int i = 0; i < m.length; i++)
	{
	    for (int j = 0; j < m[i].length; j++)
	    {
		m[i][j] = i == j ? 1 : 0;
	    }
	}
    }

    /*===========scalarMult================
      Inputs:  double x
      
      multiply each element of the calling matrix by x
    */
    public void scalarMult(int s)
    {
	for (int i = 0; i < m.length; i++)
	{
	    for (int j = 0; j < m[i].length; j++)
	    {
		m[i][j] = s * m[i][j];
	    }
	}
    }		

    /*===========matrixMult================
      Multply matrix n by the calling matrix, modify
      the calling matrix to store the result.
      
      eg.
      In the call a.matrixMult(n), n will remain the same
      and a will now be the product of n * a
    */
    public void matrixMult(Matrix n)
    {
	double[][] tmp = new double[n.m.length][m[0].length];
	for(int r = 0; r < tmp.length; r++)
	{
	    for(int c = 0; c < tmp[r].length; c++)
	    {
		tmp[r][c] = 0;
		for(int i = 0; i < m.length && i < n.m.length; i++)
		{
		    tmp[r][c] += n.m[r][i] * m[i][c];
		}
	    }
	}
	m = tmp;
    }
   
    /*===========copy================
      Create and return new matrix that is a duplicate 
      of the calling matrix
    */
    public Matrix copy()
    {
	Matrix result = new Matrix(m.length, m[0].length);
	for(int r = 0; r < m.length; r++)
	{
	    for(int c = 0; c < m[r].length; c++)
	    {
		result.m[r][c] = m[r][c];
	    }
	}
	return result;
    }

    /*===========toString================
      Crate a readable String representation of the 
      calling matrix.
    */
    public String toString()
    {
	String result = "";
	for (int i = 0; i < m.length; i++)
	{
	    for (int j = 0; j < m[i].length; j++)
	    {
		result = result + m[i][j];
	    }
	    result = result + "\n";
	}
	return result;
    }

}
