#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

extern char etext, edata, end;
/*
 * can get this info from man etext
 * https://linux.die.net/man/3/etext
 */

int main(int argc, char *argv[]) {

	// printf("The page size for this system is %ld bytes.\n",				sysconf(_SC_PAGESIZE));

	int v1 = getpid();
	void * v2 = NULL;
	printf("Program PID:\n   %d\n", v1);
	printf("End of Text Section/Program Text (etext):\n");
	printf("   %10p\n", &etext);
	printf("End of Data Section (edata):\n");
	printf("   %10p\n", &edata);
	printf("End of Program/BSS:\n");
	printf("   %10p\n", &end);

	/*
	 * sbrk(0) gets the current location of the program break
	 * https://man7.org/linux/man-pages/man2/brk.2.html
	 * 
	 * sbrk() returns a void pointer.
	 * %p prints a void pointer in hexadecimal.
	 */
	v2 = sbrk(0);
	printf("Program break (end of heap):\n");
	printf("   %p\n", v2);

	int *somep = malloc(10000000000*sizeof(int));

	// make sure lazy memory is used
	if (*somep) {
		for(int n=0; n<10000000000;++n){
			somep[n] = n*n;
		}
	}

	/*
	 * https://stackoverflow.com/questions/54294724/why-does-calling-sbrk0-twice-give-a-different-value
	 */
	v2 = sbrk(0);
	printf("Program break (end of heap):\n");
	printf("   %p\n", v2);

	void *page = sbrk(1024);

	v2 = sbrk(0);
	printf("Program break (end of heap):\n");
	printf("   %p\n", v2);

	//sleep(5550);

	exit(EXIT_SUCCESS);
}
