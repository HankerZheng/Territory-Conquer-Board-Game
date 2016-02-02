import sys
import getopt
from CS561HW1 import gamespace

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
			game_state_temp = game_state.state_copy()
	return max_value

def minimax_algorithm():
	pass

def alpha_beta_pruning():
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
		game_state.move(strategy(game_state,player, cutoff)[1], player)
		for line in game_state.stand_terri_info():
			print line
	else:
		print 'competition'
