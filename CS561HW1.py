import random

class gamespace(object):
#initialize the instance
	def __init__(self, pine_map):
		self.__pines = pine_map		
		self.__territory = [[0 for x in xrange(5)] for x in xrange(5)]	#player should be 1 or 2
		self.__score = [0,0,0]
		self.__score[0] = sum([sum(x) for x in pine_map])

#judgement
	def __is_conquer(self,posi):
		return self.__territory[posi[0]][posi[1]]

	def __is_adjacent_conquer(self,posi,direc):	 #dir = [0,1,2,3,4] [self, Left, Right, Up, Down]
		if direc == 0:
			return self.__territory[posi[0]][posi[1]]
		elif direc == 1:
			if posi[1] - 1 >= 0:
				return self.__territory[posi[0]][posi[1]-1]
			else:
				return 0
		elif direc == 2:
			if posi[1] + 1 <= 4:
				return self.__territory[posi[0]][posi[1]+1]
			else:
				return 0
		elif direc == 3:
			if posi[0] - 1 >= 0:
				return self.__territory[posi[0]-1][posi[1]]
			else:
				return 0
		elif direc == 4:
			if posi[0] + 1 <= 4:
				return self.__territory[posi[0]+1][posi[1]]
			else:
				return 0

#movement
	def __raid(self, posi, player):	#player should be 1 or 2
	#posi_dict initialize
		posi_doct = {1:[0,-1], 2:[0,1], 3:[-1,0], 4:[1,0]}
	#take the territory
		self.__territory[posi[0]][posi[1]] = player
	#calculate the score
		self.__score[player] += self.__pines[posi[0]][posi[1]]
		self.__score[0] -= self.__pines[posi[0]][posi[1]]
		for i in xrange(1,5):
			if self.__is_adjacent_conquer(posi,direc = i) == (3-player):
			#take the territory
				self.__territory[posi[0] + posi_doct[i][0]][posi[1] + posi_doct[i][1]] = player
			#calculate the score
				self.__score[player]     += self.__pines[posi[0] + posi_doct[i][0]][posi[1] + posi_doct[i][1]] 
				self.__score[3 - player] -= self.__pines[posi[0] + posi_doct[i][0]][posi[1] + posi_doct[i][1]] 

	def __sneak(self, posi, player):
	#take the territory
		self.__territory[posi[0]][posi[1]] = player
	#calculate the score
		self.__score[player] += self.__pines[posi[0]][posi[1]]
		self.__score[0] -= self.__pines[posi[0]][posi[1]]

	def move(self, posi, player):
	#return 0 when this input is valid, otherwise, return -1
		if (self.__is_conquer(posi) != 0) or (not player in [1,2]):
			return -1	#posi is already conquer
		#check whether it should be a raid or a sneak
		flag = 0
		for i in xrange(1,5):
			if self.__is_adjacent_conquer(posi,direc = i) == player:
				flag = 1
				break
		if flag == 1:
			self.__raid(posi, player)
			return 0
		else:
			self.__sneak(posi, player)
			return 0
#I/O
	def input_territory(self, input_terri):
	#input_terri is a 5X5 matrix
		for i,line in enumerate(input_terri):
			self.__territory[i] = line

	def update_score(self):
		score = [0,0,0]
		for i in xrange(5):
			for j in xrange(5):
				score[self.__territory[i][j]] += self.__pines[i][j]
		self.__score = score

	def get_score(self):
		return self.__score

	def print_pines(self):
		print 'Pines Distribution:'
		for i in self.__pines:
			print '\t%s' % i

	def stand_terri_info(self):
		output = []
		for i, item in enumerate(self.__territory):
			b = map(str, item)
			a = ''.join(b).replace('0','*')
			b = a.replace('1','X')
			a = b.replace('2','O')
			output.append(a)
		return output

	def print_territory(self):
		print 'Territory Distribution:'
		for i in self.__territory:
			print '\t%s' % i

#copy the instance
	def state_copy(self):
		copy = gamespace(self.__pines)
		copy.__score = [self.__score[0], self.__score[1], self.__score[2]]
		for i in xrange(5):
			for j in xrange(5):
				copy.__territory[i][j] = self.__territory[i][j]
		return copy

'''
1. terverse the point in the map that doesn't belong to any side of the two team. Meanwhile, decide whtether the move should be a Raid or Sneak
2. calculate the point for each unconquerred area
'''
'''
===================
    debug test
-------------------
'''
if __name__ == '__main__':
# initialize
	input_map = [[x for x in xrange(5)] for x in xrange(5)]
	game_test = gamespace(input_map)
	#initialize action pool
	action_pool = []
	for i in xrange(3):
		for j in xrange(4):
			action_pool.append([i,j])
	random.shuffle(action_pool)

	print 'initialize :'
	game_test.print_pines()
	game_test.print_territory()


	print 'test started!'
	for i in xrange(12):
		print '-----Round %2d-----' % i
		moveposi = action_pool.pop()
		print 'Player %d take action at' % (i%2 +1), moveposi
		game_test.move(moveposi, i%2+1)
		game_test.print_territory()
		print game_test.get_score()
		if i == 5:
			one_copy = game_test.state_copy()
		elif i>5:
			one_copy.move(moveposi, i%2+1)

	print game_test.get_score()
	game_test.update_score()
	print game_test.get_score()
	print one_copy.get_score()
'''
=========================================
'''



