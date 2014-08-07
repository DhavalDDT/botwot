from random import SystemRandom

from pyaib.plugins import keyword

@keyword('insult')
def keyword_insult(context, msg, trigger, args, kargs):
	""" be insulting """
	
	# determine target user
	target_user = " ".join(args) or msg.sender
	
	# pick a random insult and give it to the target user
	rand = SystemRandom()
	insult = context.config.plugin.insults[rand.randint(0, len(context.config.plugin.insults)-1)]
	msg.reply("%s: %s" % (target_user, insult))
