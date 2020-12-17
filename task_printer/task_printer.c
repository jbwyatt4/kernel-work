#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("John B. Wyatt IV");
MODULE_DESCRIPTION("Prints the first 10 tasks reported by for_each_process()");
MODULE_VERSION("0.01");

static int __init mylkm_init(void) {
	struct task_struct *task;
	int i = 0;

	rcu_read_lock();
	for_each_process(task) {
		/* Prints the name and PID of each task  */
		if (i < 10) {
			printk("%s[%d]\n", task->comm, task->pid);
			i++;
		} else {
			return 0;
		}

	}
	rcu_read_unlock();

	return 0;
}

static void __exit mylkm_exit(void) {
	printk(KERN_INFO "BYE!\n");
}

module_init(mylkm_init);
module_exit(mylkm_exit);
