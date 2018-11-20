# global variables
empty = ''
start = 'S'
grammar = None

'''
Attention: for epsilon production, the right part is an empty tuple.
'''
class production:
    # left: str, right: tuple of str
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, p):
        return self.left == p.left and self.right == p.right

    def __hash__(self):
        return hash(self.left) ^ hash(self.right)
    
    def __str__(self):
        return self.left + ' -> ' + ' '.join(self.right)

    def isEmpty(self):
        return len(self.right) == 0

class lr1_grammar:
    '''
    p_list: list of production, s_start(symbol of start): str, 
    terminals & non_terminals: set of str
    '''
    def __init__(self, p_list, s_start, terminals, non_terminals):
        self.start = production(start, (s_start))
        self.p_list = [self.start] + p_list
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.__first()
        # self.__follow()
        pass

    def __iter__(self):
        return iter(self.p_list)

    def __getitem__(self, index):
        return self.p_list[index]

    def index(self, p):
        return self.p_list.index(p)
    '''
    Initialize the FIRST table for all symbols.
    '''
    def __first(self):
        # first_table: {str => set(str)}
        self.first_table = {c: set() for c in self.terminals | self.non_terminals} 
        for t in self.terminals:
            self.first_table[t].add(t)
        updated = True
        while updated:
            updated = False
            for p in self.p_list[1:]:
                updated |= self.__first_of(p)
        pass
    '''
    Calculate the incomplete FIRST sets out of a production.
    Return whether the FIRST sets have been updated.
    '''
    def __first_of(self, p):
        updated = False
        first_set = self.first_table[p.left]
        if p.isEmpty():
            if empty not in first_set:
                first_set.add(empty)
                updated = True
        else:
            for symbol in p.right:
                if symbol in self.terminals:
                    if symbol not in first_set:
                        first_set.add(symbol)
                        updated = True
                    break
                else:
                    for s in self.first_table[symbol]:
                        if s != empty and s not in first_set:
                            first_set.add(s)
                            updated = True
                    if empty not in self.first_table[symbol]:
                        break
        return updated
    '''
    Calculate the FIRST of an expression.
    expr: list of str
    '''
    def first_of(self, expr):
        if len(expr) == 0:
            return {empty}
        result = set()
        for s in expr:
            result |= self.first_table[s]
            if empty not in self.first_table[s]:
                result -= {empty}
                break
        return result

class lr1_item:
    '''
    p: production, n: int, lastr: set of str
    n stands for the position of the dot in a production
    '''
    def __init__(self, p, n, lastr):
        self.p = p
        self.n = n
        self.lastr = lastr
        pass
    
    def __eq__(self, item):
        return self.p == item.p and self.n == item.n and self.lastr == item.lastr

    def __str__(self):
        return str(self.p) + ', ' + str(self.n) + ', ' + '|'.join(self.lastr)

    def core(self):
        return (self.p, self.n)

    def p_index(self):
        return grammar.index(self.p)

    '''
    Next symbol behinds the dot.
    '''
    def next_s(self):
        if not self.can_move():
            return None
        return self.p.right[self.n]
    '''
    Expression behind the next symbol.
    '''
    def next_expr(self):
        if not self.can_move():
            return None
        return self.p.right[self.n + 1:]
    '''
    Whether the dot has come to the end.
    '''
    def can_move(self):
        return self.n < len(self.p.right)
    '''
    Generate a new LR(1) item by moving the dot behind one symbol.
    '''
    def one_move(self):
        if not self.can_move():
            return None
        p = self.p
        n = self.n + 1
        lastr = self.lastr
        return lr1_item(p, n, lastr)

class lr1_itemset:
    '''
    init: list of lr1_item
    '''
    def __init__(self, init):
        self.items = init
        self.__extend()
        pass

    def __iter__(self):
        return iter(self.items)

    def __eq__(self, s):
        return self.items == s.items

    def __str__(self):
        return '\n'.join([str(item) for item in self.items])
    '''
    Extend the item set by Algorithm 4.53
    '''
    def __extend(self):
        queue = list(self.items)
        while len(queue) > 0:
            item = queue.pop(0)
            if not item.can_move():
                continue
            symbol = item.next_s()
            if symbol not in grammar.non_terminals:
                continue
            for p in (i for i in grammar if i.left == symbol):
                first = grammar.first_of(item.next_expr())
                if empty in first:
                    first -= {empty}
                    first |= set(item.lastr)
                new_item = lr1_item(p, 0, first)
                if self.__merge(new_item):
                    queue.append(new_item)
        pass
    '''
    Trying to merge, and if duplicated, return false; else return true.
    '''
    def __merge(self, item):
        for it in self.items:
            if it == item:
                return False
            if it.core() == item.core():
                more = item.lastr - it.lastr
                if len(more) == 0:
                    return False
                it.lastr |= more
                return True
        self.items.append(item)
        return True

class lr1_stm:
    def __init__(self):
        self.states = [lr1_itemset([lr1_item(grammar.start, 0, {'$'})])]
        self.moves = [] # list of {str => int}
        i = 0
        while i < len(self.states):
            self.__move_from(i)
            i += 1
        pass

    def __str__(self):
        result = ''
        for i in range(0, len(self.states)):
            result += str(i) + '\n' + str(self.states[i]) + '\n\n'
        result += str(self.moves)
        return result
    '''
    i_state: index of a state
    '''
    def __move_from(self, i_state):
        state = self.states[i_state]
        init_items = {} # str => set of lr1_item
        for item in (i for i in state if i.can_move()):
            symbol = item.next_s()
            if symbol in init_items:
                init_items[symbol].append(item.one_move())
            else:
                init_items[symbol] = [item.one_move()]
        self.moves.append({}) # str => int
        for symbol, items in init_items.items():
            itemset = lr1_itemset(items)
            if itemset in self.states:
                self.moves[i_state][symbol] = self.states.index(itemset)
            else:
                self.moves[i_state][symbol] = len(self.states)
                self.states.append(itemset)
        pass

'''
Get input grammar from a file and return whether the input succeeded.
'''
def input_grammar(filename):
    global grammar
    with open(filename, 'r', encoding='utf8') as f:
        t_set = set(f.readline().split())
        nont_set = set(f.readline().split())
        if len(t_set & nont_set) > 0:
            print('Terminals and Nonterminals have same symbol. Check it please.')
            return False
        s_start = f.readline().split()[0]
        if s_start not in nont_set:
            print('The start symbol is not a nonterminal. Check it please.')
            return False
        line_n = 3
        productions = []
        while True:
            line_str = f.readline().strip('\n')
            if line_str == '':
                break
            line_n += 1
            line = line_str.split()
            invalid_ids = [s for s in line if s not in t_set | nont_set]
            if len(invalid_ids) > 0:
                print('Undefined identifiers: %s' % invalid_ids)
                return False
            productions.append(production(line[0], tuple(line[1:])))
        if len(productions) == 0:
            print('No productions.')
            return False
        grammar = lr1_grammar(productions, s_start, t_set, nont_set)
    return True

'''
Construct LR(1) Parsing table by stm into an output .cc file.
'''
def construct_lr1pt(stm, filename):
    outstr = ''
    # prepare productions
    i = 0
    for p in grammar:
        outstr += '\tvector<string> right%s;\n' % i
        for s in p.right:
            outstr += '\tright%s.push_back("%s");\n' % (i, s)
        outstr += '\tproductions.push_back({"%s", right%s});\n' % (p.left, i)
        i += 1
    outstr += '\n'
    # prepare table entries
    i = 0
    for s in range(0, len(stm.states)):
        outstr += '\tactions_t at%s;\n\tgoto_t gt%s;\n' % (i, i)
        for symbol,n in stm.moves[s].items():
            if symbol in grammar.terminals:
                outstr += '\tat%s["%s"] = {\'s\', %s};\n' % (i, symbol, n)
            else:
                outstr += '\tgt%s["%s"] = %s;\n' % (i, symbol, n)
        for item in stm.states[s]:
            if item.can_move():
                continue
            if item.p == grammar.start:
                outstr += '\tat%s["$"] = {\'a\', 0};\n' % i
                continue
            p_i = item.p_index()
            for c in item.lastr:
                outstr += '\tat%s["%s"] = {\'r\', %s};\n' % (i, c, p_i)
        outstr += '\ttable.push_back({at%s, gt%s});\n' % (i, i)
        i += 1
    # generate .cc file
    with open('sat.cc', 'r', encoding='utf8') as sat, \
            open(filename, 'w', encoding='utf8') as fout:
        fout.write('// This file is generated from `syn.py` using template `sat.cc`. \n')
        fout.write('// DO NOT MODIFY IT. \n')
        flag = '// *insert point for python*'
        for line in list(sat):
            fout.write(line)
            if flag in line:
                fout.write(outstr)
    pass

if __name__ == '__main__':
    if input_grammar('grammar.txt'):
        stm = lr1_stm()
        construct_lr1pt(stm, 'syn.cc')
    else:
        print('Input failed!')
