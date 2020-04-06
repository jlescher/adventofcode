#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <set>
#include <tuple>
#include <algorithm>
#include <assert.h>

using namespace std;

template <typename T>
void print_vector(const T& t) {
	cout << "vector: ";
	for(auto v: t) {
		cout << v << " "; 
	}
	cout << endl;
}

int deliver(string s)
{
	auto cur_pos = make_tuple(0, 0);
	set<tuple<int, int>> pos;
	pos.insert(cur_pos); /* Copy ?? */
	for(auto dir: s){
		/* Move. */
		switch(dir) {
			case '<':
				std::get<0>(cur_pos) -= 1;
				break;
			case '>':
				std::get<0>(cur_pos) += 1;
				break;
			case 'v':
				std::get<1>(cur_pos) -= 1;
				break;
			case '^':
				std::get<1>(cur_pos) += 1;
				break;
		}
		/* Add. */
		pos.insert(cur_pos); /* Copy ?? */
	}
	return pos.size();
}


int main(void)
{
	assert(deliver(">") == 2);
	assert(deliver("^>v<") == 4);
	assert(deliver("^v^v^v^v^v") == 2);

	string line;
	ifstream infile("input");
	getline(infile, line);

	cout << "Part1: " << deliver(line) << endl;
}

