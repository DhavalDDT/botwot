from random import SystemRandom

from pyaib.plugins import keyword

@keyword('insult')
def keyword_insult(context, msg, trigger, args, kargs):
	""" be insulting """
	
	# determine target user
	target_user = ""
	if args:
		target_user = args[0]
	else:
		target_user = msg.sender
	
	# pick a random insult and give it to the target user
	rand = SystemRandom()
	insult = context.config.plugin.insults[rand.randint(0, len(context.config.plugin.insults)-1)]
	msg.reply("%s: %s" % (target_user, insult))
