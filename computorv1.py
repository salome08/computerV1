# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computorv1.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: shazan <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/03/24 15:50:52 by shazan            #+#    #+#              #
#    Updated: 2015/04/02 20:07:14 by shazan           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

eq = raw_input("entrez une equation: ")

if eq.count("=") != 1:
	print "Need '=' once in the equaation"
	raise SystemExit

def get_any_of(str, match):
	i = -1
	for c in str:
		i += 1
		if i == 2:
			continue
		if c in match:
			return i
	return -1

eq = eq.replace(" ","")
eq = eq.split("=")
left = eq[0]
right = eq[1]

list_l = []
i = 0
while len(left) != 0 and i < len(left):
	next_op = -1
	if left[i] is "X":
		next_op = get_any_of(left[i:], "+-")
		if next_op == -1:
			list_l.append(left)
			left = ""
		else:
			list_l.append(left[:i + next_op])
			left = left[i + next_op:]
		i = -1
	i += 1
	
list_r = []
i = 0
while len(right) != 0 and i < len(right):
	next_op = -1
	if right[i] is "X":
		next_op = get_any_of(right[i:], "+-")
		if next_op == -1:
			list_r.append(right)
			right = ""
		else:
			list_r.append(right[:i + next_op])
			right = right[i + next_op:]
		i = -1
	i += 1

def calcul_coef(list_l, list_r, n=0):
	ret = .0
	ref = "*X^" + str(n)
	for c in list_l:
		if ref in c:
			ret += eval(c[:c.find(ref)])
	for c in list_r:
		if ref in c:
			ret -= eval(c[:c.find(ref)])
	return ret

coef_x0 = calcul_coef(list_l, list_r, 0)
coef_x1 = calcul_coef(list_l, list_r, 1)
coef_x2 = calcul_coef(list_l, list_r, 2)

def get_expo(listes):
	list_expos = []
	for a in listes:
		pos_x = a.find("X")
		power = eval(a[pos_x + 2:])
		if power not in list_expos:
			list_expos.append(power)
	return list_expos

list_expos = get_expo(list_l + list_r)
for x in list_expos:
	if x > 2 or x < 0:
		coef_n = calcul_coef(list_l, list_r, x)
		if coef_n != 0:
			print "polynomial degree: ", x
			print ("The polynomial degree is stricly greater than 2, I can't solve.")
			raise SystemExit

def reduced_form(coef_x0, coef_x1, coef_x2):
	tmp = 1
	ret = ""
	if coef_x0 != 0:
		ret += "{} * X^0 ".format(coef_x0)
		tmp = 0
	if coef_x1 > 0:
		if tmp == 0:
			ret += "+ "
		else:
			tmp = 0
		ret += "{} * X^1 ".format(coef_x1)
	elif coef_x1 < 0:
		if tmp == 0:
			ret += "- "
			ret += "{} * X^1 ".format(coef_x1 * -1)
		else:
			tmp = 0
			ret += "{} * X^1 ".format(coef_x1)
	if coef_x2 > 0:
		if tmp == 0:
			ret += "+ "
		else:
			tmp = 0
		ret += "{} * X^2 ".format(coef_x2)
	elif coef_x2 < 0:
		if tmp == 0:
			ret += "- "
			ret += "{} * X^2 ".format(coef_x2 * -1)        
		else:
			tmp = 0
			ret += "{} * X^2 ".format(coef_x2)
	return ret

def complex_i():
	delta_neg = delta * -1
	denom = 2 * coef_x2
	num_1 = coef_x1 * -1 / denom
	num_2 = delta_neg**(0.5) / denom
	if denom < 0:
		denom = denom * -1
	print("{} - i * {}".format(num_1, num_2))
	print("{} + i * {}".format(num_1, num_2))

if coef_x2 != 0:
	print "Reduced form:", reduced_form(coef_x0, coef_x1, coef_x2), "= 0"
	print("Polynomial degree: 2")
	deg_max = 2
elif coef_x1 != 0:
	print "Reduced form:", reduced_form(coef_x0, coef_x1, coef_x2), "= 0"
	print("Polynomial degree: 1")
	deg_max = 1
else:
	print("Polynomial degree: 0")
	deg_max = 0

if deg_max == 2:
	delta = coef_x1**2 - 4 * coef_x2 * coef_x0
	if delta > 0:
		print "Discriminant is strictly positive, the two solutions are:"
		print (-1 * coef_x1 - delta**(0.5))/(2 * coef_x2)
		print (-1 * coef_x1 + delta**(0.5))/(2 * coef_x2)
	elif delta < 0:
		print "Discriminant is strictly negative, the two solutions are:"
		complex_i()
	elif delta == 0:
		print "discriminant is null, the solution is:"
		print eval("-1 * coef_x1 / (2 * coef_x2)")

if deg_max == 1:
	print eval ("-1 * coef_x0 / coef_x1")

if deg_max == 0:
	if not reduced_form(coef_x0, coef_x1, coef_x2):
		print "there is an infinity of value for X"
	else:
		print "il n'y a pas de solutions"
