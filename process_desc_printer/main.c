#include <stdio.h>
#include <stdlib.h>

extern char etext, edata, end;
/*
 * can get this info from man etext
 * https://linux.die.net/man/3/etext
 */

int main(int argc, char *argv[]) {
	printf("First address past:\n");
	printf("   program text (etext)      %10p\n", &etext);
	printf("   initialized data (edata)  %10p\n", &edata);
	printf("   uninitialized data (end)  %10p\n", &end);

	exit(EXIT_SUCCESS);
}
