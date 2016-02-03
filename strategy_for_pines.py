import sys
import getopt
from CS561HW1 import gamespace


def num_to_axis(posi):
	axis_table = ['A', 'B', 'C', 'D', 'D']
	string = axis_table[posi[1]]+str(posi[0]+1)
	return string

'''
frontier store the state of each node. 
each state can be represented by [move, depth, parent_log]
	move: 		the action taken by this node
	depth: 		the search depth of this node
	parent_log: a list of posi, which tells how to get to the game_state of this node's parent from root_state
	prev_bro:	the youngest elder brother's move
'''
def create_frontier(game_state, cur_frontier, cur_depth, parent_log):
	old_posi = [-1,-1]
	for i in xrange(4,-1,-1):
		for j in xrange(4,-1,-1):
			if game_state.is_conquer([i,j]) != 0 :
				continue
			#parent_log is a address, we have to allocate a new space for different parent_log
			log = list(parent_log)
			cur_frontier.append({'move':[i,j], 'depth':cur_depth+1, 'parent_log':log, 'prev_bro':old_posi})
			old_posi = [i,j]
	return None


#algorithm
def greedy_algorithm(game_state, player, cutoff):
#return a position to move into
	max_value = [-sys.maxint-1,[0,0]]
	game_state_temp = game_state.state_copy()
	for i in xrange(5):
		for j in xrange(5):
			if game_state_temp.move([i,j], player) == -1 :
				continue
			cur_value = game_state_temp.get_score()[player] - game_state_temp.get_score()[3-player]
			if cur_value > max_value[0]:
				max_value[0] = cur_value
				max_value[1] = [i,j]
			del game_state_temp
			game_state_temp = game_state.state_copy()
	return max_value


def minimax_algorithm(game_state, player, cutoff):	
	max_value = [-sys.maxint-1, [0,0]]
	min_value = [sys.maxint   , [0,0]]

	root_state = game_state.state_copy()
#initialize flag and parameter for loop
	frontier, best_move, last_depth= [], [], 0
	create_frontier(game_state = root_state, cur_frontier = frontier, cur_depth = 0, parent_log = [])
	for i in xrange(cutoff):
		#best_move[depth] store the best_move for each depth
		best_move.append( min_value if i%2 else max_value)

	while len(frontier) != 0:
		this_node = frontier.pop()
		this_game_state = root_state.state_copy()
		for i, posi in enumerate(this_node['parent_log']):
			thisplayer = player if i%2==0 else (3-player)
			this_game_state.move(posi, thisplayer)
		this_game_state.move(this_node['move'], player if this_node['depth']%2 else (3-player))

		if this_node['depth'] == cutoff:
		#when reach the cutoff depth, don't expand the node, just calculate the score and update best_move
			this_value = this_game_state.get_score()[player] - this_game_state.get_score()[3-player]
			if this_node['depth']%2:
			#search for max score
				if this_value > best_move[this_node['depth'] - 1][0]:
					best_move[this_node['depth'] - 1] = [this_value, this_node['move']]
			else:
			#search for min score
				if this_value < best_move[this_node['depth'] - 1][0]:
					best_move[this_node['depth'] - 1] = [this_value, this_node['move']]
			fh.write('%5s %s %s\n' % (this_node['move'], this_node['depth'], best_move))
		else:
		#it's not the cutoff depth, continue expand this node
			this_node['parent_log'].append(this_node['move'])
			create_frontier(game_state = this_game_state, cur_frontier = frontier, cur_depth = this_node['depth'], parent_log = this_node['parent_log'])
			if this_node['depth'] < last_depth:
			#if it is going up,
				#terverse its parent
				#update best_move both this depth and upper depth. upper depth's posi is defined by p_move
				a = min(best_move[this_node['depth'] - 1], [best_move[this_node['depth']][0],this_node['prev_bro']]) 
				b = max(best_move[this_node['depth'] - 1], [best_move[this_node['depth']][0],this_node['prev_bro']]) 
				best_move[this_node['depth'] - 1] = b if this_node['depth']%2 else a
				best_move[this_node['depth']] = min_value if this_node['depth']%2 else max_value
				fh.write('%5s %s %s\n' % (this_node['move'], this_node['depth'], best_move))
		last_depth = this_node['depth']
		#p_move: the last step to get to parent state, used to update best_move when more optimal
		del this_game_state
	print best_move
	return best_move[0]


def alpha_beta_pruning(game_state, player, cutoff):
	pass

#file I/O
def read_file_input(f_path):
	pine_map = []
	terri_map = []
	fh = open(f_path,'r')
	lines = fh.read().splitlines()
	fh.close()
	if len(lines) == 13:
		for i, line in enumerate(lines):
			if i <= 0: 
				strategy = int(line) - 1
			elif i <= 1:
				if line == 'X':
					player = 1
				elif line == 'O':
					player = 2
			elif i <= 2:
				cutoff = int(line)
			elif i <= 7:
				pine_map.append(map(int,line.split()))
			elif i <= 12:
				tmp = line.replace('*','0 ')
				tmp = tmp.replace('X','1 ')
				tmp = tmp.replace('O','2 ')
				terri_map.append(map(int,tmp.split()))
		return {'strategy':strategy, 'player':player, 'cutoff':cutoff, 'pine_map':pine_map, 'terri_map':terri_map, 'lines': len(lines)}
	else:
		for i, line in enumerate(lines):
			if i <= 0:
				battle_num = int(line)
			elif i <= 1:
				if line == 'X':
					player1 = 1
				elif line == 'O':
					player1 = 2
			elif i <= 2:
				strategy1 = int(line) - 1
			elif i <= 3:
				cutoff1 = int(line)
			elif i <= 4:
				if line == 'X':
					player2 = 1
				elif line == 'O':
					player2 = 2
			elif i <= 5:
				strategy2 = int(line) - 1
			elif i <= 6:
				cutoff2 = int(line)
			elif i <= 11:
				pine_map.append(map(int,line.split()))
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
	fh = open('output.txt','w')
	# assign value from input file
	if data['lines'] == 13:
		strategy = strategy_pool[data['strategy']]
		player = data['player']
		cutoff = data['cutoff']
		pine_map = data['pine_map']
		terri_map = data['terri_map']
	else:
		player = data['player']	#player[0] means first, player[1] means second
		strategy = [strategy_pool[data['strategy'][0]], strategy_pool[data['strategy'][1]] ]
		cutoff = data['cutoff']
		pine_map = data['pine_map']
		terri_map = data['terri_map']
	#update info in gamespac
	game_state = gamespace(pine_map)
	game_state.input_territory(terri_map)
	game_state.update_score()

#start action
	if data['lines'] == 13:
		next_move = strategy(game_state,player, cutoff)[1]
		print next_move
		game_state.move(next_move, player)
		for line in game_state.stand_terri_info():
			print line
	else:
		print 'competition'
