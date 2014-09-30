import wolframalpha

from pyaib.plugins import keyword

@keyword('wa')
def keyword_wolframalpha(context, msg, trigger, args, kargs):
	""" look up wolfram alpha """
	
	if msg.sender == "Zachary_DuBois":
		msg.reply("%s: blerg" % target_user)
	else:
		# figure out first who to target and what the query is
		target_user = ""
		query = ""
		if len(args) >= 3 and args[-2] == "|":
			target_user = args[-1]
			query = " ".join(args[:-2])
		else:
			target_user = msg.sender
			query = " ".join(args)
		
		wa = wolframalpha.Client(context.config.plugin.wa.appid)
		res = wa.query(query)
		if len(res.pods) > 1:
			msg.reply("%s: %s" % (target_user, res.pods[1].text))
		else:
			msg.reply("%s: no results" % target_user)

