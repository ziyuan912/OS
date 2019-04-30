#include <stdlib.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sched.h>
#include "processer.h"
#include <linux/kernel.h>

static int isRunning;
static int time;
static int finish_ps;
static int t_switch;

int cmp(const void *a, const void *b) {
	int ready_a = ((struct process *)a)->ready_time;
	int ready_b = ((struct process *)b)->ready_time;
	if(ready_a > ready_b)return 1;
	else if(ready_a == ready_b)return 0;
	else return -1;
}

int FIFO(struct process *processes, int processnum, int time){
	int next = -1;
	if(isRunning != -1)return isRunning;
	else{
		for(int i = 0;i < processnum;i ++){
			if(processes[i].ready_time > time || processes[i].exec_time == 0)
				continue;
			else if(next == -1 || processes[i].ready_time < processes[next].ready_time)
				next = i;
		}
		return next;
	}
}

int SJF(struct process *processes, int processnum, int time)  {
	if (isRunning != -1) return isRunning;
	int next = -1;
	for (int i = 0; i < processnum; i++) {
		if (processes[i].ready_time > time || processes[i].exec_time == 0)
			continue;
		if (next == -1 || processes[i].exec_time < processes[next].exec_time)
				next = i;
	}
	return next;
}

int PSJF(struct process *processes, int processnum, int time)  {
	int next = -1;
	for (int i = 0; i < processnum; i++) {
		if (processes[i].ready_time > time || processes[i].exec_time == 0)
			continue;
		else if (next == -1 || processes[next].exec_time > processes[i].exec_time)
		{
				next = i;
		}
	}
	return next;
}

int RR(struct process *processes, int processnum, int time){
	int next = -1;
	 if (isRunning == -1) {
		for (int i = 0; i < processnum; i++)
		{
			if (processes[i].ready_time <= time && processes[i].exec_time > 0)
			{
				next = i;
				break;
			}
		}
	 }
	 else if ((time - t_switch) % 500 == 0)  {
		next = (isRunning + 1) % processnum;
		while (processes[next].ready_time > time || processes[next].exec_time == 0)
			next = (next+1) % processnum;
	 }
	 else next = isRunning;
 	return next;
}

int scheduler(struct process *processes, int processnum, int schpolicy) {
	qsort(processes, processnum, sizeof(struct process), cmp);

	isRunning = -1;
	time = 0;
	finish_ps = 0;
	t_switch = 0;
	if(finish_ps == processnum)return 0;
	proc_assign_cpu(getpid(), PARENT_CPU);
	proc_wakeup(getpid());
	for (int i = 0; i < processnum; i++){
		if(processes[i].exec_time == 0){
			finish_ps ++;
			continue;
		}
		processes[i].pid = proc_exec(processes[i]);
		proc_block(processes[i].pid);
	}
	while(1){
		if(isRunning != -1 && processes[isRunning].exec_time == 0){
			waitpid(processes[isRunning].pid, NULL, 0);
			printf("%s %d\n",processes[isRunning].name, processes[isRunning].pid );
			isRunning = -1;
			finish_ps += 1;
			if(finish_ps == processnum)break;
		}
		int next;
		switch(schpolicy){
			case 0:
				next = FIFO(processes, processnum, time);
				break;
			case 1:
				next = RR(processes, processnum, time);
				break;
			case 2:
				next = SJF(processes, processnum, time);
				break;
			case 3:
				next = PSJF(processes, processnum, time);
				break;
		}
		if(next != -1){
			if(isRunning == -1){
				proc_wakeup(processes[next].pid);
				t_switch = time;
			}
			else if(isRunning != next){
				proc_block(processes[isRunning].pid);
				proc_wakeup(processes[next].pid);
				t_switch = time;
			}
			isRunning = next;
		}
		UNIT_T();
		time ++;
		if(isRunning != -1){
			processes[isRunning].exec_time -= 1;
		}
	}
	return 0;
}
