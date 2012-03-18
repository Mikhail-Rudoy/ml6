#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <unistd.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"
#include "matrix.h"
#include "parser.h"


/*======== void parse_file () ==========
Inputs:   char * filename 
          struct matrix * transform, 
          struct matrix * pm,
          screen s
Returns: 

Goes through the file named filename and performs all of the actions listed in that file.
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
	 v: draw the lines of the edge matrix to the screen
	    display the screen
	 g: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 q: end parsing

See the file script for an example of the file format

IMPORTANT MATH NOTE:
the trig functions int math.h use radian mesure, but us normal
humans use degrees, so the file will contain degrees for rotations,
be sure to conver those degrees to radians (M_PI is the constant
for PI)

03/08/12 16:22:10
jdyrlandweaver
====================*/
void parse_file ( char * filename, 
                  struct matrix * transform, 
                  struct matrix * pm,
                  screen s)
{
  char line[512];
  color c;
  double args[6];
  struct matrix* tmp;
  FILE* file = fopen(filename, "r");
  if(file)
  {
    for(fgets(line, 512, file); strcmp(line, "q\n"); fgets(line, 512, file))
    {
      sleep(2);
      if(!strcmp(line, "i\n"))
      {
	ident(transform);
      }
      else if(!strcmp(line, "a\n"))
      {
	matrix_mult(transform, pm);
      }
      else if(!strcmp(line, "v\n"))
      {
	c.red = 0;
	c.green = 0;
	c.blue = 255;
	clear_screen(s);
	draw_lines(pm, s, c);
	display(s);
      }
      else if(!strcmp(line, "l\n"))
      {
	fgets(line, 512, file);
	sscanf(line, "%lf %lf %lf %lf %lf %lf ", &args[0], &args[1], &args[2], 
	       &args[3], &args[4], &args[5]);
	add_edge(pm, args[0], args[1], args[2], 
	       args[3], args[4], args[5]);
	printf("%lf %lf %lf %lf %lf %lf\n", args[0], args[1], args[2],
               args[3], args[4], args[5]);
      }
      else if(!strcmp(line, "s\n"))
      {
	fgets(line, 512, file);
	sscanf(line, "%lf %lf %lf ", &args[0], &args[1], &args[2]);
	tmp = make_scale(args[0], args[1], args[2]);
	matrix_mult(tmp, transform);
	free_matrix(tmp);
	printf("%lf %lf %lf\n", args[0], args[1], args[2]);
      }
      else if(!strcmp(line, "t\n"))
      {
	fgets(line, 512, file);
	sscanf(line, "%lf %lf %lf", &args[0], &args[1], &args[2]);
	tmp = make_translate(args[0], args[1], args[2]);
	matrix_mult(tmp, transform);
	free_matrix(tmp);
	printf("%lf %lf %lf\n", args[0], args[1], args[2]);
      }
      else if(!strcmp(line, "x\n"))
      {
	fgets(line, 512, file);
	sscanf(line, "%lf ", &args[0]);
	tmp = make_rotX(args[0] * 3.14159265358979323846264338327950 / 180.0);
	matrix_mult(tmp, transform);
	free_matrix(tmp);
	printf("%lf\n", args[0]);
      }
      else if(!strcmp(line, "y\n"))
      {
	fgets(line, 512, file);
	sscanf(line, "%lf ", &args[0]);
	tmp = make_rotY(args[0] * 3.14159265358979323846264338327950 / 180.0);
	matrix_mult(tmp, transform);
	free_matrix(tmp);
	printf("%lf\n", args[0]);
      }
      else if(!strcmp(line, "z\n"))
      {
	fgets(line, 512, file);
	sscanf(line, "%lf", &args[0]);
	tmp = make_rotZ(args[0] * 3.14159265358979323846264338327950 / 180.0);
	matrix_mult(tmp, transform);
	free_matrix(tmp);
	printf("%lf\n", args[0]);
      }
      else if(!strcmp(line, "g\n"))
      {
	fgets(line, 512, file);
	strtok(line, "\n");
	c.red = 0;
	c.green = 0;
	c.blue = 255;
	clear_screen(s);
	draw_lines(pm, s, c);
	save_extension(s, line);
	printf("%s\n", line);
      }
    }
  }
  else
  {
    printf("Invalid filename passed: %s", filename);
  }
  fclose(file);
}
