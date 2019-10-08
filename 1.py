import copy


def printWithXInTable(n, tab):
	for i in range(n + 1):
		for j in range(n + 1):
			print('{:>7.2f}'.format(tab[i][j]), end="")
		pam = str(int(tab[i][n + 1]))
		if pam == "88":
			pam = "  F"
		elif pam == "99":
			pam = ""
		else:
			pam = "  X" + pam
		print(pam)
	for i in range(n + 2):
		pam = str(int(tab[n + 1][i]))
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
	print("\n" + "Answer:\n" + "F" + str(flag) + " = " + " " + '{:<9.3f}'.format(tab[n][0]*zn))
	pam = [0] * (n + 1)
	for i in range(n + 1):
		pam[i] = 0
	for i in range(n):
		if 0 < tab[i][n + 1] <= n:
			pam[tab[i][n + 1]] = tab[i][0]
	for i in range(1, n + 1):
		print("X" + str(i) + " = " + '{:<7.2f}'.format(pam[i]))
	print()


def printOpor(n, tab):
	print("\n" + "Opor answer:\n" + "F" + " = " + " " + '{:<9.3f}'.format(tab[n][0]))
	pam = [0] * (n + 1)
	for i in range(n + 1):
		pam[i] = 0
	for i in range(n):
		if 0 < tab[i][n + 1] <= n:
			pam[tab[i][n + 1]] = tab[i][0]
	for i in range(1, n + 1):
		print("X" + str(i) + " = " + '{:<7.2f}'.format(pam[i]))
	print()

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


def calculateSimplexTable(n, tab):
	kol = 0
	while True:
		kol += 1
		mi = 10000000
		k = -1
		for i in range(1, n + 1):
			if tab[n][i] > 0 and tab[n][i] < mi:
				mi = tab[n][i]
				k = i
		if k == -1:
			print('{:>28s}'.format("No more positive in F"))
			break
		mi = 10000000
		r = -1
		for i in range(0, n):
			if tab[i][k] != 0:
				if tab[i][0] / tab[i][k] < mi and tab[i][0] / tab[i][k] > 0:
					mi = tab[i][0] / tab[i][k]
					r = i
		if r == -1:
			print('{:>28s}'.format("No more positive in S/ Xk"))
			break
		print('{:<28s}'.format("Razr stolb " + "X" + str(tab[n + 1][k])))
		print('{:<28s}'.format("Razr stroka " + "X" + str(tab[r][n + 1])), end="\n\n")
		tab2 = copy.deepcopy(tab)
		tab[r][k] = 1 / tab2[r][k]
		for i in range(n + 1):
			for j in range(n + 1):
				if j != k:
					tab[r][j] = tab2[r][j] / tab2[r][k]
					if i != r:
						tab[i][j] = tab2[i][j] - tab2[i][k] * tab2[r][j] / tab2[r][k]
			if i != r:
				tab[i][k] = -tab2[i][k] / tab2[r][k]
		tab[n + 1][k], tab[r][n + 1] = tab[r][n + 1], tab[n + 1][k]
		print('{:>28s}'.format("Symplic table " + str(kol)))
		printWithXInTable(n, tab)
	return tab


def findOpor(n, tab):
	kol = 0
	while True:
		kol += 1
		ma = -1
		k = -1
		fl = True
		for i in range(0, n + 1):
			if tab[i][0] < 0:
				pam = i
				fl = False
				break
		if fl:
			break
		for i in range(1, n + 1):
			if tab[pam][i] < 0:
				k = i
				break
		if k == -1:
			print('{:>28s}'.format("Error"))
			break
		mi = 10000000
		r = -1
		for i in range(0, n):
			if tab[i][k] != 0:
				if tab[i][0] / tab[i][k] < mi and tab[i][0] / tab[i][k] > 0:
					mi = tab[i][0] / tab[i][k]
					r = i
		if r == -1:
			print('{:>28s}'.format("No more positive in S/ Xk"))
			break
		print('{:<28s}'.format("Razr stolb " + "X" + str(tab[n + 1][k])))
		print('{:<28s}'.format("Razr stroka " + "X" + str(tab[r][n + 1])), end="\n\n")
		tab2 = copy.deepcopy(tab)
		tab[r][k] = 1 / tab2[r][k]
		for i in range(n + 1):
			for j in range(n + 1):
				if j != k:
					tab[r][j] = tab2[r][j] / tab2[r][k]
					if i != r:
						tab[i][j] = tab2[i][j] - tab2[i][k] * tab2[r][j] / tab2[r][k]
			if i != r:
				tab[i][k] = -tab2[i][k] / tab2[r][k]
		tab[n + 1][k], tab[r][n + 1] = tab[r][n + 1], tab[n + 1][k]
		print('{:>28s}'.format("Symplic table " + str(kol)))
		printWithXInTable(n, tab)
	printOpor(n, tab)
	return tab


def getA():
	# max
	a = [[2, 1, 1],
	 [1, 2, 0],
	 [0, 0.5, 1]]
	# min
	'''a = [[2, 1, 0],
	     [1, 2, 0.5],
	     [1, 0, 1]]'''
	return a


def getB():
	# max
	b = [4, 6, 2]
	# min
	#b = [2, 8, 3]
	return b


def getC():
	# max
	c = [2, 8, 3]
	# min
	#c = [4, 6, 2]
	return c


def main():
	a = getA()
	b = getB()
	c = getC()
	n = 3
	flag = "max"
	tab = createSimplexTable(flag, n, a, b, c)
	print('{:>28s}'.format("Default symplic table"))
	printWithXInTable(n, tab)
	tab = findOpor(n, tab)
	tab = calculateSimplexTable(n, tab)
	if type(tab) == list: # for Errors
		printAnswer(n, flag, tab)


main()
