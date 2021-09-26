from ast import literal_eval
from operator import itemgetter
import random

parallels_num = 7
series_num = 13

def load_caps():
	data = {}
	cap = []; r = []; num = []
	with open('caps91.txt') as f:
		for line in f:
			cap.append(int(line.split(",")[1]))
			num.append(int(line.split(",")[0]))
			r.append(int(line.split(",")[2]))
	return { "num":num,"cap":cap,"r":r }

def gen_caps_file():
	stuff = [ random.randrange(2450,2790) for x in range(91)]
	with open('caps.txt', "w") as fhandle:
		for s in stuff:
		    fhandle.write(f'{s}\n')

def compose(stuff):
	global parallels_num, series_num
	mystuff = stuff.copy()
	series = []
	for s_num in range(series_num):
		parallels = []
		for p_num in range(parallels_num):
			parallels.append(mystuff.pop(random.randint(0, len(mystuff)-1)))
		series.append(parallels)
	return series

def fit(series):
	sums = []
	for p in series:
		sums.append(sum(p))
	sums.sort()
	d = sums[-1]-sums[0] #максимальная разность емкостей параллелей
	return d

def minmax(series):
	sums = []
	for p in series:
		sums.append(sum(p))
	mini = sums.index(min(sums))
	maxi = sums.index(max(sums))
	return mini, maxi, sums[mini], sums[maxi]

def find_optimum(stuff):
	m = compose(stuff)
	i = 0
	while fit(m) > 1:
		i += 1;
		if i > 5000:
			return find_optimum(stuff)
			
		mi, mx, misum, mxsum = minmax(m)

		while True:
			r7_1 = random.randrange(0,6);
			r7_2 = random.randrange(0,6);
			x = abs(mxsum - m[mx][r7_1] + m[mi][r7_2])
			if x < mxsum:
				break

		m[mi][r7_2], m[mx][r7_1] = m[mx][r7_1], m[mi][r7_2]
	return m

def printer(m, data):
	for p in m:
		print(p, sum(p))
	print("Total delta:",fit(m),"\n")

	cap = data.get("cap"); r = data.get("r"); num = data.get("num")
	for p in m:
		rsum = 0; capsum = 0
		for el_of_p in p:
			i = 0; 
			if el_of_p in cap:
				i = cap.index(el_of_p)
			capsum += cap[i]; 
			if rsum == 0:
				rsum = r[i]
			else:
				rsum = rsum*r[i]/(rsum+r[i])
			print(f"{num[i]:02d}",":",el_of_p,':',r[i]," ", end='', sep='')
			cap.remove(cap[i]); r.remove(r[i]); num.remove(num[i])
		print(" | CSum:",capsum," RTot:",f"{rsum:.2f}",sep='')
	print("NumberOfCell:Cap:R")


data = load_caps()
m = find_optimum(data.get("cap"))
printer(m, data)
