#include <stdio.h>
#include <stdlib.h>

/* Implement a circular list: i.e. chain the last element on the first one */

struct e {
	struct e *next;
	int i;
};


int run(struct e *head, struct e *ntbc, int num){
	struct e *free_e = NULL;
	while (num > 1) {
		free_e = ntbc->next;
		ntbc->next = ntbc->next->next;
		free(free_e) ; /* Dont care if it does not work */
		num -= 1;
		head = head->next;
		if ((num % 2) == 0) {
			ntbc = ntbc->next;
		}
	}
	return head->i;
}

int main(int argc, char* argv[])
{
	int num;
	int i;

	/* Malloc as many e struct as necessary */
	struct e *head = NULL;            /* Current element of the circular buffer */
	struct e *next_to_be_canceled = NULL;  /* Element before the one that should be canceled */ 
	struct e *prev = NULL;
	struct e *cur  = NULL;

	if (argc != 2) {
		fprintf(stderr, "usage: ./main <num>\n");
		exit(EXIT_FAILURE);
	}
	num = atoi(argv[1]);

	for (i=1; i<=num; i++) {
		cur = malloc(sizeof(struct e));
		if (cur == NULL) { 
			fprintf(stderr, "malloc failure, cannot recover\n");
			exit(EXIT_FAILURE);
		}
		cur->i = i;

		/* Chain */
		if (prev != NULL) {
			prev->next = cur;
		}
		else { /* prev == NULL => first element */
			head = cur;
		}
		prev = cur;

		if (i == num/2) {
			next_to_be_canceled = cur;
		}
	}
	/* Chain on first element */
	cur->next = head;

	printf("P2: %d\n", run(head, next_to_be_canceled, num));
}
