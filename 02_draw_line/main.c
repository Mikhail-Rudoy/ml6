#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"

int main() {

  screen s;
  color c;

  c.red = 0;
  c.green = 255;
  c.blue = 255;

  draw_line(0, 0, XRES, YRES-50, s, c);

  display( s );
  
  
}  
