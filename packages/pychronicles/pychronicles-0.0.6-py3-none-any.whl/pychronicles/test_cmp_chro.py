#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparison between recognition from sequences using lists and roaring bitmaps

@author: Thomas Guyet
@date: 01/2020
@institution: AGROCAMPUS-OUEST/IRISA
"""

from chroaring import Sequence, Chroaring
from chronicle import Chronicle

import random
import time


vocsize=5
maxdelay=20
chrosize=3
cd=0.6
seq=[random.randint(0,vocsize) for i in range(2000)]

s=Sequence()
for i in seq:
	s.append(i)

#print(seq)
#print(s)

C=Chronicle()
Coa=Chroaring()


for i in range(chrosize):
	e=random.randint(0,vocsize)
	C.add_event(i,e)
	Coa.add_event(i,e)
	for j in range(i):
		if random.random() < cd:
			u=random.randint(-maxdelay,maxdelay)
			l=random.randint(-maxdelay,maxdelay)
			if u<l:
				u,l=l,u
			C.add_constraint(j,i, (l,u) )
			Coa.add_constraint(j,i, (l,u) )

C.minimize()
Coa.minimize()
print(C)
if not C.inconsistent:
	t0=time.time()
	occs=C.enum(seq)
	tc=time.time()-t0
	print(occs)
	print("-----------------------------")
	t0=time.time()
	occs=Coa.enum(s)
	tcoa=time.time()-t0
	print(occs)
	print(tc,tcoa)
	
	