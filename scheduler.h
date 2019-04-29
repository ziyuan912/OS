#define FIFO 0
#define RR 1
#define SJF 2
#define PSJF 3

int schedule(struct process *processes, int processnum, int schpolicy);
