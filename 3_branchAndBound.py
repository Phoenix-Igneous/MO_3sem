import copy

flEnd = False
base = set()
bbase = set()
answ = dict()


def printWithXInTable(tab):
	m = len(tab)
	n = len(tab[0])
	print()
	for i in range(m - 1):
		for j in range(n - 1):
			print('{:>7.2f}'.format(tab[i][j]), end="")
		pam = str(int(tab[i][-1]))
		if pam == "88":
			pam = "  F"
		elif pam == "99":
			pam = ""
		else:
			pam = "  X" + pam
		print(pam)
	for i in range(n):
		pam = str(int(tab[-1][i]))
		if pam == "77":
			pam = "  S"
		elif pam == "99":
			pam = ""
		else:
			pam = "  X" + pam
		print('{:>7s}'.format(pam), end="")
	print()


def printAnswer(n, flag, tab):
	if flag == "max":
		zn = -1
	else:
		zn = 1
	#print("\n" + "Answer:\n" + "F" + str(flag) + " = " + " " + '{:<9.3f}'.format(tab[-2][0] * zn))
	print("\n" + "Answer:\n" + "F" + " = " + " " + '{:<9.3f}'.format(tab[-2][0] * zn))
	le = len(bbase)
	pam = [0] * (le + 1)
	for i in range(le):
		pam[i] = 0
	m = len(tab)
	for i in range(m):
		if tab[i][-1] in bbase:
			pam[tab[i][-1]] = tab[i][0]
	for i in range(1, le + 1):
		print("X" + str(i) + " = " + '{:<7.2f}'.format(pam[i]))
	print()
	answ[tab[-2][0] * zn] = pam


def printOpor(tab):
	print("\n" + "Opor answer:\n" + "F" + " = " + " " + '{:<9.3f}'.format(-tab[-2][0]))
	n = len(bbase)
	pam = [0] * (n + 1)

	for i in range(n + 1):
		pam[i] = 0
	for i in range(len(tab)):
		if tab[i][-1] in bbase:
			pam[tab[i][-1]] = tab[i][0]
	for i in range(1, len(bbase) + 1):
		print("X" + str(i) + " = " + '{:<7.2f}'.format(pam[i]))

	answ[tab[-2][0] * (-1)] = pam
	print()
	print(*answ)


def createSimplexTable(flag, n, a, b, c):
	tab = [[0] * (n + 2) for i in range(n + 2)]
	if flag == "max":
		flag = 1
	else:
		flag = -1
	for i in range(n):
		tab[i][0] = b[i] * flag
		for j in range(1, n + 1):
			tab[i][j] = a[i][j - 1] * flag
		tab[n][i + 1] = flag * c[i]  # +-
	tab[n][0] = 0  # F(s)
	for i in range(n + 1):
		tab[i][n + 1] = i + n + 1
		tab[n + 1][i] = i
	tab[n + 1][0] = 77  # S
	tab[n][n + 1] = 88  # F
	tab[n + 1][n + 1] = 99  # empty
	return tab


def findOpor(tabA):
	#print("Start opor")
	kol = 0
	m = len(tabA)
	n = len(tabA[0])
	while True:
		kol += 1
		ma = -1
		k = -1
		fl = True
		for i in range(0, m - 2):
			if tabA[i][0] < 0:
				pam = i
				fl = False
				break
		if fl:
			break
		for i in range(1, n - 1):
			if tabA[pam][i] < 0:
				k = i
				break
		if k == -1:
			print('{:>28s}'.format("Error"))
			break
		mi = 10000000
		r = -1
		for i in range(0, m - 2):
			if tabA[i][k] != 0:
				if tabA[i][0] / tabA[i][k] < mi and tabA[i][0] / tabA[i][k] >= 0:
					mi = tabA[i][0] / tabA[i][k]
					r = i
		if r == -1:
			# print('{:>28s}'.format("No more positive in S/ Xk"))
			break
		#print('{:<28s}'.format("Razr stolb " + "X" + str(tabA[-1][k])))
		#print('{:<28s}'.format("Razr stroka " + "X" + str(tabA[r][-1])), end="\n\n")
		tab2 = copy.deepcopy(tabA)
		tabA[r][k] = 1 / tab2[r][k]
		for i in range(m - 1):
			for j in range(n - 1):
				if j != k:
					tabA[r][j] = tab2[r][j] / tab2[r][k]
					if i != r:
						tabA[i][j] = tab2[i][j] - tab2[i][k] * tab2[r][j] / tab2[r][k]
			if i != r:
				tabA[i][k] = -tab2[i][k] / tab2[r][k]
		tabA[-1][k], tabA[r][-1] = tabA[r][-1], tabA[-1][k]
		#printWithXInTable(tabA)
		'''print('{:>28s}'.format("Calculated Symplics table " + str(kol)))
		printWithXInTable(tabA)'''
	# print('{:>28s}'.format("Opor Symplics table " + str(kol)))
	#printWithXInTable(tabA)
	#printOpor(tabA)
	return tabA


def calculateSimplexTable(tabB):
	pam = copy.deepcopy(tabB)
	tabB = findOpor(copy.deepcopy(tabB))
	if pam != tabB:
		print("Here was opor")
	'''if tabB[-2][0] < 0:
		print("Minus in F v opornom")
		return tabB'''
	kol = 0
	m = len(tabB)
	n = len(tabB[0])
	flEnd = False
	while True:
		kol += 1
		mi = 10000000
		k = -1
		for i in range(1, n - 1):
			if tabB[-2][i] >= 0 and tabB[-2][i] < mi:
				mi = tabB[-2][i]
				k = i
		if k == -1:
			# print('{:>28s}'.format("No more positive in F"))
			flEnd = True
			break
		mi = 10000000
		r = -1
		for i in range(0, m - 2):
			if tabB[i][k] != 0:
				if tabB[i][0] / tabB[i][k] < mi and tabB[i][0] / tabB[i][k] >= 0 and tabB[i][k]>0:
					mi = tabB[i][0] / tabB[i][k]
					r = i
		if r == -1:
			# print('{:>28s}'.format("No more positive in S/ Xk"))
			flEnd = True
			break
		# print('{:<28s}'.format("Razr stolb " + "X" + str(tabB[-1][k])))
		# print('{:<28s}'.format("Razr stroka " + "X" + str(tabB[r][-1])), end="\n\n")
		tab2 = copy.deepcopy(tabB)
		tabB[r][k] = 1 / tab2[r][k]
		for i in range(m - 1):
			for j in range(n - 1):
				if j != k:
					tabB[r][j] = tab2[r][j] / tab2[r][k]
					if i != r:
						tabB[i][j] = tab2[i][j] - tab2[i][k] * tab2[r][j] / tab2[r][k]
			if i != r:
				tabB[i][k] = -tab2[i][k] / tab2[r][k]
		tabB[-1][k], tabB[r][-1] = tabB[r][-1], tabB[-1][k]
		#print('{:>28s}'.format("Symplic table " + str(kol)))
		#printWithXInTable(tabB)
	print('{:>28s}'.format("Symplic table "), end="")
	printWithXInTable(tabB)
	flEnd = True
	return tabB


def checkFree(tabC):
	m = len(tabC)
	n = len(tabC[0])
	for i in range(0, m):
		if (tabC[i][0] % 1 != 0) and (tabC[i][-1] in base):
			return i
	return -1


def checkCalcTable(tab):
	m = len(tab)
	n = len(tab[0])
	fl_e = True
	for i in range(n - 1):
		if tab[-2][i] >= 0:
			fl_e = False
			break
	if fl_e:
		for i in range(m - 2):
			if tab[i][0] < 0:
				return True
	return False


def addInDefTab(fl, nameX, num, tabIn):
	m = len(tabIn)
	n = len(tabIn[0])
	tab2 = [[0] * (n) for i in range(m + 1)]
	if fl == "<":
		fl = 1
	else:
		fl = -1
	for i in range(m - 2):
		for j in range(n):
			tab2[i][j] = tabIn[i][j]
	for i in range(n):
		tab2[-3][i] = 0
		if tabIn[-1][i] == nameX:
			tab2[-3][i] = fl
	tab2[-3][0] = num * fl
	tab2[-3][-1] = m + n - 3
	for j in range(n):
		tab2[-2][j] = tabIn[-2][j]
	for j in range(1, n):
		tab2[-1][j] = tabIn[-1][j]
	tab2[-1][0] = 77  # S
	tab2[-2][-1] = 88  # F
	tab2[-1][-1] = 99  # empty
	return tab2


def branchAndBound(tabI, dTab):
	i = checkFree(tabI)
	if i == -1:
		printAnswer(len(tabI[0]), "max", tabI)
		return
	if checkCalcTable(tabI):
		print("exit")
		return
	num1 = tabI[i][0] - tabI[i][0] % 1
	print("\n", "Start X", tabI[i][-1], " <= ", num1, sep='')
	dTab1 = addInDefTab("<", tabI[i][-1], num1, copy.deepcopy(dTab))
	print("def tab", end="")
	printWithXInTable(dTab1)
	tab1 = calculateSimplexTable(copy.deepcopy(dTab1))
	'''if tab1 == False:
		print("End ", "X", tabI[i][-1], " <= ", num1, sep='')
		return'''
	branchAndBound(copy.deepcopy(tab1), copy.deepcopy(dTab1))
	print("End ", "X", tabI[i][-1], " <= ", num1, sep='')
	print("\n", "Start X", tabI[i][-1], " >= ", num1 + 1, sep='')
	if checkCalcTable(tabI):
		print("exit")
		return
	dTab2 = addInDefTab(">", tabI[i][-1], num1 + 1, copy.deepcopy(dTab))
	print("def tab", end="")
	printWithXInTable(dTab2)
	tab2 = calculateSimplexTable(copy.deepcopy(dTab2))
	'''if tab2 == False:
		print("End ", "X", tabI[i][-1], " >= ", num1 + 1, sep='')
		return'''
	branchAndBound(copy.deepcopy(tab2), copy.deepcopy(dTab2))
	print("End ", "X", tabI[i][-1], " >= ", num1 + 1, sep='')


def bruteForce():
	a = getA()
	b = getB()
	c = getC()
	len1 = len(a)
	d = dict()
	ma = -10000000
	print()
	print("Start brute force")
	for i in range(100):
		for j in range(100):
			for k in range(100):
				fl = True
				pam = 0
				for ii in range(len1):
					pam += a[ii][0] * i + a[ii][1] * j + a[ii][2] * k
					if pam > b[ii]:
						fl = False
						break
					pam = 0
				if fl:
					if c[0] * i + c[1] * j + c[2] * k > ma:
						ma = c[0] * i + c[1] * j + c[2] * k
						d[ma] = [i, j, k]
						print(ma, d[ma])
	print("Fmax=", ma)
	for i in range(1, len(bbase) + 1):
		print("X" + str(i) + " = " + '{:<7.2f}'.format(d[ma][i-1]))


def getA():
	a = [[2, 1, 1],
	     [1, 2, 0],
	     [0, 0.5, 1]]
	'''a = [[3, 1, 0],
	     [1, 1, 0.5],
	     [1, 0, 4]]'''
	return a


def getC():
	c = [2, 8, 3]
	# c = [5, 2, 6]
	return c


def getB():
	b = [4, 6, 2]
	# b = [7, 4, 3]
	return b


def main():
	n = 3
	m = 3
	flag = "max"
	tab = createSimplexTable(flag, n, getA(), getB(), getC())
	'''tab = findOpor(n, tab)
	tab = calculateSimplexTable(n, n, tab)'''
	for i in range(1, n + 1):
		base.add(i)
		bbase.add(i)
	print('{:>28s}'.format("Default symplic table"), end ="")
	printWithXInTable(tab)
	num = 0
	pam = calculateSimplexTable(copy.deepcopy(tab))
	branchAndBound(copy.deepcopy(pam), copy.deepcopy(tab))
	print()
	pam = sorted(answ)[-1]
	print("F" + str(flag) + " = " + str(pam))
	pam = answ[pam]
	for i in range(1, len(bbase) + 1):
		print("X" + str(i) + " = " + '{:<7.2f}'.format(pam[i]))
	bruteForce()
	#print(*answ)


main()
