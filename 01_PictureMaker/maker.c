#include<string.h>
#include<stdlib.h>
#include<fcntl.h>
#include<stdio.h>

void main()
{
  int fd;
  int r = 0;
  int g = 0;
  int b = 0;
  int x;
  int y;
  int xres = 400;
  int yres = 400;
  int maxc = 256;
  char line[256];

  umask(0);
  srand(time(0));

  fd = open("pic.ppm", O_CREAT | O_TRUNC | O_WRONLY, 0666);
  
  sprintf(line, "P3 \n%d %d %d \n", xres, yres, maxc);

  write(fd, line, strlen(line));

  for(x = 0; x < xres; x++)
  {
    r -= 10;
    r += random() % 21;
    g -= 10;
    g += random() % 21;
    b -= 10;
    b += random() % 21;
    r %= maxc;
    if(r < 0){r = 0;}
    g %= maxc;
    if(g < 0){g = 0;}
    b %= maxc;
    if(b < 0){b = 0;}
    for(y = 0; y < yres; y++)
    {
      sprintf(line, "%d %d %d ", r, g, b);
      write(fd, line, strlen(line));
    }
    sprintf(line, "\n");
    write(fd, line, strlen(line));
  }

  close(fd);
}
