#include <stdio.h>
#include <stdlib.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"

//Insert your line algorithm here
void draw_line(int x0, int y0, int x1, int y1, screen s, color c)
{
  int dx, dy;
  int x, y, s;

  dx = x1-x0;
  dy = y1-y0;

  if(dx == 0)//vertical line
  {
    for(y = (dy > 0) ? y0 : y1; y <= y1 && y <= y0; y++)
    {
      plot(s, c, x0, y);
    }
  }
  else if(dy == 0)//horizontal line
  {
    for(x = (dx > 0) ? x0 : x1; x <= x1 && x <= x0; x++)
    {
      plot(s, c, x, y0);
    }
  }
  else if(dy == dx)//diagonal top-left/bottom-right
  {
    for(x = (dx > 0) ? x0 : x1, y = (dy > 0) ? y0 : y1; x <= x1 && x <= x0; x++, y++)
    {
      plot(s, c, x, y);
    }
  }
  else if(dy + dx == 0)//diagonal top-right/bottom-left
  {
    for(x = (dx > 0) ? x0 : x1, y = (dy < 0) ? y0 : y1; x <= x1 && x <= x0; x++, y--)
    {
      plot(s, c, x, y);
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
      
    }
    else if(dx < 0)//octant 3
    {

    }
    else if(dx > dy)//octant 1
    {
      for(x = x0, y = y0; x <= x1; x++)
      {
	plot(s, c, x, y);
	if(s > 0)
	{
	  y++;
	  s = s + dx;
	}
	x++;
	s = s - dy;
      }
    }
    else//octant 2
    {

    } 
  }
}

