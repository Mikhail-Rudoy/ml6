#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "matrix.h"

/*-------------- struct matrix *new_matrix() --------------
Inputs:  int rows
         int cols 
Returns: 

Once allocated, access the matrix as follows:
m->m[r][c]=something;
if (m->lastcol)... 
*/
struct matrix *new_matrix(int rows, int cols) {
  double **tmp;
  int i;
  struct matrix *m;

  tmp = (double **)malloc(rows * sizeof(double *));
  for (i=0;i<rows;i++) {
      tmp[i]=(double *)malloc(cols * sizeof(double));
    }

  m=(struct matrix *)malloc(sizeof(struct matrix));
  m->m=tmp;
  m->rows = rows;
  m->cols = cols;
  m->lastcol = 0;

  return m;
}


/*-------------- void free_matrix() --------------
Inputs:  struct matrix *m 
Returns: 

1. free individual rows
2. free array holding row pointers
3. free actual matrix
*/
void free_matrix(struct matrix *m) {

  int i;
  for (i=0;i<m->rows;i++) {
      free(m->m[i]);
    }
  free(m->m);
  free(m);
}


/*======== void grow_matrix() ==========
Inputs:  struct matrix *m
         int newcols 
Returns: 

Reallocates the memory for m->m such that it now has
newcols number of collumns
====================*/
void grow_matrix(struct matrix *m, int newcols) {
  int i;
  for (i=0;i<m->rows;i++) {
      m->m[i] = realloc(m->m[i],newcols*sizeof(double));
    }
  m->cols = newcols;
}

/*-------------- void copy_matrix() --------------
Inputs:  struct matrix *a
         struct matrix *b 
Returns: 

copy matrix a to matrix b
*/
void copy_matrix(struct matrix *a, struct matrix *b) {
  int r, c;

  for (r=0; r < a->rows; r++) 
    for (c=0; c < a->cols; c++)  
      b->m[r][c] = a->m[r][c];  
}




/*-------------- void print_matrix() --------------
Inputs:  struct matrix *m 
Returns: 

print the matrix
*/
void print_matrix(struct matrix *m) {
  int i, j;
  for(i = 0; i < (*m).cols; i++){
    for(j = 0; j < (*m).rows; j++)
      printf("%lf ", (*m).m[i][j]);
    printf("\n");
  }
  printf("\n");
}

/*-------------- void ident() --------------
Inputs:  struct matrix *m <-- assumes m is a square matrix
Returns: 

turns m in to an identity matrix
*/
void ident(struct matrix *m)
{
  int x,y;
  for(x = 0; x < m->cols; x++)
  {
    for(y = 0; y < m->rows; y++)
    {
      m->m[x][y] = (x == y);
    }
  }
}


/*-------------- void scalar_mult() --------------
Inputs:  double n
         struct matrix *m 
Returns: 

multiply each element of m by n
*/
void scalar_mult(double n, struct matrix *m)
{
  int x,y;
  for(x = 0; x < m->cols; x++)
  {
    for(y = 0; y < m->rows; y++)
    {
      m->m[x][y] *= n;
    }
  }
}


/*-------------- void matrix_mult() --------------
Inputs:  struct matrix *a
         struct matrix *b 
	 struct matrix *m
Returns: 

*/
void matrix_mult(struct matrix *a, struct matrix *b, struct matrix *m)
{
  int x,y;
  int i;
  for(x = 0; x < m->cols; x++)
  {
    for(y = 0; y < m->rows; y++)
    {
      m->m[x][y] = 0;
      for(i = 0; i < a->cols && i < b->rows; i++)
      {
	m->m[x][y] += ((a->m[x][i]) * (b->m[i][y]));
      }
    }
  }
}
