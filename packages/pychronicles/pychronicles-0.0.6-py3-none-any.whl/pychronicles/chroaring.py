#!/bin/python3
# -*- coding: utf-8 -*-
"""
Chronicles enumeration from sequences encoded using roaring bitmaps

@author: Thomas Guyet
@date: 01/2020
@institution: AGROCAMPUS-OUEST/IRISA
"""

from pyroaring import BitMap
from chronicle import EventMapper, Chronicle, resize

class Sequence:
	"""
	@author: Thomas Guyet
	@date: 01/2020
	@institution: AGROCAMPUS-OUEST/IRISA
	"""
	def __init__(self):
		self.data = {} # {item : position Bitmap}
		self.curpos=0

	def append(self, item, pos=None):
		if pos==None:
			self.curpos +=1
		else:
			self.curpos = pos
		if not item in self.data:
			self.data[item]=BitMap()
		self.data[item].add(self.curpos)

	def find(self, item, interval=(0,float("inf"))):
		"""
		return the position of the item in the sequence within the interval of position
		"""
		if item not in self.data:
			return []
		interval=(max(0,interval[0]), min(self.curpos,interval[1]) )
		rd = self.data[item].rank( interval[0]-0.1 )
		rf = self.data[item].rank( interval[1]+0.1 )
		return list(self.data[item][rd:rf].to_array())

	def __str__(self):
		return str(self.data)

class Chroaring (Chronicle):
	"""
	@author: Thomas Guyet
	@date: 01/2020
	@institution: AGROCAMPUS-OUEST/IRISA
	"""

	def __init__(self, emapper=None):
		"""
		- emapper is an event mapper, if not provided, a new one is created
		"""
		Chronicle.__init__(self, emapper)


	################ All occurrences exact recognition #####################
	   
	def __complete_enum__(self, occurrence, gamma, kr, sequence):
		"""
		:kr: recursion level
		:sequence: 
		return a list of occurrences that add the description of the matching of the item_index-th item of the chronicle to the occurrence
		"""
		
		item_index = gamma[kr]
		
		if not item_index in self.sequence: #end of chronicle multiset -> end of recursion
			return [occurrence]
			
		item=self.sequence[ item_index ]
		
		occurrences = []
		seqoccs = sequence.find( self.emapper.event(item), (occurrence[item_index][0], occurrence[item_index][1]))
		
		#print(item_index, item, self.emapper.event(item), occurrence, seqoccs)
				
		#assert(occurrence[item_index][1]<len(sequence))
		for p in seqoccs:
			#create a new occurrence to be modified
			new_occ = occurrence[:]
			new_occ[item_index] = (p,p)
			
			satisfiable=True
			#propagate chronicle constraints
			for k in self.tconst:
				v = self.tconst[k]
				if (k[0]==item_index) and (k[1] in self.sequence) and not (k[1] in gamma):
					#print( new_occ[ k[1] ],"->")
					new_occ[ k[1] ] = (max(new_occ[ k[1] ][0], p+v[0]), min(new_occ[ k[1] ][1], p+v[1]))
					#print( "->", new_occ[ k[1] ])
					if new_occ[ k[1] ][0]>new_occ[ k[1] ][1]: #if empty interval, it is not satisfiable
						satisfiable=False
						break
				elif (k[1]==item_index) and (k[0] in self.sequence) and not (k[0] in gamma):
					#print( new_occ[ k[0] ],"->' (", v,")")
					new_occ[ k[0] ] = (max(new_occ[ k[0] ][0], p-v[1]), min(new_occ[ k[0] ][1], p-v[0]))
					#print( "->'", new_occ[ k[0] ])
					if new_occ[ k[0] ][0]>new_occ[ k[0] ][1]: #if empty interval, it is not satisfiable
						satisfiable=False
						break
					
			if satisfiable:
				#add the occurrence to the list
				occurrences.append( new_occ )
		return occurrences
	
	
	def __recenum__(self, occurrence, gamma, kr, sequence):
		"""
		recursive call for occurrence recognition
		return a list of occurrences recognized from the last_item_index of the chronicle until its last item
		"""

		chro_size=max( self.sequence.keys() )+1
		if kr==chro_size: # final case
			return [occurrence]			

		index = self._next(occurrence, gamma, kr, sequence)
		if index==-1: #next item not found
			return []
		gamma.append(index)
		occurrences = []
		loc_occs = self.__complete_enum__(occurrence, gamma, kr, sequence)
		for occ in loc_occs:
		   reoccs= self. __recenum__(occ, gamma, kr+1, sequence)
		   occurrences.extend(reoccs)
		gamma.pop()
		return occurrences
	
	def __enum(self,sequence):
		"""
		Method that checks whether the chronicle occurs in the sequence 
		sequence: list of event identifiers
		Return a list of occurrences
		"""
		occurrences = [] #list of occurrences
		
		chro_size=max( self.sequence.keys() )+1
		if chro_size==0 :
			return occurrences
		
		k = 0
		gamma= [ self._next([], [], 0, sequence) ]
		item_index = gamma[0]
		item=self.sequence[item_index]
		
		occ=sequence.find( self.emapper.event(item) )
		
		#print(item_index, item, self.emapper.event(item), occ, self.sequence)
		
		for p in occ:
			# create a new occurrence
			new_occ = []
			resize(new_occ, chro_size, (0,sequence.curpos))
			new_occ[item_index] = (p,p)

			# propagate chronicle constraints
			for k in self.tconst:
				v = self.tconst[k]
				if (k[0]==item_index) and (k[1] in self.sequence):
					new_occ[ k[1] ] = (max(0,p+v[0]), min(p+v[1],sequence.curpos))
				elif (k[1]==item_index) and (k[0] in self.sequence):
					new_occ[ k[0] ] = (max(0,p-v[1]), min(p-v[0],sequence.curpos))
			
			# ajouter l'occurrence à la liste des occurrences
			loc_occ = self.__recenum__(new_occ, gamma, 1, sequence)
			occurrences.extend( loc_occ )
				
		return occurrences
		
				
	def enum(self,sequence):
		"""
		Method that checks whether the chronicle occurs in the sequence 
		sequence: list of events
		Return a list of occurrences
		"""
		assert isinstance(sequence, Sequence), 'Argument of wrong type: a Sequence is awaited'
		return self.__enum(sequence)
		'[self.emapper.id(event) if event else None for event in sequence]'
	

if __name__ == "__main__":
	
	
	seq = Sequence()

	seq.append(3)
	seq.append(2)
	seq.append(3,6)
	seq.append(1)
	seq.append(3)
	
	c=Chroaring()
	c.add_event(0,2)
	c.add_event(1,3)
	c.add_event(2,1)
	c.add_constraint(0,1, (4,5))
	print(c)
	
	ret=c.recognize(seq)
	print(ret)
	
	
	
	
