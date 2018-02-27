#include <fstream>
#include <iostream>
#include <string>
#include <tuple>

std::tuple<int, int> cnt(const std::string& s)
{
	int floor = 0;
	int pos = -1;
	for (const char& c : s) {
		if (c == '(') {
			floor++;
		}
		if (c == ')') {
			floor--;
		}

		if ((pos == -1) && (floor == -1)) {
			pos = &c - &s[0];
			pos += 1;
		}
	}
	return std::make_tuple(floor, pos);
}

int main(void)
{
	std::string line;
	std::ifstream infile("input"); /* Get an input file stream object */
	std::getline(infile, line);    /* Get the first line of the ifsream in line */

	std::tuple<int, int> tuple = cnt(line);
	std::cout << "Part1: " << std::get<0>(tuple) << std::endl;
	std::cout << "Part2: " << std::get<1>(tuple) << std::endl;
	return 0;
}

