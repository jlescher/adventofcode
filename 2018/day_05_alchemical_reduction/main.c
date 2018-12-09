#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void  add(char* stack, int *i, char c) {
        if (*i > 0 && abs(stack[(*i) - 1] - c) == abs('A' - 'a')) {
                        *i -= 1;
        }
        else {
                stack[*i] = c;
                *i += 1;
        }
}

int p1(char *in, int sz)
{
        int i = 0;
        int j = 0;
        char * stack;

        stack = malloc(sz*sizeof(char));
        if (stack == NULL) {
                fprintf(stderr, "Cannot malloc\n");
                exit(EXIT_FAILURE);
        }

        for(j = 0; j < sz; j++) {
                add(stack, &i, in[j]);
        }

        return i;
}


int p1_char(char c, char *in, int sz)
{
        char *buf;
        int i;
        int j = 0;

        buf = malloc(sz*sizeof(char));
        if (buf == NULL) {
                fprintf(stderr, "Cannot malloc\n");
                exit(EXIT_FAILURE);
        }
        /* Copy in to big_array by removing c and c +abs('a' - 'A') */
        for (i=0; i<sz; i++) {
                if (in[i] != c && in[i] != c + abs('A' - 'a')) {
                        buf[j] = in[i];
                        j += 1;
                }
        }
        return p1(buf, j);
}

int p2(char *input, int size)
{
        int i = 0;
        int min;
        int mini;
        int letters[26] = {0};

        /* Get which letters are in the string. */
        for (i=0; i<size; i++) {
                if ('A' <= input[i] && input[i] <= 'Z') {
                        letters[input[i]-'A'] = 1;
                }
                else if ('a' <= input[i] && input[i] <= 'z') {
                        letters[input[i]-'a'] = 1;
                }
                else {
                        printf("Something went wrong.\n");
                }
        }

        /* Get min(p1_char(X)). */
        min = -1;
        for (i=0; i<26; i++) {
                if (letters[i] == 1) {
                        mini = p1_char('A'+i, input, size);
                        if (min == -1) {
                                min = mini;
                        }
                        else if (mini < min) {
                                min = mini;
                        }
                }
        }
        return min;
}

int main(int argc, char* argv[])
{
        FILE *fp = NULL;
        char *in;
        int sz;
        int r_sz;

        /******** Fetch input */
        if (argc != 2) {
                fprintf(stderr, "usage: ./main <input>\n");
                exit(EXIT_FAILURE);
        }

        if ( (fp = fopen(argv[1], "r")) == NULL) {
                printf("burn in hell\n");
        }

        fseek(fp, 0L, SEEK_END);
        sz = ftell(fp);
        sz -= 1; /* New line. */
        rewind(fp);

        in = malloc(sz*sizeof(char));
        if (in == NULL) {
                fprintf(stderr, "Cannot malloc\n");
                exit(EXIT_FAILURE);
        }

        r_sz = fread(in, 1, sz, fp);
        if (sz != r_sz) {
                fprintf(stderr, "Cannot read input\n");
                exit(EXIT_FAILURE);
        }

        /* Beware of the trailing "\n" character! */
        printf("P1: %d\n", p1(in, sz));
        printf("P2: %d\n", p2(in, sz));
        return 0;
}
