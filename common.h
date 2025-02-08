#include <stdlib.h>
#include <wchar.h>
#include <wctype.h>
#include <stdio.h>
#include <locale.h>
#include <langinfo.h>
#include <assert.h>
#include <ctype.h>
#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

#ifndef COMMON_H
#define COMMON_H


#define UNDEF -1
#define BUF_LEN 256
#define INFTY 1000000
#define EPS 0.000001

#ifndef MAX
#define MAX(a,b) (((a)>(b))?(a):(b))
#define MIN(a,b) (((a)<(b))?(a):(b))
#endif

#ifndef SQR
#define SQR(x) ((x) * (x))
#endif

#define ERR_MESG(x) { perror(x); return -1; }

#define Malloc(n,type) (type *) malloc( (unsigned) ((n)*sizeof(type)))
#define Realloc(loc,n,type) (type *) realloc( (char *)(loc), \
                                              (unsigned) ((n)*sizeof(type)))

#define matrix_alloc(mat,rows,cols,type) {                        \
    int ii;                                                       \
    type *temp;                                                   \
                                                                  \
    if (NULL == (mat = (type **) malloc(rows*sizeof(type *))))    \
       ERR_MESG("Out of memory");                                 \
    if (NULL == (temp = (type *) calloc(rows*cols,sizeof(type)))) \
        ERR_MESG("Out of memory");                                \
    for (ii = 0; ii < rows; temp += cols, ii++)                   \
        mat[ii] = temp;                                           \
  }

#define matrix_free(mat) {                      \
    free(mat[0]);                               \
    free(mat);                                  \
  }

#endif


FILE* FOPEN(char name[], char mode[])
{ 
  FILE *f;
  if((f = fopen(name, mode)) == NULL) {
    printf("Could not open file <%s>\t in <%s> mode \n", name, mode);
    exit(0) ;
  }
  return f;
}

void sig_end_prog()
{
  system("vlc /home/jiaul/songs/Violin/ShortBus.mp3");
}
