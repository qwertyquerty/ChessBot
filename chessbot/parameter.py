import re
from bson.objectid import ObjectId

class Parameter():
	type_name = "object"
	name = "arg"
	required = True

	def __init__(self, name = None, required = True):
		self.required = required
		if name:
			self.name = name
	
	def parse(self, ctx, arg):
		return None

class ParamUser(Parameter):
	type_name = "user"
	name = "user"

	def parse(self, ctx, arg):
		mention_re = re.search(r"^<@!?(\d+)>$", arg)
		id_re = re.search(r"^(\d+)$", arg)

		id = None

		if mention_re:
			id = mention_re.group(1)
		elif id_re:
			id = id_re.group(1)
		
		try:
			id = int(id)
		except:
			id = None
		
		return ctx.bot.get_user(id)

class ParamGameID(Parameter):
	type_name = "game_id"
	name = "game"

	def parse(self, ctx, arg):
		try:
			ObjectId(arg)
			return arg
		except:
			return None

class ParamString(Parameter):
	type_name = "text"
	name = "text"

	def parse(self, ctx, arg):
		return str(arg)

class ParamInt(Parameter):
	type_name = "number"
	name = "number"

	def parse(self, ctx, arg):
		try:
			return int(arg)
		except:
			return None

# This is probably a terrible idea, still think I'm a genius for it though
# You know you're doing something wrong when you self roll type unions
class ParamUnion(Parameter):
	name = "query"
	def __init__(self, params, name=None, required=False):
		super(ParamUnion, self).__init__(name, required)

		self.params = params
		self.type_name = "/".join([param.type_name for param in self.params])

		if not name:
			self.name = "/".join([param.name for param in self.params])
	
	def parse(self, ctx, arg):
		for param in self.params:
			parsed = param.parse(ctx, arg)
			if parsed:
				return parsed
		
		return None