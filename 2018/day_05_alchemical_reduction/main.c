#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BIG_ARRAY_SIZE 0x10000
char input[BIG_ARRAY_SIZE];
char big_array[BIG_ARRAY_SIZE];
char big_array_alt[BIG_ARRAY_SIZE];

int filter(char *out, char* in, int size)
{
        int i = 0; /* Index that runs through all elements of "in". */
        int j = 0; /* Index of the first empty square of "out". */
        while(i < size-1) {
                if ( abs(in[i+1] - in [i]) == abs('A' - 'a')) {
                        /* Pair collapses. */
                        i += 2;
                }
                else {
                        out[j] = in[i];
                        j += 1;
                        i += 1;
                }
        }
        /* Copy the left-overs. */
        if (i == size - 1) {
                out[j] = in[i];
                j += 1;
        }

        return j;
}

int p1(char *input, int size)
{
        memcpy(big_array, input, size);
        char *in = big_array;
        char *out = big_array_alt;
        char *tmp;
        int len = size;
        int len_alt = 0;
        int len_tmp = 0;
        while (len != len_alt) {
                len_alt = filter(out, in, len);
                /* Alternate. */
                tmp = out;
                out = in;
                in = tmp;
                len_tmp = len_alt;
                len_alt = len;
                len = len_tmp;
        }
        return len;
}

int p1_char(char c, char *input, int size)
{
        int i = 0;
        int j = 0;

        /* Copy input to big_array by removing c and c +abs('a' - 'A') */
        for (i=0; i<size; i++) {
                if (input[i] != c && input[i] != c + abs('A' - 'a')) {
                        big_array[j] = input[i];
                        j += 1;
                }
        }
        return p1(big_array, j);
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
        FILE *f = NULL;
        int cnt;

        /******** Fetch input */
        if (argc != 2) {
                fprintf(stderr, "usage: ./main <input>\n");
                exit(EXIT_FAILURE);
        }

        if ( (f = fopen(argv[1], "r")) == NULL) {
                printf("burn in hell\n");
        }

        cnt = fread(input, 1, sizeof(big_array), f);
        if (cnt == sizeof(big_array)) {
                printf("big_array is not big enough.\n");
        }

        /* Beware of the trailing "\n" character! */
        printf("P1: %d\n", p1(input, cnt-1));
        printf("P2: %d\n", p2(input, cnt-1));
        return 0;
}
