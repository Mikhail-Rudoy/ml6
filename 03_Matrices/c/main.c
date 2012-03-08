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
  add_edge(edges, 100, 200, 0, 200, 200, 0);
  add_edge(edges, 200, 200, 0, 200, 100, 0);
  add_edge(edges, 200, 100, 0, 100, 100, 0);
  add_edge(edges, 100, 100, 0, 100, 200, 0);
  add_edge(edges, 500, 500, 0, 400, 400, 0);
  add_edge(edges, 500, 400, 0, 400, 500, 0);
  screen s;
  color c;
  c.red = 255;
  c.blue = 0;
  c.green = 0;
  draw_lines(edges, s, c);
  save_ppm(s, "pic.ppm");

  struct matrix* A = new_matrix(4, 4);
  struct matrix* B = new_matrix(4, 4);
  struct matrix* C = new_matrix(4, 4);
  struct matrix* D = new_matrix(4, 4);
  struct matrix* E = new_matrix(4, 4);
  struct matrix* tmp;
  int i, j;
  for(i = 0; i < 4; i++)
  {
    for(j = 0; j < 4; j++)
    {
      B->m[i][j] = (i - 2.5) * (i - 2.5) * (3 * j * j * j - 1);
      C->m[i][j] = i + j + 3;
      D->m[i][j] = 100 - i * j / 0.3;
      E->m[i][j] = 4 * i + j;
    }
  }
  ident(A);
  printf("Matrix A set by ident method\n");
  print_matrix(A);
  printf("Matrix B set by hand\n");
  print_matrix(B);
  tmp = matrix_mult(A, B);
  printf("A*B=\n");
  print_matrix(tmp);
  free_matrix(tmp);
  tmp = matrix_mult(B, A);
  printf("B*A=\n");
  print_matrix(tmp);
  free_matrix(tmp);
  printf("Matrix C set by hand\n");
  print_matrix(C);
  printf("Matrix D set by hand\n");
  print_matrix(D);
  tmp = matrix_mult(C, D);
  printf("C*D=\n");
  print_matrix(tmp);
  free_matrix(tmp);
  printf("Matrix E set by hand\n");
  print_matrix(E);
  scalar_mult(2, E);
  printf("2*E=\n");
  print_matrix(E);
  return 0;
}  
