def get_input(filename):
    f = open(filename, 'r', encoding='utf-8')
    line = f.readline().strip('\n').replace(' ', ',').replace('\t', ',')
    alphabet = line.split(',')
    for c in alphabet:
        if len(c) > 1:
            print('Alphabet is wrong.')
            return None
    rules = {}
    while True:
        line = f.readline().strip('\n')
        if line == '':
            break
        k = line.find('\t')
        if k == -1:
            print('Rule is wrong: ' + line)
            return None
        cate = line[:k]
        re = line[(k+1):]
        if cate in rules.values():
            print('The category is duplicated: ' + cate)
            return None
        if re in rules.keys():
            print('The regular expression is duplicated: ' + re)
            return None
        rules[re] = cate
    return alphabet, rules

def preprocess(alphabet, re):
    re = re.replace(' ', '').replace('\t', '')
    expr = ''
    flag = True # whether the char before the next char is '|' or '(' or '&'
    for c in re:
        if c in alphabet or c == '(':
            if not flag:
                expr += '&'
            expr += c
            flag = c == '('
        elif c == '|' or c == '&':
            if flag:
                print('Wrong regular expression: ' + re)
                return None
            expr += c
            flag = True
        elif c == ')' or c == '*':
            expr += c
            flag = False
        else:
            print('Char not in alphabet: ' + c + ' in RE: ' + re)
            return None
    return expr

def infix2postfix(re):
    stack = []
    priority = {'|': 1, '&': 2, '*': 3}
    postfix = ''
    re = '(' + re + ')'
    for c in re:
        if c in priority.keys():
            while stack[-1] != '(' and priority[stack[-1]] >= priority[c]:
                postfix += stack.pop()
            stack.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            postfix += c
    if len(stack) > 0:
        return None
    return postfix

def postfix2nfa(start_s, postfix):
    stack = []
    state_n = start_s # the next number to be taken by the next state
    for c in postfix:
        if c == '&':
            latter = stack.pop()
            former = stack.pop()
            former[2] += latter[2] + [(former[1], latter[0], '')]
            former[1] = latter[1]
            stack.append(former)
        elif c == '|':
            latter = stack.pop()
            former = stack.pop()
            left = state_n
            right = left + 1
            state_n = right + 1
            former[2] += latter[2]
            former[2] += [(left, former[0], ''), (left, latter[0], '')]
            former[2] += [(former[1], right, ''), (latter[1], right, '')]
            former[0] = left
            former[1] = right
            stack.append(former)
        elif c == '*':
            former = stack.pop()
            left = state_n
            right = left + 1
            state_n = right + 1
            former[2] += [(former[1], former[0], ''), (left, former[0], '')]
            former[2] += [(former[1], right, ''), (left, right, '')]
            former[0] = left
            former[1] = right
            stack.append(former)
        else:
            stack.append([state_n, state_n + 1, [(state_n, state_n + 1, c)]])
            state_n += 2
    return stack.pop()

def rule2nfa(alphabet, rule):
    s0 = 0
    F = {}
    edges = []
    state_n = s0 + 1
    for re in rule:
        fa = postfix2nfa(state_n, infix2postfix(preprocess(alphabet, re)))
        edges += fa[2] + [(s0, fa[0], '')]
        F[fa[1]] = rule[re]
        state_n = fa[1] + 1
    move = [{} for i in range(0, state_n)]
    for e in edges:
        if e[2] in move[e[0]].keys():
            move[e[0]][e[2]].add(e[1])
        else:
            move[e[0]][e[2]] = {e[1]}
    return s0, F, move

def eps_closure_s(s, move):
    result = set()
    queue = [s]
    while len(queue) > 0:
        result.add(queue[0])
        if '' in move[queue[0]].keys():
            for st in move[queue[0]]['']:
                if st not in result and st not in queue:
                    queue.append(st)
        queue.pop(0)
    return result

def eps_closure_T(T, move):
    result = set()
    for s in T:
        result |= eps_closure_s(s, move)
    return result

def nfa2dfa(alphabet, s0, F, move):
    states = [eps_closure_s(s0, move)]
    head = 0
    dtran = []
    while head < len(states):
        dtran.append({})
        for c in alphabet:
            # calculate the next state
            U = set()
            for s in states[head]:
                if c in move[s].keys():
                    U |= move[s][c]
            if len(U) == 0:
                continue
            U = eps_closure_T(U, move)
            # add into dtran table
            if U not in states:
                states.append(U)
            dtran[head][c] = states.index(U)
        head += 1
    # calculate final states
    final_state = {}
    Fset = set(F.keys())
    for s in states:
        intersection = s & Fset
        if len(intersection) > 0:
            final_state[states.index(s)] = F[list(intersection)[0]]
    return 0, final_state, dtran

def min_dfa(s0, F, move):
    # partition
    part = [list(range(0, len(move)) - F.keys()), list(F.keys())]
    weak_move = [{} for i in range(0, len(move))]
    while True:
        # calculate the weak_move table
        for i in range(0, len(move)):
            for k, v in move[i].items():
                weak_move[i][k] = [j for j in range(0, len(part)) if v in part[j]][0]
        # make new partition
        new_part = []
        for group in part:
            g_part = []
            for state in group:
                find = False
                for gg in g_part:
                    if weak_move[gg[0]] == weak_move[state]:
                        find = True
                        gg.append(state)
                        break
                if not find:
                    g_part.append([state])
            new_part += g_part
        # judge if new partition is the same as former partition
        if new_part == part:
            break
        else:
            part = new_part
    # construct the min dfa
    new_s0 = [i for i in range(0, len(part)) if s0 in part[i]][0]
    new_F = {}
    for (k, v) in F.items():
        new_F[[i for i in range(0, len(part)) if k in part[i]][0]] = v
    new_move = [weak_move[group[0]] for group in part]
    return new_s0, new_F, new_move

'''
This simulator is DEPRECATED now. See the `README.md` file in the 
same directory for more infomation.
'''
def dfa_simulate(s0, F, move, txt):
    s = s0
    for c in txt:
        if c not in move[s].keys():
            return (None, txt)
        s = move[s][c]
    if s in F.keys():
        return (F[s], txt)
    else:
        return (None, txt)

def dfa2cc(s0, F, move, filename):
    # prepare str to output
    outstr = '\ts0 = %s;\n' % s0
    for k,v in F.items():
        outstr += '\tF[%s] = "%s";\n' % (k, v)
    i = 0
    for m in move:
        var = 'm' + str(i)
        outstr += '\tmap<char,int> %s;\n' % var
        for k,v in m.items():
            outstr += "\t%s['%s'] = %s;\n" % (var, k, v)
        outstr += '\tmove.push_back(%s);\n' % var
        i += 1
    # generate cc file
    flag = '// *insert point for python*'
    with open('lat.cc', 'r', encoding='utf-8') as lat, \
            open(filename, 'w', encoding='utf-8') as fout:
        fout.write('// This file is generated from `lex.py` using template `lat.cc`. \n// DO NOT MODIFY.\n')
        for line in list(lat):
            fout.write(line)
            if flag in line:
                fout.write(outstr)
    pass

if __name__ == '__main__':
    alphabet, rule = get_input('rules.txt')
    nfa_s0, nfa_F, nfa_move = rule2nfa(alphabet, rule)
    dfa_s0, dfa_F, dfa_move = nfa2dfa(alphabet, nfa_s0, nfa_F, nfa_move)
    dfa_s0, dfa_F, dfa_move = min_dfa(dfa_s0, dfa_F, dfa_move)
    dfa2cc(dfa_s0, dfa_F, dfa_move, 'lexical_analyser.cc')
'''
    f = open('input.txt', 'r', encoding='utf-8')
    for w in f.read().split():
        result = dfa_simulate(dfa_s0, dfa_F, dfa_move, w)
        print(result)
'''

