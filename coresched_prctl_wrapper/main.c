// SPDX-License-Identifier: GPL-2.0-or-later

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */

#include <sys/prctl.h>

char str_sleep[] = "/usr/bin/sleep";
static char *argv_sleep[] = {"sleep", "30"};
char str_stress_ng[] = "/usr/bin/stress-ng";
static char *argv_stress_ng[] = {"stress-ng", "--matrix", "0", "-t", "30s"};

const int PR_SCHED_CORE = 62;
const int PR_SCHED_CORE_GET = 0;
const int PR_SCHED_CORE_CREATE = 1;
const int PR_SCHED_CORE_SHARE_TO = 2;
enum pid_type {PIDTYPE_PID = 0, PIDTYPE_TGID, PIDTYPE_PGID};

int main(int argc, char *argv[]) {
	unsigned long long cookie = 0;
	int prctl_ret;
	int ret = EXIT_SUCCESS;
	int option = 0;
	pid_t pid=fork();

	if (argc == 2 && strcmp(argv[1], "stress-ng") == 0) {
		option = 1;
	}

	if (pid == 0) { /* Child Process */
		/* Wait a little for the parent process to set the child process
		to a coregroup */
		usleep(1000);
		if (option == 1) {
			printf("Stress-ng Test!\n");
			execv(str_stress_ng, argv_stress_ng);
		} else {
			printf("Quick Sleep Test!\n");
			execv(str_sleep, argv_sleep);
		}
		printf("Should not get here! Execv failure!\n");
		exit(127); /* only if execv fails */
	} else { /* Parent Process */
		/* PID=TID when there is only one thread for a process */
		prctl_ret = prctl(PR_SCHED_CORE, PR_SCHED_CORE_CREATE, pid,
				  PIDTYPE_TGID, 0); // ret < 0
		if (prctl_ret) {
			printf("core_sched create failed -- TGID\n");
			printf("%i\n", prctl_ret);
			ret = -1;
			goto end_label;
		}
		prctl_ret = prctl(PR_SCHED_CORE, PR_SCHED_CORE_GET, pid, PIDTYPE_PID,
			(unsigned long)&cookie);
		if (prctl_ret) {
			printf("core_sched get cookie failed -- TGID\n");
			printf("%i\n", prctl_ret);
			ret = -1;
			goto end_label;
		}
		printf("Cookie Value: %llu\n", cookie);
		if (cookie <= 0) {
			printf("Bad Cookie\n");
			ret = -1;
			goto end_label;
		}
		printf("Waiting for child process to finish!\n");
		waitpid(pid,0,0); /* wait for child to exit */
	}
end_label:
	return ret;
}
