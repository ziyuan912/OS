#include <linux/ktime.h>
#include <linux/linkage.h>
#include <linux/kernel.h>

asmlinkage long sys_GET_TIME(unsigned long *sec, unsigned long *nsec)
{
	struct timespec now;
	getnstimeofday(&now);
	*sec = now.tv_sec;
	*nsec = now.tv_nsec;
	return 0;
}
