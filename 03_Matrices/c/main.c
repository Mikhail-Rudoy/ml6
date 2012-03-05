#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ml6.h"
#include "display.h"
#include "draw.h"
#include "matrix.h"

int main() 
{
  struct matrix* edges = new_matrix(4, 4);
  ident(edges);
  add_edge(edges, 100, 200, 0, 200, 200, 0);
  add_edge(edges, 200, 200, 0, 200, 100, 0);
  add_edge(edges, 200, 100, 0, 100, 100, 0);
  add_edge(edges, 100, 100, 0, 100, 200, 0);
  add_edge(edges, 500, 500, 0, 400, 400, 0);
  add_edge(edges, 500, 400, 0, 400, 500, 0);
  print_matrix(edges);
  screen s;
  color c;
  c.red = 255;
  c.blue = 0;
  c.green = 0;

  draw_lines(edges, s, c);
  display(s);  

  struct matrix* mat = new_matrix(4, 4);
  struct matrix* m2 = new_matrix(4, 4);
  struct matrix* m3 = new_matrix(4, 4);
  int i, j;
  print_matrix(mat);
  ident(mat);
  print_matrix(mat);
  mat->m[1][2]=5;
  mat->m[1][3]=7;
  print_matrix(mat);
  scalar_mult(2, mat);
  print_matrix(mat);
  scalar_mult(-3, mat);
  print_matrix(mat);
  ident(m2);
  matrix_mult(mat, m2, m3);
  print_matrix(m3);
  matrix_mult(m2, mat, m3);
  print_matrix(m3);
  for(i = 0; i < 4; i++)
  {
    for(j = 0; j < 4; j++)
    {
      m2->m[i][j] = i * j + 3 + j * j + i;
    }
  }
  print_matrix(m2);
  matrix_mult(m3, m2, mat);
  print_matrix(mat);
}  
