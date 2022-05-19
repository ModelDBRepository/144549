// $Id: misc.h,v 1.33 2010/06/05 15:32:28 billl Exp $

#include <stdlib.h>
#include <math.h>
#include <limits.h> /* contains LONG_MAX */
#include <time.h>
#include <sys/time.h>
#if defined(__APPLE__) && defined(__MACH__)
 #include <float.h>
#else
 #include <values.h>
#endif
#include <pthread.h>

#if !defined(t)
  #define _pval pval
#endif

typedef struct LISTVEC {
  int isz;
  Object* pL;
  double** pv;
  unsigned int* plen;
  unsigned int* pbuflen;
} ListVec;

typedef struct BVEC {
 int size;
 int bufsize;
 short *x;
 Object* o;
} bvec;

#define BYTEHEADER int _II__;  char *_IN__; char _OUT__[16]; int BYTESWAP_FLAG=0;
#define BYTESWAP(_X__,_TYPE__) \
    if (BYTESWAP_FLAG == 1) { \
	_IN__ = (char *) &(_X__); \
	for (_II__=0;_II__<sizeof(_TYPE__);_II__++) { \
		_OUT__[_II__] = _IN__[sizeof(_TYPE__)-_II__-1]; } \
	(_X__) = *((_TYPE__ *) &_OUT__); \
    }

#define UNCODE(_X_,_J_,_Y_) {(_Y_)=floor((_X_)/sc[(_J_)])/sc[4]; \
                             (_Y_)=floor(sc[4]*((_Y_)-floor(_Y_))+0.5);}
#define MIN(X,Y) ((X) < (Y) ? (X) : (Y))
#define MAX(X,Y) ((X) > (Y) ? (X) : (Y))

//square root of 2 * PI
#define SQRT2PI 2.5066282746310002416
//ln(2), base e log of 2
#define LG2 0.69314718055994530941723212145818
#define VRRY 200
#define ISVEC(_OB__) (strncmp(hoc_object_name(_OB__),"Vector",6)==0)

// Andre Fentons cast designations
typedef	unsigned char	ui1;	/* one byte unsigned integer */
typedef	char		si1;	/* one byte signed integer */
typedef unsigned short	ui2;	/* two byte unsigned integer */
typedef short		si2;	/* two byte signed integer */
typedef unsigned int	ui4;	/* four byte unsigned integer */
typedef int		si4;	/* four byte signed integer */
typedef float		sf4;	/* four byte signed floating point number */
typedef double		sf8;	/* eight byte signed floating point number */

extern double ERR,GET,SET,OK,NOP,ALL,NEG,POS,CHK,NOZ,GTH,GTE,LTH,LTE,EQU;
extern double EQV,EQW,EQX,NEQ,SEQ,RXP,IBE,EBI,IBI,EBE;

extern unsigned int  dcrsz;
extern double       *dcr;
extern double       *dcrset(int);
extern unsigned int  scrsz;
extern unsigned int *scr;
extern unsigned int *scrset(int);
extern unsigned int  iscrsz;
extern int *iscr;
extern int *iscrset(int);
extern double BVBASE;
#ifndef NRN_VERSION_GTEQ_8_2_0
extern double* hoc_pgetarg();
extern void hoc_notify_iv();
extern double hoc_call_func(Symbol*, int narg);
extern FILE* hoc_obj_file_arg(int narg);
extern Object** hoc_objgetarg();
char *gargstr();
char** hoc_pgargstr();
extern void vector_resize();
extern int vector_instance_px();
extern void* vector_arg();
extern double* vector_vec();
extern int vector_buffer_size(void*);
extern double hoc_epsilon;
extern int stoprun;
extern void set_seed();
extern unsigned int valseed;
extern void mcell_ran4_init(unsigned int *idum);
extern double mcell_ran4(unsigned int* idum,double* ran_vec,unsigned int n,double range);
extern int nrn_mlh_gsort();
extern int ivoc_list_count(Object*);
extern Object* ivoc_list_item(Object*, int);
extern int hoc_is_double_arg(int narg);
extern int hoc_is_str_arg(int narg);
extern int hoc_is_object_arg(int narg);
extern int hoc_is_pdouble_arg(int narg);
extern Symbol *hoc_get_symbol(char *);
extern Symbol *hoc_lookup(const char*);
extern Point_process* ob2pntproc(Object*);

extern char* hoc_object_name(Object*);
void FillListVec(ListVec* p,double dval);
void ListVecResize(ListVec* p,int newsz);
extern short *nrn_artcell_qindex_;
extern double nrn_event_queue_stats(double*);
extern void clear_event_queue();
#endif
ListVec* AllocListVec(Object* p);
ListVec* AllocILV(Object*, int, double *);
int cmpdfn(double a, double b);
void dshuffle(double* x, int nx);
void FreeListVec(ListVec** pp);
static void hxe() { hoc_execerror("",0); }
int IsList(Object* p);
int list_vector_px(Object *ob, int i, double** px);
int list_vector_px2(Object *ob, int i, double** px, void** vv);
int list_vector_px3(Object *ob, int i, double** px, void** vv);
int list_vector_px4(Object *ob, int i, double** px, unsigned int n);
double* list_vector_resize(Object *ob, int i, int sz);
int openvec(int, double **);
int uniq2(int n, double *x, double *y, double *z);
double *vector_newsize(void* vv, int n);

static double sc[6];
static FILE*  testout;

//* in vecst.mod
extern int** getint2D(int rows,int cols);
extern void freeint2D(int*** ppp,int rows);
extern double** getdouble2D(int rows,int cols);
extern void freedouble2D(double*** ppp,int rows);
extern double ismono1 (double *x, int n, int flag);

//* in stats.mod
double kcorfast(double* input1, double* input2, double* i1d , double* i2d,int n,double* ps);
double Rktau (double* x, double* y, int n); // R version
double kcorfast (double* input1, double* input2, double* i1d , double* i2d,int n,double* ps);
