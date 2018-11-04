// This file is generated from `lex.py` using template `lat.cc`. 
// DO NOT MODIFY.
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
	s0 = 0;
	F[28] = "test0";
	F[29] = "yakumo";
	F[30] = "test1";
	F[31] = "key";
	F[33] = "hakurei";
	F[34] = "kirisame";
	F[35] = "test2";
	F[32] = "key";
	F[36] = "kero";
	map<char,int> m0;
	m0['a'] = 1;
	m0['b'] = 3;
	m0['k'] = 5;
	m0['m'] = 8;
	m0['x'] = 28;
	m0['y'] = 28;
	m0['z'] = 9;
	m0['1'] = 29;
	move.push_back(m0);
	map<char,int> m1;
	m1['a'] = 4;
	m1['b'] = 10;
	m1['c'] = 11;
	m1['d'] = 12;
	move.push_back(m1);
	map<char,int> m2;
	m2['a'] = 4;
	m2['b'] = 2;
	m2['c'] = 11;
	m2['d'] = 12;
	move.push_back(m2);
	map<char,int> m3;
	m3['a'] = 4;
	m3['b'] = 3;
	move.push_back(m3);
	map<char,int> m4;
	m4['a'] = 4;
	m4['b'] = 19;
	move.push_back(m4);
	map<char,int> m5;
	m5['a'] = 13;
	m5['e'] = 14;
	move.push_back(m5);
	map<char,int> m6;
	m6['a'] = 25;
	m6['e'] = 26;
	move.push_back(m6);
	map<char,int> m7;
	m7['a'] = 27;
	m7['e'] = 21;
	move.push_back(m7);
	map<char,int> m8;
	m8['a'] = 15;
	m8['e'] = 16;
	m8['m'] = 8;
	m8['s'] = 17;
	m8['t'] = 17;
	move.push_back(m8);
	map<char,int> m9;
	m9['x'] = 30;
	m9['y'] = 30;
	m9['z'] = 18;
	move.push_back(m9);
	map<char,int> m10;
	m10['a'] = 4;
	m10['b'] = 31;
	m10['c'] = 11;
	m10['d'] = 12;
	move.push_back(m10);
	map<char,int> m11;
	m11['b'] = 11;
	m11['c'] = 11;
	m11['d'] = 12;
	move.push_back(m11);
	map<char,int> m12;
	m12['d'] = 12;
	m12['e'] = 33;
	move.push_back(m12);
	map<char,int> m13;
	m13['e'] = 20;
	m13['i'] = 22;
	move.push_back(m13);
	map<char,int> m14;
	m14['k'] = 6;
	m14['r'] = 23;
	m14['1'] = 29;
	move.push_back(m14);
	map<char,int> m15;
	m15['a'] = 15;
	m15['e'] = 16;
	m15['s'] = 17;
	m15['t'] = 17;
	move.push_back(m15);
	map<char,int> m16;
	m16['r'] = 34;
	move.push_back(m16);
	map<char,int> m17;
	m17['e'] = 16;
	m17['s'] = 17;
	m17['t'] = 17;
	move.push_back(m17);
	map<char,int> m18;
	m18['x'] = 35;
	m18['y'] = 35;
	move.push_back(m18);
	map<char,int> m19;
	m19['a'] = 4;
	m19['b'] = 32;
	move.push_back(m19);
	map<char,int> m20;
	m20['r'] = 24;
	move.push_back(m20);
	map<char,int> m21;
	m21['r'] = 23;
	move.push_back(m21);
	map<char,int> m22;
	m22['i'] = 22;
	m22['k'] = 6;
	m22['1'] = 29;
	move.push_back(m22);
	map<char,int> m23;
	m23['o'] = 36;
	move.push_back(m23);
	map<char,int> m24;
	m24['u'] = 36;
	move.push_back(m24);
	map<char,int> m25;
	m25['i'] = 22;
	move.push_back(m25);
	map<char,int> m26;
	m26['k'] = 6;
	m26['1'] = 29;
	move.push_back(m26);
	map<char,int> m27;
	m27['e'] = 20;
	move.push_back(m27);
	map<char,int> m28;
	move.push_back(m28);
	map<char,int> m29;
	m29['1'] = 29;
	move.push_back(m29);
	map<char,int> m30;
	move.push_back(m30);
	map<char,int> m31;
	m31['a'] = 4;
	m31['b'] = 2;
	m31['c'] = 11;
	m31['d'] = 12;
	move.push_back(m31);
	map<char,int> m32;
	m32['a'] = 4;
	m32['b'] = 3;
	move.push_back(m32);
	map<char,int> m33;
	m33['e'] = 33;
	move.push_back(m33);
	map<char,int> m34;
	m34['r'] = 34;
	move.push_back(m34);
	map<char,int> m35;
	move.push_back(m35);
	map<char,int> m36;
	m36['k'] = 7;
	move.push_back(m36);
	// analyze
	for(string &w: words) {
		token *t = simulateDfa(s0, F, move, w);
		cout << '(' << t->cate << ',' << t->word << ')' << endl;
	}
	return 0;
}
