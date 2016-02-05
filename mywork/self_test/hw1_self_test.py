import sys, os, random
sys.path.append('../')
from file_compare import file_compare
# from game_space import gamespace

def main():
	for ipart in ['part1_test','part2_test']:
		for itest in range(0,100):
			os.chdir('.\\Hongtai')
			os.popen('python .\\hw1_test.py -i ..\\%s\\%d.txt' % (ipart,itest))
			os.chdir('..\\Han')
			os.popen('python .\\hw1cs561s16.py -i ..\\%s\\%d.txt'% (ipart,itest))
			os.chdir('..')

			input_file=open('.\\'+ipart+'\\%d.txt' % itest, 'r')
			lines=input_file.readline()
			input_file.close()
			task=int(lines.strip())
			if task==1:
				target_file=['next_state.txt']
			elif task==2 or task==3:
				target_file=['traverse_log.txt','next_state.txt']
			elif task==4:
				target_file=['trace_state.txt']
			for itarget in target_file:
				print 'start compare',ipart,itest
				target1='.\\Hongtai\\'+itarget
				target2='.\\Han\\'+itarget
				ret_val= file_compare(target1, target2, itarget)
				if ret_val==0:
					return

main()