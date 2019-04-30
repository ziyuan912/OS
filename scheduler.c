#include "schedular.h"
#include <stdlib.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sched.h>

static int isRunning;

int cmp(const void *a, const void *b) {
    return ((struct process *)a)->ready_time - ((struct process *)b)->ready_time;
}

int next_process(struct process *processes, int processnum, int schpolicy) {
    if (isRunning != -1 && schpolicy == SJF)
        return isRunning;

    int next = -1;

    if (schpolicy == SJF) {
        for (int i = 0; i < processnum; i++) {
	    if (processes[i].pid == -1 || processes[i].exec_time == 0)
	        continue;
	    if (next == -1 || processes[i].exec_time < processes[next].exec_time)
		next = i;
	}
    }

    return next;
}

int schedule(struct process *processes, int processnum, int schpolicy) {
    qsort(processes, processnum, sizeof(struct process), cmp);

    for (int i = 0; i < processnum; i++)
	processes[i].pid = -1;
}
