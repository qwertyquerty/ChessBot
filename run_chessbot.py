from chessbot.config import *
from chessbot.bot import ChessBot

from multiprocessing import Process

from time import sleep

def begin_process(pid):
	bot = ChessBot(
		pid = pid, 
		max_messages = MAX_MESSAGE_CACHE,
		shard_ids = list(range(SHARDS_PER_PROCESS * pid, SHARDS_PER_PROCESS * (pid+1))),
		shard_count = PROCESSES * SHARDS_PER_PROCESS
	)

	bot.run(BOTTOKEN)

processes = {}

if __name__ == '__main__':
	for pid in range(PROCESSES):
		p = Process(target=begin_process, args=(pid,))
		processes[pid] = p
		p.start()

	
	while 1:
		sleep(1)
		for pid in list(processes.keys()):
			if not processes[pid].is_alive():
				print("Process {} failed! Restarting...".format(pid))

				del processes[pid]

				p = Process(target=begin_process, args=(pid,))
				processes[pid] = p
				p.start()

