#include <stdio.h>
#include <stdlib.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"

//Insert your line algorithm here
void draw_line(int x0, int y0, int x1, int y1, screen s, color c)
{
  int dx, dy;
  int x, y;

  dx = x1-x0;
  dy = y1-y0;

  if(dx == 0)
  {
    for(y = (dy > 0) ? y0 : y1; y <= y1 && y <= y0; y++)
    {
      plot(s, c, x0, y);
    }
  }
  else if(dy == 0)
  {
    for(x = (dx > 0) ? x0 : x1; x <= x1 && x <= x0; x++)
    {
      plot(s, c, x, y0);
    }
  }
  else if(dy == dx)
  {
    for(x = (dx > 0) ? x0 : x1, y = (dy > 0) ? y0 : y1; x <= x1 && x <= x0; x++, y++)
    {
      plot(s, c, x, y);
    }
  }
  else if(dy + dx == 0)
  {
    for(x = (dx > 0) ? x0 : x1, y = (dy < 0) ? y0 : y1; x <= x1 && x <= x0; x++, y--)
    {
      plot(s, c, x, y);
    }
  }
}

