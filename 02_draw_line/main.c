#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"

void randomizeColor(color*);

int main()
{
  screen s;
  color c;
  int x = 150;
  int y = 250;
  int x2, y2;
  double i = 2;

  srand(time(0));
  
  do
  {
    randomizeColor(&c);
    
    //find x2, y2
    x2 = (int)(250 + 100 * cos(i + atan2(y - 250, x - 250)));
    y2 = (int)(250 + 100 * sin(i + atan2(y - 250, x - 250)));
    
    draw_line(x, y, x2, y2, s, c);
    x = x2;
    y = y2;
  }
  while(!(x == 150 && y == 250));

  display(s); 
}

void randomizeColor(color* c)
{
  c->red = rand() % 255;
  c->blue = rand() % 255;
  c->green = rand() % 255;
}
