import copy

'''
1.
Составляем вектор весов
Внешность   Фин.запросы Домовитость Характер
2             6             5         8
1/(2+6+5+8)		
Нормализовав получим
0,095 	0,285 0,238 0,38
			Внешность   Фин.запросы Домовитость Характер
А. Татьяна     7           8          5           5
B. Лариса      9           4          2           8
C. Наталья     3           6          9           7
D. Ольга       6           9          8           2
В качестве главного критерия выберем критерий Характер
Установим минимально допустимые уровни для остальных критериев:
Внешность не менее 0,5*Amax1
фин. запросы        0.2*Amax2
Домовитость       0.4*Amax3
Проведём нормировку



2.
Выберем в качестве главных критериев для данного метода Внешность и
Домовитость. Внешность – по оси х, Домовитость– по оси у. Сформируем
множество Парето графическим методом (координаты каждой точки и точки
утопии в выводе функции, график – рис1). Оба критерия
максимизируются, поэтому точка утопии находится в правом верхнем
углу графика.

'''


def normalizeVec(vec):
	n = len(vec)
	pam = 0
	for i in range(n):
		pam += vec[i]
	pam = 1 / pam
	for i in range(n):
		vec[i] = vec[i] * pam
	print("Normalize Vec:")
	for i in range(n):
		print('{:>7.2f}'.format(vec[i]), end="")
	print()
	return vec


def normalizeTab(tab, numberMainC):
	n = len(tab)
	m = len(tab[0])
	pamMa = [-100] * m
	pamMi = [100000] * m
	for j in range(m):
		if j == numberMainC - 1:
			continue
		for i in range(n):
			pamMa[j] = max(pamMa[j], tab[i][j])
			pamMi[j] = min(pamMi[j], tab[i][j])
	for i in range(n):
		for j in range(m):
			if j == numberMainC - 1:
				continue
			mi = pamMi[j]
			ma = pamMa[j]
			tab[i][j] = (tab[i][j] - mi) / (ma - mi)
	return tab


def printWithAll(tab, pam):
	print()
	pam2 = [" ", "Внешность", "Фин.зап.", "Домов.", "Характер"]
	n = len(tab)
	m = len(tab[0])
	for j in range(m + 1):
		print('{:>9s}'.format(pam2[j]), end="")
	print()
	for i in range(n):
		print('{:>9s}'.format(pam[i]), end="")
		for j in range(m):
			print('{:>9.2f}'.format(tab[i][j]), end="")
		print()


def findBest(tab, pam):
	fl = ""
	n = len(tab)
	m = len(tab[0])
	for i in range(n):
		fl = pam[i]
		for j in range(m):
			if tab[i][j] == 0:
				fl = ""
				break
		if fl != "":
			break
	print("The best is: ", end="")
	print('{:>9s}'.format(fl))


def changeForLimit(tab, pam, numbCr):
	print("Start changing Limits")
	print("The main crit N:", numbCr)
	printWithAll(tab, pam)
	normalizeTab(tab, numbCr)
	printWithAll(tab, pam)
	findBest(tab, pam)


def graphParetto(tab, names, n1, n2):
	print()
	print("Start Paretto")
	n = len(tab)
	pamMaX = -1
	pamMaY = -1
	for i in range(n):
		pamMaX = max(pamMaX, tab[i][n1 - 1])
		pamMaY = max(pamMaY, tab[i][n2 - 1])
	print("Num for X=", n1, "Num for Y=", n2)
	print("Max X =", pamMaX, "Max Y =", pamMaY)
	pammi = 10000000000
	pam = ""
	print("R:")
	for i in range(n):
		print('{:>9s}'.format(names[i]), end="")
		r = (tab[i][n1 - 1] - pamMaX) ** 2 + (tab[i][n2 - 1] - pamMaY) ** 2
		print('{:>7.2f}'.format(r ** (1 / 2)))
		if r < pammi:
			pammi = r
			pam = i
	print("The best is: ", end="")
	print(names[i], " (", tab[i][n1 - 1], " , ", tab[i][n2 - 1], ")", sep="")


def normalizeTabW(tab):
	n = len(tab)
	m = len(tab[0])
	pa = [0] * m
	for j in range(m):
		pam = 0
		for i in range(n):
			pam += tab[i][j]
		pa[j] = 1 / pam
	for i in range(n):
		for j in range(m):
			tab[i][j] *= pa[j]
	return tab


def weightAndAssociation(tab, pam):
	print()
	print("Start WeightAndAssociation")
	print("Default Vec:")
	vec = [0.5 + 1,
	       1,
	       1 + 1,
	       0 + 0.5
	       ]
	n = len(tab)
	for i in range(n):
		print('{:>9.2f}'.format(vec[i]), end="")
	print()
	vec = normalizeVec(vec)
	vec2 = [[0] for i in range(n)]
	for i in range(n):
		vec2[i][0] = vec[i]
	vec = vec2
	m = len(tab[0])
	aa = [0] * n
	tab = normalizeTabW(tab)
	print("Normalize tab")
	printWithAll(tab, pam)
	for i in range(n):
		for j in range(m):
			aa[i] += tab[i][j] * vec[j][0]
	tab = aa
	print("Union Crit:")
	print("(", end="")
	for i in range(n):
		print('{:>9.2f}'.format(tab[i]), end="")
	print(")")
	ma = -1
	name = -1
	for i in range(n):
		if tab[i] > ma:
			ma = tab[i]
			name = i
	print("The best is:", pam[name])


def printCrit(names, crit):
	n = len(names)
	print('{:>9s}'.format(""), end="")
	for i in range(n):
		print('{:>9s}'.format(names[i]), end="")
	print('{:>9s}'.format("Сум. стр."), end="")
	print('{:>9s}'.format("Нормир."), end="")
	print()
	for i in range(n):
		print('{:>9s}'.format(names[i]), end="")
		for j in range(n + 2):
			print('{:>9.2f}'.format(crit[i][j]), end="")
		print()


def fillTabAndGetNormir(names, crit1, wei):
	n = len(names)
	for i in range(n):
		su = 0
		for j in range(n):
			if i == j:
				crit1[i][j] = 1
			if crit1[i][j] == 0 and crit1[j][i] != 0:
				crit1[i][j] = 1 / crit1[j][i]
			su += crit1[i][j]
		crit1[i][-2] = su
	su = 0
	for i in range(n):
		su += crit1[i][-2]
	if su != 0:
		su = 1 / su
	for i in range(n):
		crit1[i][-1] = crit1[i][-2] * su
	normir = [crit1[i][-1] for i in range(n)]
	printCrit(names, crit1)
	kk=0
	for i in range(n):
		for j in range(n):
			kk+= crit1[i][j]*wei
	if wei!=1:
		'''print("ИС =", end='')
		print('{:>5.2f}'.format((kk-n)/(n-1)), end="")
		print("%")'''
		print("Отношение согл.=", end='')
		print('{:>5.2f}'.format((kk - n) / (n - 1)/0.9), end="")
		print("%")
	return normir


def metHierarchy(names, iVec):
	normVec = normalizeVec(iVec)
	print()
	print("Start Hierarchy")
	pam2 = ["Внешность", "Фин.зап.", "Домов.", "Характер"]
	n = len(names)
	k = 0
	print()
	print(pam2[k])
	crit1 = [[0] * (n + 2) for i in range(n)]
	crit1[0][1] = 8
	crit1[0][2] = 6
	crit1[0][3] = 3
	crit1[1][2] = 9
	crit1[1][3] = 8
	crit1[2][3] = 4
	norm1 = fillTabAndGetNormir(names, crit1,normVec[k])
	k += 1
	print()
	print(pam2[k])
	crit1 = [[0] * (n + 2) for i in range(n)]
	crit1[0][1] = 8
	crit1[0][2] = 7
	crit1[0][3] = 4
	crit1[1][2] = 3
	crit1[1][3] = 2
	crit1[2][3] = 4
	norm2 = fillTabAndGetNormir(names, crit1,normVec[k])
	k += 1
	print()
	print(pam2[k])
	crit1 = [[0] * (n + 2) for i in range(n)]
	crit1[0][1] = 8
	crit1[0][2] = 3
	crit1[0][3] = 2
	crit1[1][2] = 2
	crit1[1][3] = 3
	crit1[2][3] = 9
	norm3 = fillTabAndGetNormir(names, crit1,normVec[k])
	k += 1
	print()
	print(pam2[k])
	crit1 = [[0] * (n + 2) for i in range(n)]
	crit1[0][1] = 5
	crit1[0][2] = 6
	crit1[0][3] = 8
	crit1[1][2] = 7
	crit1[1][3] = 9
	crit1[2][3] = 7
	norm4 = fillTabAndGetNormir(names, crit1,normVec[k])
	print()
	crit1 = [[0] * (n + 2) for i in range(n)]
	crit1[0][1] = 8
	crit1[0][2] = 0.5
	crit1[0][3] = 0.125
	crit1[1][2] = 3
	crit1[1][3] = 0.111
	crit1[2][3] = 1
	norm5 = fillTabAndGetNormir(pam2, crit1, 1)

	tab = [[0]*n for i in range(n)]
	for j in range(n):
		tab[j][0] = norm1[j]
		tab[j][1] = norm2[j]
		tab[j][2] = norm3[j]
		tab[j][3] = norm4[j]
	vec = [0]*n
	for i in range(n):
		for j in range(n):
			vec[i] += tab[i][j] * norm5[j]
	print("Union Crit:")
	print("(", end="")
	for i in range(n):
		print('{:>9.2f}'.format(vec[i]), end="")
	print(")")
	ma = -1
	name = -1
	for i in range(n):
		if vec[i] > ma:
			ma = vec[i]
			name = i
	print("The best is:", names[name])


def main():
	tab = [[7, 8, 5, 5],
	       [9, 4, 2, 8],
	       [3, 6, 9, 7],
	       [6, 9, 8, 2]]
	names = ["Татьяна", "Лариса", "Наталья", "Ольга"]
	vec = [2, 6, 5, 8]
	changeForLimit(copy.deepcopy(tab), names, 4)
	graphParetto(copy.deepcopy(tab), names, 1, 3)
	weightAndAssociation(copy.deepcopy(tab), names)
	metHierarchy(names, vec)


main()
