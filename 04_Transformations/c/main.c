#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"
#include "matrix.h"
#include "parser.h"

int main(int argc, char** argv)
{
  struct matrix* edges = new_matrix(4, 4);
  struct matrix* transform = new_matrix(4, 4);
  screen s;

  if(argc < 2)
  {
    printf("Not enough arguments; please provide the name of a script file");
    return 1;
  }
  
  parse_file(argv[1], transform, edges, s); 

  free_matrix(transform);
  free_matrix(edges);
  return 0;
}  
