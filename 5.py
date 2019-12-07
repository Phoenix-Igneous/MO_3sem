from random import *
import copy
from math import *
import matplotlib.pyplot as plt

INF = 100000000000000000000000

def getWeightA(r):
	a = [0] * r
	m = int((r - 1) / 2 - (r - 1) / 2 % 1)
	a[m] = uniform(0, 1)
	sumHalf = a[m]
	sumAll = a[m]
	for i in range(m - 1, 0, -1):
		a[i] = 0.5 * uniform(0, 1 - sumHalf)
		a[r - 1 - i] = a[i]
		sumHalf += a[i]
		sumAll += 2 * a[i]
	a[0] = 0.5 * (1 - a[m])
	a[r - 1] = 0.5 * a[0]
	sumAll += 2 * a[0]
	for i in range(r):
		a[i] /= sumAll
	return a


def getSignFiltr(signWithNoise, a, r, k):
	signFiltred = []
	m = floor((r - 1) / 2)
	for i in range(m, k - m + 1):
		pam = 0
		for j in range(i - m, i + m+1):
			#print(j)
			#print("l",len(signWithNoise))
			#print(signWithNoise[j])
			#print("a[j + m - k]", a[j + m - k])
			#print("signWithNoise[j-1]", signWithNoise[j-1])
			pam += a[j + m - i] / signWithNoise[j]
			#print(pam)
		pam = 1 / pam
		#print("pam=",pam)
		signFiltred.append(pam)
	#print("ff", *signFiltred)
	'''print("l")
	print(*signFiltred)
	print("ll")'''
	return signFiltred


def getNearestWD(signFiltred, signWithNoise, r, k):
	m = floor((r - 1) / 2)
	w = []
	d = []
	d.append(abs(signFiltred[0] - signWithNoise[0]))
	for i in range(1, k - m - 1):
		w.append(abs(signFiltred[i] - signFiltred[i-1]))
		d.append(abs(signFiltred[i] - signWithNoise[i]))
	#print(*signFiltred)
	#print("h",max(w), max(d))
	return [max(w), max(d)]


def getAllNew(signWithNoise, r, k):
	a = getWeightA(r)
	signFiltred = getSignFiltr(copy.deepcopy(signWithNoise), copy.deepcopy(a), r, k)
	receivedWD = getNearestWD(copy.deepcopy(signFiltred), copy.deepcopy(signWithNoise), r, k)
	return [receivedWD[0], receivedWD[1], a, signFiltred]

def main():
	xMin = 0
	xMax = pi
	A = 0.5/2
	r = 5
	P = 0.95
	e = 0.01
	K = 100
	x = [0]*(K+1)
	signGener = [0]*(K+1)
	signWithNoise = [0]*(K+1)
	noise = [0]*(K+1)
	L = 10
	M = floor((r - 1) / 2)
	print("%-3s%7s%10s%7s%18s" % ("k", "x", "signGen", "noise", "signWithNoise"))
	for i in range(K + 1):
		x[i] = xMin + i * (xMax - xMin) / K
		signGener[i] = sin(x[i]) + 2 * A
		noise[i] = uniform(-A, A)
		signWithNoise[i] = signGener[i] + noise[i]
		print("%-3d%7.3f%8.3f%10.3f%15.3f" % (i, x[i], signGener[i], noise[i], signWithNoise[i]))
	print()
	N = floor(log(1 - P) / log(1 - e / (xMax - xMin)))
	plt.title("Омега-Дельта")
	distMin = INF
	for l in range(L+1):
		ll = l/L
		print("Лямбда", ll)
		arrDist = getAllNew(copy.deepcopy(signWithNoise), r, K)
		for i in range(0, N):
			dist = max(arrDist[0], arrDist[1])
			if i == 0:
				distMin = dist
				pam = arrDist
			elif dist < distMin:
				distMin = dist
				pam = arrDist
		print("J( ", pam[0], "; ", pam[1], ") = ",
	      ll * pam[0] + (1 - ll) * pam[1])
		print("dist =  ", pam[0])
		plt.plot(pam[0], pam[1], linestyle=":", marker='o', label=ll)
		if l == 0:
			pamMin = pam
			dmin = distMin
			llMin = l / L
		else:
			if distMin < dmin:
				pamMin = pam
				dmin = distMin
				llMin = l / L
	plt.legend(loc='upper left')
	plt.savefig('C:/Users/volko/Desktop/CC/MO/5/w-del1_r5.png', format='png')
	plt.show()
	plt.plot(range(0, K + 1), signWithNoise, color='g', label="f_real")
	plt.plot(range(0, K + 1), signGener, color='b', label="f_ideal")
	if r == 5:
		plt.plot(range(K - M - 1), pamMin[3], color='r', label="result")
	if r == 3:
		plt.plot(range(K - M), pamMin[3], color='r', label="result")
	plt.savefig('C:/Users/volko/Desktop/CC/MO/5/plot1_r5.png', format='png')
	plt.legend(loc='upper left')
	plt.show()
	plt.title("Noise")
	plt.plot(signGener, noise, color='y')
	plt.savefig('C:/Users/volko/Desktop/CC/MO/5/noise1_r5.png', format='png')
	plt.show()
	print("\n\n\n")
	print("Результат")
	print("J = ", llMin * pamMin[0] + (1 - llMin) * pamMin[1])
	print("w = ", pamMin[0])
	print("o = ", pamMin[1])
	print("alfa = ", pamMin[2])
	print("lambda = ", llMin)


main()