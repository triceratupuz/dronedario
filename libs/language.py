'''
definitions
; - groups division

(1  2 3...)v p m
55v p n

v - volume - float
p - pan - float
m - modulator - int -index for list item
t - action time - under development
'''


def toFloat(str):
	try:
		f = float(str)
		return True
	except ValueError:
		#print "excemption"
		return False
	

def dictsequence(dict):
	'''gives a list of dictionay keys sorted by value'''
	lista = sorted(dict, key=lambda x : dict[x]) 
	return lista


def findPar(strpar, sortedkeys, pos,group):
	strpar_index = sortedkeys.index(strpar)
	retv = -1
	retvs = ''
	if pos[strpar] > -1:
		if strpar_index == (len(sortedkeys) - 1):
			retvs = group[pos[strpar] + 1:]
		else:
			retvs = group[pos[strpar] + 1:pos[sortedkeys[strpar_index + 1]]]
	if toFloat(retvs):
		retv = float(retvs)
	else:
		retv = -1
	#print "par: %s val %f" % (strpar, retv)
	return retv


def groupInst(group):
	options =["(", ")", "v", "p", "m","t"]
	#parameters=["instrs", "vol", "pan", "mod"]
	pos ={}
	for item in options:
		#print item
		pos[item] = group.find(item)
	#sorted keys by value
	sortedkeys = dictsequence(pos)
	#find instr
	if pos["("] < pos[")"]:#well formed list of instrs
		inst_str = group[pos["("] + 1:pos[")"]].split()
	else:
		inst_str = [-1]
	vol = findPar("v", sortedkeys, pos, group)
	pan = findPar("p", sortedkeys, pos, group)
	mod = findPar("m", sortedkeys, pos, group)
	time = findPar("t", sortedkeys, pos, group)
	actionsG =[]
	for item in inst_str:
		actionsG.append([int(item), float(vol), float(pan), int(mod), float(time)])
	return actionsG



def divideGroups(string):
	groups = string.split(";")
	actions =[]
	for group in groups:
		for item in groupInst(group):
			if item[0] <> -1:
				actions.append(item)
	return actions






if __name__ == '__main__':
	sttt = "(55 38) p 0.3m7;(48)1k7p12t12;Commento;(81v0.8m6"
	print divideGroups(sttt)