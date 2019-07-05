#include <linux/kernel.h>
#include <linux/linkage.h>

asmlinkage int mycall(char * msg){
	printk("%s",msg);
	return 0;
}
