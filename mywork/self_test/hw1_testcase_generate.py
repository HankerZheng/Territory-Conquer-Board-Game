import sys, os, random
sys.path.append('../')
from file_compare import file_compare
from game_space import gamespace


def test_part1_generate(num):
	for i in xrange(num):
		#create the file
		test_file = open('.\\part1_test\\%d.txt' % i, 'w')
		#generate the parameter randomly
		tasknum = random.randint(1,3)
		player = random.choice(['X','O'])
		cutoff = random.randint(min_cutoff ,max_cutoff)
		board_grid_value = [[random.randint(1,99) for i in xrange(5)] for j in xrange(5)]
		this_move_pool = list(move_pool)
		random.shuffle(this_move_pool)
		current_move = random.randrange(min_move, max_move, 2) if player == 'X' else random.randrange(min_move, max_move,2)
		game_state = gamespace(board_grid_value)
		this_player = 1
		for i in range(current_move):
			game_state.move(this_move_pool.pop(),this_player)
			this_player = 3 - this_player
		current_board_state = game_state.stand_terri_info()
		#write the parameter into file
		test_file.write('%d\n'%tasknum)
		test_file.write('%s\n'%player)
		test_file.write('%d\n'%cutoff)
		for line in board_grid_value:
			test_file.write('%s\n'%' '.join(map(str,line)))
		for i, line in enumerate(current_board_state):
			if i == 4:		test_file.write('%s' % line)
			else:			test_file.write('%s\n' % line)
		test_file.close()




def test_part2_generate(num):
	for i in xrange(num):
		#create the file
		test_file = open('.\\part2_test\\%d.txt' % i, 'w')
		#generate the parameter randomly
		tasknum = 4
		fir_player = random.choice(['X','O'])
		fir_p_algo = random.randint(1,3)
		fir_cutoff = random.randint(min_cutoff,max_cutoff)
		sec_player = 'X' if fir_player == 'O' else 'O'
		sec_p_algo = random.randint(1,3)
		sec_cutoff = random.randint(min_cutoff,max_cutoff)
		board_grid_value = [[random.randint(1,99) for i in xrange(5)] for j in xrange(5)]
		this_move_pool = list(move_pool)
		random.shuffle(this_move_pool)
		current_move = random.randrange(min_move, max_move, 2) if fir_player == 'X' else random.randrange(min_move, max_move, 2)
		game_state = gamespace(board_grid_value)
		this_player = 1
		for i in range(current_move):
			game_state.move(this_move_pool.pop(),this_player)
			this_player = 3 - this_player
		current_board_state = game_state.stand_terri_info()
		#write the parameter into file
		test_file.write('%d\n'%tasknum)
		test_file.write('%s\n'%fir_player)
		test_file.write('%d\n'%fir_p_algo)
		test_file.write('%d\n'%fir_cutoff)
		test_file.write('%s\n'%sec_player)
		test_file.write('%d\n'%sec_p_algo)
		test_file.write('%d\n'%sec_cutoff)
		for line in board_grid_value:
			test_file.write('%s\n'%' '.join(map(str,line)))
		for i, line in enumerate(current_board_state):
			if i == 4:		test_file.write('%s' % line)
			else:			test_file.write('%s\n' % line)
		test_file.close()


min_cutoff = 1
max_cutoff = 4
min_move = 2
max_move = 23

move_pool = []
for i in xrange(5):
	for j in xrange(5):
		move_pool.append([i,j])
test_part1_generate(100)
test_part2_generate(100)