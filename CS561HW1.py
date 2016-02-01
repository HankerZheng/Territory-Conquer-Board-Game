import random

class territory(object):
	def __init__(self, input_map):
		self.map = input_map		
		self.north = [[0 for x in xrange(5)] for x in xrange(5)]
		self.west = [[0 for x in xrange(5)] for x in xrange(5)]
	def map_copy(self):
		copy = territory(self, self.map)
		copy.north = self.north
		copy.west = self.west
		return copy

class player(object):
	def __init__(self,side,thismap): #side = 0 == north, 1 == west
		self.__score = 0
		self.__side = side
		self.__map = thismap
		if side == 0:
			self.my_territory = thismap.north
			self.his_territory = thismap.west
		else:
			self.my_territory = thismap.west
			self.his_territory = thismap.north

	def __is_conquer(self,posi):
		if self.my_territory[posi[0]][posi[1]] == 1:
			return 1	#this posi belongs to my terri
		elif self.his_territory[posi[0]][posi[1]] == 1:
			return 2	#this posi belongs to his teri
		else:
			return 0

	def __is_adjacent_conquer(self,posi,direc,owner):	 #dir = [0,1,2,3,4] [self, Left, Right, Up, Down]
		if owner == 0:	#owner = 0 is yourself
			thismap = self.my_territory
		else:			#owner = 1 is the other
			thismap = self.his_territory

		if direc == 0:
			return thismap[posi[0]][posi[1]]
		elif direc == 1:
			if posi[1] - 1 >= 0:
				return thismap[posi[0]][posi[1]-1]
			else:
				return 0
		elif direc == 2:
			if posi[1] + 1 <= 4:
				return thismap[posi[0]][posi[1]+1]
			else:
				return 0
		elif direc == 3:
			if posi[0] - 1 >= 0:
				return thismap[posi[0]-1][posi[1]]
			else:
				return 0
		elif direc == 4:
			if posi[0] + 1 <= 4:
				return thismap[posi[0]+1][posi[1]]
			else:
				return 0


	def __raid(self, posi):
		posi_doct = {1:[0,-1], 2:[0,1], 3:[-1,0], 4:[1,0]}
		self.my_territory[posi[0]][posi[1]] = 1
		for i in xrange(1,5):
			if self.__is_adjacent_conquer(posi,direc = i,owner = 1) == 1:
				self.his_territory[posi[0]+ posi_doct[i][0]][posi[1] + posi_doct[i][1]] = 0
				self.my_territory[posi[0] + posi_doct[i][0]][posi[1] + posi_doct[i][1]] = 1

	def __sneak(self, posi):
		self.my_territory[posi[0]][posi[1]] = 1

	def move(self, posi):
		if self.__is_conquer(posi) != 0:
			return -1	#posi is already conquer
		#check whether it should be a raid or a sneak
		flag = 0
		for i in xrange(1,5):
			if self.__is_adjacent_conquer(posi,direc = i, owner = 0):
				flag = 1
				break
		if flag == 1:
			self.__raid(posi)
			return 0
		else:
			self.__sneak(posi)
			return 0


	def update_score(self):
		score = 0
		for i in xrange(5):
			for j in xrange(5):
				if self.my_territory[i][j]:
					score += self.__map[i][j]
		self.__score = score

	def get_score(self):
		return self.__score

	def print_territroy(self):
		print 'Territory %d:' % self.__side
		for i in self.my_territory:
			print '\t%s' % i

	def state_copy(self):
		copy = player(self.__side, self.__map.copy())
		copy.score = self.__score
		return copy

'''
1. terverse the point in the map that doesn't belong to any side of the two team. Meanwhile, decide whtether the move should be a Raid or Sneak
2. calculate the point for each unconquerred area
3.  
'''
if __name__ == '__main__':
	# initialize
	input_map = [[x for x in xrange(5)] for x in xrange(5)]
	testmap = territory(input_map)
	player0 = player(0,testmap)
	player1 = player(1,testmap)
		#initialize action pool
	action_pool = []
	for i in xrange(3):
		for j in xrange(4):
			action_pool.append([i,j])
	random.shuffle(action_pool)

	print 'initialize :'
	player0.print_territroy()
	player1.print_territroy()

	print 'test started!'
	for i in xrange(12):
		print '-----Round %2d-----' % i
		thisplayer = player0 if (i % 2 == 0) else player1
		thisposi = action_pool.pop()
		thisplayer.move(thisposi)
		print 'After Player%d conquer:' % (i % 2) , thisposi
		thisplayer.print_territroy()




