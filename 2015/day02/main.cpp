#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

template <typename T>
void print_vector(const T& t) {
	cout << "vector: ";
	for(auto v: t) {
		cout << v << " "; 
	}
	cout << endl;
}

int main(void)
{
	string line;
	ifstream infile("input");
	int wrap   = 0;
	int ribbon = 0;

	while (getline(infile, line)) {
		istringstream ss(line);
		vector<int> d;
		for(string each; getline(ss, each, 'x'); d.push_back(stoi(each))); /* Get the dimensions. */
		sort(d.begin(), d.end());
		wrap += 2 * (d[0]*d[1] + d[0]*d[2] + d[1]*d[2]) + d[0]*d[1];
		ribbon += 2 * (d[0] + d[1]) + d[0]*d[1]*d[2];
	}
	cout << "Part1: " << wrap << endl;
	cout << "Part1: " << ribbon << endl;

	return 0;
}

