#ifndef _PROCESS_H_
#define _PROCESS_H_

#include <sys/types.h>
#include <linux/kernel.h>

#define CHILD_CPU 1
#define PARENT_CPU 0

struct process {
	char name[32];
	int ready_time;
	int exec_time;
	pid_t pid;
};

int proc_assign_cpu(int pid, int core);

int proc_exec(struct process proc);

int proc_block(int pid);

int proc_wakeup(int pid);

void UNIT_T();

#endif
