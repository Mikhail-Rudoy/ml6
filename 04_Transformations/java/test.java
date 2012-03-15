import java.io.*;
import java.util.*;
import java.lang.Math.*;

public class test
{
    public static void main(String[] args)
    {
	Parser p = new Parser();
	
       	try
	{
	    FileReader in = new FileReader(args[0]);
	    BufferedReader bin = new BufferedReader(in);
	    p.parseFile(bin);
	}
	catch (IOException e)
	{
	    
	}
    }
}