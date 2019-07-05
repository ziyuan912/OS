#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sched.h>
#include <errno.h>
#include <unistd.h>
#include "processer.h"
#include "schedule.h"
#include <linux/kernel.h>
int main()
{
	char policy[50];
	int processnum;
	int schpolicy;

	scanf("%s", policy);
	scanf("%d", &processnum);
	struct process *processes = (struct process *)malloc(sizeof(struct process)*processnum);
	for(int i = 0;i < processnum;i ++)
		scanf("%s %d %d",processes[i].name, &processes[i].ready_time, &processes[i].exec_time);
	if(strcmp(policy, "FIFO") == 0)schpolicy = 0;
	else if(strcmp(policy, "RR") == 0)schpolicy = 1;
	else if(strcmp(policy, "SJF") == 0)schpolicy = 2;
	else if(strcmp(policy, "PSJF") == 0)schpolicy = 3;
	else{
		fprintf(stderr, "bad policy!\n");
		exit(0);
	}
	scheduler(processes, processnum, schpolicy);
	return 0;
}
