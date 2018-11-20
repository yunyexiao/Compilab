/**
 * This file is a template for generating lexical analyser.
 * Do not modify it.
 */
#include<iostream>
#include<fstream>
#include<map>
#include<vector>
#include<string>

using namespace std;

typedef map<int, string> f_t;
typedef vector<map<char, int>> move_t;

struct token {
	string cate;
	string word;
};

token *simulateDfa(const int s0, f_t &F, move_t &move, const string &word) {
	int s = s0;
	for(char c: word) {
		if(move[s].find(c) == move[s].end()) {
			return new token{"None", word};
		}
		s = move[s][c];
	}
	if(F.find(s) != F.end()) {
		return new token{F[s], word};
	} else {
		return new token{"None", word};
	}
}

int main(int argc, char **argv) {
	if(argc < 2) {
		cout << "No input file! Please try again.\n";
		return -1;
	}
	// get input
	ifstream fin(argv[1]);
	vector<string> words;
	while(fin){
		string w;
		fin >> w;
		if(w.length() > 0) words.push_back(w);
	}
	// prepare dfa
	int s0;
	f_t F;
	move_t move;
	// *insert point for python*
	// analyze
	for(string &w: words) {
		token *t = simulateDfa(s0, F, move, w);
		cout << '(' << t->cate << ',' << t->word << ')' << endl;
	}
	return 0;
}
