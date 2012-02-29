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
  double x = 20;
  double y = 250;
  double x2, y2;
  double i = 1;

  srand(time(0));

  do
  {
    randomizeColor(&c);
    
    x2 = 250 + (cos(i) * (x - 250) - sin(i) * (y - 250));
    y2 = 250 + (sin(i) * (x - 250) + cos(i) * (y - 250));
    
    draw_line((int)x, (int)y, (int)x2, (int)y2, s, c);

    x = x2;
    y = y2;
  }
  while(!(x < 20.1 && x > 19.9 && y < 250.1 && y > 249.9));
  
  display(s);
  save_extension(s, "pic.png");
}

void randomizeColor(color* c)
{
  c->red = rand() % 200 + 56;
  c->blue = rand() % 200 + 56;
  c->green = rand() % 200 + 56;
}
