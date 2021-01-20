#include <stdio.h>
#include <stdlib.h>

extern char etext, edata, end;
/*
 * can get this info from man etext
 * https://linux.die.net/man/3/etext
 */

int main(int argc, char *argv[]) {

	printf("End of Text Section (edata):\n");
	/*printf("   program text (etext)      %10p\n", &etext);*/
	printf("   initialized data (edata)  %10p\n", &edata);
	printf("End of Data Section (start of heap):\n");
	printf("   uninitialized data (end)  %10p\n", &end);

	exit(EXIT_SUCCESS);
}
