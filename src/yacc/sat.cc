#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<map>

using namespace std;

struct action {
	char a; // can be 's' or 'r' or 'a', 'a' == "acc"
	int s;
};

typedef map<string, action> actions_t;
typedef map<string, int> goto_t;

struct ptrow {
	actions_t action_table;
	goto_t goto_table;
};

typedef vector<ptrow> parsing_table_t;

struct production {
	string left;
	vector<string> right;
};

ostream &operator<<(ostream &os, const production &p) {
	os << p.left << " -> ";
	for(string s: p.right) os << s << ' ';
	return os;	   
}

int parse(vector<production> &productions, parsing_table_t &table, vector<string> &sentence) {
	vector<int> state_stack;
	vector<string> char_stack;
	state_stack.push_back(0);
	char_stack.push_back("$");
	sentence.push_back("$");
	int input_p = 0;
	while(1) {
		actions_t &action_table = table[state_stack.back()].action_table;
		string &input = sentence[input_p];
		if(action_table.find(input) == action_table.end()) {
			cout << "Invalid sentence!\n";
			return -1;
		}
		action &ac = action_table[input];
		switch(ac.a) {
			case 'a':
				cout << "Accepted.\n";
				return 0;
			case 's':
				state_stack.push_back(ac.s);
				char_stack.push_back(input);
				input_p++;
				break;
			case 'r':
				{
					production &p = productions[ac.s];
					state_stack.erase(state_stack.end() - p.right.size(), state_stack.end());
					char_stack.erase(char_stack.end() - p.right.size(), char_stack.end());
					goto_t &goto_table = table[state_stack.back()].goto_table;
					if(goto_table.find(p.left) == goto_table.end()) {
						cout << "Error!\n";
						return -1;
					}
					state_stack.push_back(goto_table[p.left]);
					char_stack.push_back(p.left);
					cout << p << endl;
					break;
				}
			default:
				cout << "Inner Error: action " << ac.a << " is invalid.\n";
				return -2;
		}
	}
}

int main(int argc, char** argv) {
	if(argc < 2) {
		cerr << "No input file!\n";
		return -1;
	}
	// get input tokens/sentence
	ifstream fin(argv[1]);
	vector<string> sentence;
	while(fin) {
		string token;
		fin >> token;
		if(token.length() > 0) {
			sentence.push_back(token);
		}
	}
	// init productions and parsing table
	vector<production> productions;
	parsing_table_t table;
	// *insert point for python*

	// parsing and output reduction list
	parse(productions, table, sentence);
	return 0;
}
