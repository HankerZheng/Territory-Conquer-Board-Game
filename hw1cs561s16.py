import sys
import random

class gamespace(object):
#initialize the instance
	def __init__(self, pine_map):
		self.__pines = pine_map		
		self.__territory = [[0 for x in xrange(5)] for x in xrange(5)]	#player should be 1 or 2
		self.__score = [0,0,0]
		self.__score[0] = sum([sum(x) for x in pine_map])

#judgement
	def step_allowed(self):
		depth_max = 0
		for i in xrange(5):
			for j in xrange(5):
				if self.__territory[i][j] == 0:
					depth_max += 1
		return depth_max

	def is_conquer(self,posi):
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
		if (self.is_conquer(posi) != 0) or (not player in [1,2]):
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


def num_to_axis(posi):
	axis_table = ['A', 'B', 'C', 'D', 'E']
	string = axis_table[posi[1]]+str(posi[0]+1)
	return string

def str_infi(value):
	if value <= -sys.maxint-1:	return '-Infinity'
	elif value >= sys.maxint:	return 'Infinity'
	else:						return str(value)

def traverse_log_minimax(posi, depth, value):
	string = list()
	string = ['root'] if depth == 0 else [num_to_axis(posi)]
	string.append(str_infi(depth))
	string.append(str_infi(value))
	return ','.join(string)

def traverse_log_alpha_beta(posi, depth, value):
	string = list()
	string = ['root'] if depth == 0 else [num_to_axis(posi)]
	string.append(str_infi(depth))
	string.append(str_infi(value[0]))
	string.append(str_infi(value[2]))
	string.append(str_infi(value[3]))
	return ','.join(string)

#return the min. return val1 if equal
def my_min(val1, val2):
	if val1[0] <= val2[0]:	return val1
	else:					return val2

#return the max. return val1 if equal
def my_max(val1, val2):
	if val1[0] >= val2[0]:	return val1
	else:					return val2

def not_in_alpha_beta(this_value, value):
	if this_value[0] > value[2] and this_value[0] < value[3]:
	# this_value is in the between of alpha and beta
		return 0
	elif this_value[0] <= value[2]:
	# this_value is less than alpha
		return -1
	else:
	# this_value is larger than beta
		return 1

#	frontier store the state of each node. 
#	each state can be represented by [move, depth, parent_log]
#		move: 		the action taken by this node
#		depth: 		the search depth of this node
#		parent_log: a list of posi, which tells how to get to the game_state of this node's parent from root_state
def create_frontier(game_state, cur_frontier, cur_depth, parent_log):
	frontier = []
	for i in xrange(5):
		for j in xrange(5):
			if game_state.is_conquer([i,j]) != 0:	continue
			#parent_log is a address, we have to allocate a new space for different parent_log
			frontier.append({'move':[i,j], 'depth':cur_depth+1, 'parent_log':list(parent_log)})
	#have to reverse it because we get one node by popping from the frontier, which is from the end to the front
	frontier.reverse()
	cur_frontier += frontier
	return None


#algorithm
#return a position to move into
def greedy_algorithm(game_state, player, cutoff, trace):
	max_value = [-sys.maxint-1,[0,0]]
	game_state_temp = game_state.state_copy()
	for i in xrange(5):
		for j in xrange(5):
			if game_state_temp.move([i,j], player) == -1:	continue
			cur_value = game_state_temp.get_score()[player] - game_state_temp.get_score()[3-player]
			if cur_value > max_value[0]:
				max_value[0] = cur_value
				max_value[1] = [i,j]
			del game_state_temp
			game_state_temp = game_state.state_copy()
	return max_value[1]

def minimax_algorithm(game_state, player, cutoff, trace):	
	max_value = [-sys.maxint-1, [0,0]]
	min_value = [sys.maxint   , [0,0]]
	depth_max = game_state.step_allowed()
	cutoff = cutoff if cutoff < depth_max else depth_max

	root_state = game_state.state_copy()
	#initialize frontier, best_move, last_depth for loop
	frontier, best_move, last_depth= [], [], 0
	create_frontier(game_state = root_state, cur_frontier = frontier, cur_depth = 0, parent_log = [])
	for i in xrange(cutoff+1):
	#best_move[depth] store the best_move for each depth
		best_move.append( list(min_value) if i%2 else list(max_value))	
	if trace:
		fh_tl.write('Node,Depth,Value')
		fh_tl.write('\n%s' % traverse_log_minimax([], 0, best_move[0][0]))

	#main loop, search down to the cutoff depth
	while len(frontier) != 0:
		this_node = frontier.pop()
		this_depth = this_node['depth']
		#get the game state for this node
		this_game_state = root_state.state_copy()
		for i, posi in enumerate(this_node['parent_log']):
			thisplayer = player if i%2==0 else (3-player)
			this_game_state.move(posi, thisplayer)
		this_game_state.move(this_node['move'], player if this_depth%2 else (3-player))

		if this_depth == cutoff:
		#when reach the cutoff depth, don't expand the node, just calculate the score and update best_move
			this_value = this_game_state.get_score()[player] - this_game_state.get_score()[3-player]
			best_move[this_depth][0] = this_value
			if (trace):	fh_tl.write( '\n%s'% traverse_log_minimax(this_node['move'], this_depth, this_value))

			#depth for this node to retrospect			
			retro_depth = 1 if len(frontier) == 0 else frontier[len(frontier)-1]['depth']
			last_parent = this_node['move']
			#update best_move both this depth and all its upper depth.
			for depth in xrange(this_depth,retro_depth - 1,-1):	
			#depth, depth-1, depth-2, ..., 1
				#terverse its parent
				parent_move = this_node['parent_log'].pop() if len(this_node['parent_log']) else []
				#update the best_move
				less_val   = my_min(best_move[depth - 1], [best_move[depth][0],last_parent]) 
				larger_val = my_max(best_move[depth - 1], [best_move[depth][0],last_parent])
				best_move[depth - 1] = larger_val if depth%2 else less_val
				if (trace):	fh_tl.write( '\n%s'% traverse_log_minimax(parent_move, depth-1, best_move[depth - 1][0]))
				last_parent = parent_move
		else:
		#it's not the cutoff depth, continue expand this node			
			this_node['parent_log'].append(this_node['move'])
			create_frontier(game_state = this_game_state, cur_frontier = frontier, cur_depth = this_depth, parent_log = this_node['parent_log'])
			best_move[this_depth] = list(min_value) if this_depth%2 else list(max_value)
			if (trace):	fh_tl.write( '\n%s'% traverse_log_minimax(this_node['move'], this_depth, best_move[this_depth][0]))
		#before finish one loop, delete the redundant memory	
		del this_game_state
	return best_move[0][1]


#if this depth is in search for MAX value, then only update the left  side of bound, that is alpha
#if this depth is in search for MIN value, then only update the right side of bound, that is beta
#if MAX searching line, exceeding the alpha(left) bound, ignore it
#						exceeding the beta(right) bound, prune the leave without propagate to grandparent
#if MIN searching line, exceeding the alpha(left) bound, prune the leave without propagate to grandparent
#						exceeding the beta(right) bound, ignore it
def alpha_beta_pruning(game_state, player, cutoff, trace):
	max_value = [-sys.maxint-1, [0,0], -sys.maxint-1, sys.maxint]
	min_value = [sys.maxint   , [0,0], -sys.maxint-1, sys.maxint]
	depth_max = game_state.step_allowed()
	cutoff = cutoff if cutoff < depth_max else depth_max

	root_state = game_state.state_copy()
	#initialize frontier, best_move, last_depth for loop
	frontier, best_move, last_depth= [], [], 0
	create_frontier(game_state = root_state, cur_frontier = frontier, cur_depth = 0, parent_log = [])
	for i in xrange(cutoff+1):
	#best_move[depth] store the best_move for each depth
		best_move.append( list(min_value) if i%2 else list(max_value))	
	if (trace):	
		fh_tl.write('Node,Depth,Value,Alpha,Beta')
		fh_tl.write('\n%s' % traverse_log_alpha_beta([], 0, best_move[0]))

	#main loop, search down to the cutoff depth
	while len(frontier) != 0:
		this_node = frontier.pop()
		this_depth = this_node['depth']
		#get the game state for this node
		this_game_state = root_state.state_copy()
		for i, posi in enumerate(this_node['parent_log']):
			thisplayer = player if i%2==0 else (3-player)
			this_game_state.move(posi, thisplayer)
		this_game_state.move(this_node['move'], player if this_depth%2 else (3-player))

		if this_depth == cutoff:
		#when reach the cutoff depth, don't expand the node, just calculate the score and update best_move
			#traverse this node -- print info in this node
			best_move[this_depth] = [this_game_state.get_score()[player] - this_game_state.get_score()[3-player]] + \
									 list(best_move[this_depth-1][1:4])
			if (trace):	fh_tl.write( '\n%s'% traverse_log_alpha_beta(this_node['move'], this_depth, best_move[this_depth]))
			#prune test!
			prune_check = not_in_alpha_beta(best_move[this_depth], best_move[this_depth-1])
			if (prune_check == 1 and (this_depth-1)%2 == 0) or (prune_check == -1 and (this_depth-1)%2 == 1):
			# this value exceeds the right bound of MAX searching line or
			# this value exceeds the left  bound of MIN searching line 		PRUNING
				next_node = {'depth': 0} if len(frontier) == 0 else frontier.pop()
				while next_node['depth'] == this_depth:
					next_node = {'depth': 0} if len(frontier) == 0 else frontier.pop()
				if next_node['depth'] != 0:
					frontier.append(next_node)
				best_move[this_depth-1][0] = best_move[this_depth][0]

			#depth for this node to retrospect			
			retro_depth = 1 if len(frontier) == 0 else frontier[len(frontier)-1]['depth']
			last_parent = this_node['move']

			for depth in xrange(this_depth,retro_depth - 1,-1):	
			#depth, depth-1, depth-2, ..., 1
				#terverse its parent
				parent_move = this_node['parent_log'].pop() if len(this_node['parent_log']) else []
				#update the best_move
				prune_check = not_in_alpha_beta(best_move[depth], best_move[depth-1])
				if (depth-1)%2 == 1:
				#parent depth is searching for MIN
					if prune_check == 0:
					#best_move[this_depth][0] is in bound
						best_move[depth-1][3] = best_move[depth][0]
						best_move[depth-1][1] = last_parent
						best_move[depth-1][0] = best_move[depth][0]
					#best_move[this_depth][0] is larger than beta, do nothing
				else:
				#parent depth is searching for MAX
					if prune_check == 0:
					#best_move[this_depth][0] is in bound
						best_move[depth-1][2] = best_move[depth][0]
						best_move[depth-1][1] = last_parent
						best_move[depth-1][0] = best_move[depth][0]
					#best_move[this_depth][0] is less than alpha, do nothing
				if trace:	fh_tl.write( '\n%s'% traverse_log_alpha_beta(parent_move, depth-1, best_move[depth - 1]))
				last_parent = parent_move

		else:
		#it's not the cutoff depth, continue expand this node			
			this_node['parent_log'].append(this_node['move'])
			create_frontier(game_state = this_game_state, cur_frontier = frontier, cur_depth = this_depth, parent_log = this_node['parent_log'])
			#best_move is set to default for next expand according to depth
			best_move[this_depth][2:4] = list(best_move[this_depth-1][2:4])				#[alpha, beta] inherits from its parent
			best_move[this_depth][0:2] = list(min_value[0:2]) if this_depth%2 else list(max_value[0:2])
			if trace:	fh_tl.write( '\n%s'% traverse_log_alpha_beta(this_node['move'], this_depth, best_move[this_depth]))
		#before finish one loop, delete the redundant memory	
		del this_game_state
	return best_move[0][1]

#file I/O
def read_file_input(f_path):
	pine_map = []
	terri_map = []
	fh = open(f_path,'r')
	lines = fh.read().splitlines()
	fh.close()
	if len(lines) == 13:
		for i, line in enumerate(lines):
			if i <= 0:		strategy = int(line) - 1
			elif i <= 1:
				if line == 'X':		player = 1
				elif line == 'O':	player = 2
			elif i <= 2:	cutoff = int(line)
			elif i <= 7:	pine_map.append(map(int,line.split()))
			elif i <= 12:
				tmp = line.replace('*','0 ')
				tmp = tmp.replace('X','1 ')
				tmp = tmp.replace('O','2 ')
				terri_map.append(map(int,tmp.split()))
		return {'strategy':strategy, 'player':player, 'cutoff':cutoff, 'pine_map':pine_map, 'terri_map':terri_map, 'lines': len(lines)}
	else:
		for i, line in enumerate(lines):
			if i <= 0:		battle_num = int(line)
			elif i <= 1:
				if line == 'X':		player1 = 1
				elif line == 'O':	player1 = 2
			elif i <= 2:	strategy1 = int(line) - 1
			elif i <= 3:	cutoff1 = int(line)
			elif i <= 4:
				if line == 'X':		player2 = 1
				elif line == 'O':	player2 = 2
			elif i <= 5:	strategy2 = int(line) - 1
			elif i <= 6:	cutoff2 = int(line)
			elif i <= 11:	pine_map.append(map(int,line.split()))
			elif i <= 16:
				tmp = line.replace('*','0 ')
				tmp = tmp.replace('X','1 ')
				tmp = tmp.replace('O','2 ')
				terri_map.append(map(int,tmp.split()))
		return {'battle_num':battle_num, 'player':[player1,player2], 'strategy':[strategy1,strategy2],
				'cutoff':[cutoff1,cutoff2], 'pine_map':pine_map,'terri_map':terri_map, 'lines': len(lines)}


if __name__ == '__main__':
#initialization
	strategy_pool = [greedy_algorithm, minimax_algorithm, alpha_beta_pruning]
	input_f_path = sys.argv[2]
	# read from the INPUT file
	data = read_file_input(input_f_path)
	# assign value from input file
	if data['lines'] == 13:
		strategy = strategy_pool[data['strategy']]
		player = data['player']
		cutoff = data['cutoff']
		pine_map = data['pine_map']
		terri_map = data['terri_map']
		if data['strategy']:	fh_tl = open('traverse_log.txt','w')
		fh_ns = open('next_state.txt','w')
	else:
		player = data['player']	#player[0] means first, player[1] means second
		strategy = [strategy_pool[data['strategy'][0]], strategy_pool[data['strategy'][1]] ]
		cutoff = data['cutoff']
		pine_map = data['pine_map']
		terri_map = data['terri_map']
		fh_ts = open('trace_state.txt','w')
	#update info in gamespac
	game_state = gamespace(pine_map)
	game_state.input_territory(terri_map)
	game_state.update_score()

#start action
	if data['lines'] == 13:
		next_move = strategy(game_state,player, cutoff, 1)
		game_state.move(next_move, player)
		for i, line in enumerate(game_state.stand_terri_info()):
			if i == 0:	fh_ns.write('%s'%line)
			else:		fh_ns.write('\n%s'%line)
		if data['strategy']:	fh_tl.close()
		fh_ns.close()
	else:
		player_index = 0
		while game_state.step_allowed():
			next_move = strategy[player_index](game_state, player[player_index], cutoff[player_index], 0)
			game_state.move(next_move, player[player_index])
			#print this state
			for i, line in enumerate(game_state.stand_terri_info()):
				if i == 0:	fh_ts.write('%s'%line)
				else:		fh_ts.write('\n%s'%line)
			player_index = 1 - player_index		#0,1,0,1,0,....
			if game_state.step_allowed():	fh_ts.write('\n')
		fh_ts.close()