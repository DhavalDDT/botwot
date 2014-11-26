from pyaib.plugins import keyword, plugin_class

@plugin_class
class Jiggle(object):
	def __init__(self, context, config):
		pass
	
	
	@keyword("jiggle")
	def keyword_jiggle(self, context, msg, trigger, args, kargs):
		""" jiggle that robot ass """
		
		target_user = " ".join(args) or "phalacee"
		
		context.PRIVMSG(
			msg.channel or msg.sender, 
			"\x01ACTION jiggles his robot ass at %s\x01" % target_user 
			)

