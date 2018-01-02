#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
	int i;
	int j;
	double double_sqrt;
	int integer_sqrt;
	int cnt = 0;
	int inc;
	for(i=106700; i<= 123700; i+=17){
		inc = 0;
		double_sqrt = sqrt(i);
		integer_sqrt = (int)double_sqrt;
		for(j=2; j < integer_sqrt; j++)
			if(i%j == 0){
				inc = 1;
				break;
			}
		if(inc)
			cnt += 1;
	}
	printf("cnt:%d\n", cnt);
}
