f = open('solution.utm','r')
statecounter = 'DAA'
tapesymbol = {'b':'D','0':'DC','1':'DCC'}
states = {'start':'DA','HALT':'DH'}
final = []
for line in f.readlines():
    if '#' in line:
        continue
    if not line.strip('\n'):
        continue
    line = line.split(',')
    line = map(lambda x:x.strip(),line)
    state,read,write,direction,nextstate = line
    if state in states.keys():
        encstate = states[state]
    else:
        encstate = statecounter
        states[state] = encstate
        statecounter += 'A'
    encread = tapesymbol[read]
    encwrite = tapesymbol[write]
    if nextstate in states.keys():
        encnextstate = states[nextstate]
    else:
        encnextstate = statecounter
        states[nextstate] = encnextstate
        statecounter += 'A'
    line = ';'+encstate+encread+encwrite+direction.upper()+encnextstate
    final.append(line)


f = open('states','w')
f.write(str(states))
f.close()
f = open('solution','w')
f.write(''.join(final))
f.close()
