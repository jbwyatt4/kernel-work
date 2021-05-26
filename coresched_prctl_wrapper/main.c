#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */

#include <sys/prctl.h>

int main(int argc, char *argv[]) {
	pid_t pid=fork();
	if (pid == 0) { /* Child Process*/
		static char *argv[]={"stress-ng", "--matrix", "0", "-t", "30s"};
		/*execv("stress-ng", argv);*/
		execv("/usr/bin/stress-ng",argv);
		printf("Should not get here!\n");
		exit(127); /* only if execv fails */
	} else { /* Parent Process */
		/* PID=TID when there is only one thread for a process */
		printf("Waiting!\n");
		waitpid(pid,0,0); /* wait for child to exit */
	}
	return EXIT_SUCCESS;
}
