from chessbot import config
from chessbot.config import *
from chessbot.util import *

from pymongo import MongoClient
import datetime
import random

import chess
from bson.objectid import ObjectId
import chess.variant
import chess.pgn

client = MongoClient()
db = client.chess

users = db.users
guilds = db.guilds
games = db.games


users.create_index("id",unique=True)
guilds.create_index("id",unique=True)
games.create_index("timestamp")

class DBObject():

	collection = None

	def __init__(self, d):
		if d:
			self.exists = True
			self._id = d["_id"]
		else:
			self.exists = False

	@classmethod
	def from_id(cls,id):
		d = cls.collection.find_one({"_id": ObjectId(id)})
		return cls(d)

	def __bool__(self):
		return self.exists

	def __str__(self):
		return str(self.__dict__)

	def __repr__(self):
		return self.__str__()

	def set(self,key,val):
		self.collection.update_one({"_id": ObjectId(self._id)},{"$set": {key:val}})

	def push(self,key,val):
		self.collection.update_one({"_id": ObjectId(self._id)},{"$push": {key:val}})

	def pull(self,key,val):
		self.collection.update_one({"_id": ObjectId(self._id)},{"$pull": {key:val}})

	def inc(self,key,val):
		self.collection.update_one({"_id": ObjectId(self._id)},{"$inc": {key:val}})

	def pop(self,key,val):
		self.collection.update_one({"_id": ObjectId(self._id)},{"$pop": {key:val}})

	def delete(self):
		self.collection.delete_one({"_id": ObjectId(self._id)})

class Game(DBObject):

	collection = db.games

	def __init__(self,d):
		super().__init__(d)
		if not self.exists: return

		self.basefen = d["fen"]
		self.variant = d["variant"]
		self.board = get_base_board(self)

		self.moves = d["moves"]
		for move in self.moves:
			self.board.push(chess.Move.from_uci(move))

		self.fen = self.board.fen()
		self.winner = d["winner"]
		self.loser = d["loser"]
		self.outcome = d["outcome"]
		self.done = self.outcome != OUTCOME_UNFINISHED
		self.p1 = d["1"]
		self.p2 = d["2"]
		self.white = d["1"]
		self.black = d["2"]
		self.players = [self.black,self.white]
		self.id = d["_id"]
		self.ranked = d["ranked"]
		self.valid = d["valid"]
		self.timestamp = d["timestamp"]


	@classmethod
	def new(cls,u1,u2, variant=VARIANT_STANDARD, fen=None, rated=True):
		if fen == None:
			if variant == VARIANT_RACINGKINGS:fen = chess.variant.RacingKingsBoard().fen()
			elif variant == VARIANT_HORDE:fen = chess.variant.HordeBoard().fen()
			elif variant == VARIANT_960:
				holder = chess.Board(chess960=True)
				boar_num = random.randint(0,960)
				holder.set_chess960_pos(boar_num)
				fen = holder.fen()
			else: fen = chess.Board().fen()
		data = {"fen": fen, "moves": [], "winner": None, "loser": None, "outcome": OUTCOME_UNFINISHED, "1": u1, "2": u2, "ranked": rated, "valid": True, "timestamp": datetime.datetime.utcnow(), "variant": variant}
		games.insert_one(data)
		return Game.from_user_id(u1)

	@classmethod
	def from_user_id(cls,userid):
		d = games.find_one({"$or": [{"$and":[{"1":userid},{"outcome": OUTCOME_UNFINISHED}]},  {"$and":[{"2":userid},{"outcome": OUTCOME_UNFINISHED}]}]})
		return cls(d)

	@classmethod
	def from_user_id_recent(cls,userid):
		try:
			d = games.find({"$or": [{"1":userid}, {"2":userid}]}).sort('timestamp',-1).next()
		except:
			d = None
		return cls(d)

	def add_move(self, move):
		self.push("moves", move)

	def end(self, winner, loser, outcome):
		self.set("winner", winner)
		self.set("loser", loser)
		self.set("outcome", outcome)

	def pgn(self):
		board = get_base_board(self)
		pb = chess.pgn.Game().without_tag_roster()
		pb.setup(board)
		pb.headers["Site"] = BOTURL
		pn = pb
		for i in self.moves:
			pn = pn.add_variation(chess.Move.from_uci(i))
		return pb



class User(DBObject):

	collection = db.users

	def __init__(self,d):
		super().__init__(d)
		if not self.exists: return

		self.name = d["name"]
		self.id = d["id"]
		self._id = d["_id"]

		### STUFF THAT RELIES ON FETCHING GAMES THAT WE WILL LAZY LOAD WHEN NEEDED ###
		self._list_of_games = None
		self._badges = None
		
		self.votes = d["votes"]
		self.bio = d["bio"]
		self.flags = d["flags"]
		self.rating = d["rating"]
		self.rating_deviation = d["rating_deviation"]
		self.rating_volatility = d["rating_volatility"]
		self.glicko = glicko_env.create_rating(self.rating, self.rating_deviation, self.rating_volatility)
		self.level = d["level"]

	@classmethod
	def from_user_id(cls,userid):
		d = db.users.find_one({"id": userid})
		return cls(d)

	@classmethod
	def new(cls,userid,name):
		rating = glicko_env.create_rating()

		data = {"name": name, "id": userid, "flags": 0, "votes": 0, "bio": None, "rating": rating.mu, "rating_deviation": rating.phi, "rating_volatility": rating.sigma, "level": 0}
		users.insert_one(data)

		return User.from_user_id(userid)

	@classmethod
	def from_mem(cls,mem):
		d = User.from_user_id(mem.id)
		if not d:
			return User.new(mem.id, str(mem))
		else:
			return d

	@classmethod
	def from_name(cls,name):
		d = db.users.find_one({"name": name})
		return cls(d)

	def get_games(self):
		gs = games.find({"$or": [{"1":self.id},{"2":self.id}]}).sort('timestamp',-1)
		out = []
		for game in gs:
			out.append(Game(game))
		return out

	def delete_games(self):
		d = games.delete_many({"$or": [{"1":self.id},{"2":self.id}]})
		return d

	def blacklist(self):
		db.games.update_many({"$or": [{"1":self.id}, {"2":self.id}]}, {"$set": {"valid": False}})
		self.set('flags', self.flags|USER_FLAG_BLACKLISTED)
		rating_sync()
		return self

	def unblacklist(self):
		db.games.update_many({"$or": [{"1":self.id}, {"2":self.id}]}, {"$set": {"valid": True}})
		self.set('flags', self.flags&~USER_FLAG_BLACKLISTED)
		rating_sync()
		return self
	
	def get_rank(self):
		rank_cur = db.users.find().sort("rating", -1)
		i = 0

		for user in rank_cur:
			if user["id"] == self.id:
				return i
		
			i += 1
	
	def update_glicko(self, glicko):
		self.collection.update_one({"_id": ObjectId(self._id)}, {"$set": {
			"rating": glicko.mu,
			"rating_deviation": glicko.phi,
			"rating_volatility": glicko.sigma
		}})
	
	def list_of_games(self): # Lazy load in the list of games only when needed
		if self._list_of_games == None:
			self._list_of_games = list(games.find({"$and": [{"$or": [{"1":self.id}, {"2":self.id}]}, {"valid": True}]})) # Get all valid games the user is in
	
		return self._list_of_games

	def badges(self):
		if self._badges == None:
			self._badges = []
			if self.level >= LEVEL_OWNER: self._badges.append("developer")
			if self.level >= LEVEL_ADMIN: self._badges.append("admin")
			if self.win_count() >= 3: self._badges.append("novice")
			elif self.win_count() >= 10: self._badges.append("intermediate")
			elif self.win_count() >= 20: self._badges.append("expert")
			if self.game_count() >= 50: self._badges.append("addicted")
			if self.rating >= 1800: self._badges.append("brilliant")
			elif self.rating >= 1500: self._badges.append("proficient")
			elif self.rating <= 1000: self._badges.append("blunder")
			if self.votes >= 5: self._badges.append("voter")
			if self.flags & USER_FLAG_BLACKLISTED: self._badges.append("blacklisted")
			if self.flags & USER_FLAG_TOURNAMENT_1ST: self._badges.append("tournament-first-place")
			if self.flags & USER_FLAG_TOURNAMENT_2ND: self._badges.append("tournament-second-place")
			if self.flags & USER_FLAG_PATRON: self._badges.append("patron")
			if self.flags & USER_FLAG_MASTER: self._badges.append("master")
		
		return self._badges

	def win_count(self):
		return len([
			game for game in self.list_of_games() if (
				(
					game["outcome"] == OUTCOME_CHECKMATE or
					game["outcome"] == OUTCOME_RESIGN
				) and
				game["winner"] == self.id and
				game["ranked"] == True
			)
		])

	def loss_count(self):
		return len([
			game for game in self.list_of_games() if (
				(
					game["outcome"] == OUTCOME_CHECKMATE or
					game["outcome"] == OUTCOME_RESIGN
				) and
				game["loser"] == self.id and
				game["ranked"] == True
			)
		])

	def draw_count(self):
		return len([
			game for game in self.list_of_games() if (
				game["outcome"] == OUTCOME_DRAW and
				game["ranked"] == True
			)
		])

	def game_count(self):
		return len([
			game for game in self.list_of_games() if (
				(
					game["outcome"] != OUTCOME_EXIT and
					game["outcome"] != OUTCOME_UNFINISHED
				) and
				game["ranked"] == True
			)
		])


class Guild(DBObject):

	collection = db.guilds

	def __init__(self,d):
		super().__init__(d)
		if not self.exists: return

		self.name = d["name"]
		self.id = d["id"]
		self._id = d["_id"]
		self.prefix = d["prefix"]
		self.calls = d["calls"]
		self.games = d["games"]
		self.subscribed = d["subscribed"]


	@classmethod
	def from_guild_id(cls,id):
		d = db.guilds.find_one({"id": id})
		return cls(d)

	@classmethod
	def new(cls,id,name):
		data = {"name":name, "id":id, "prefix":PREFIX, "calls": 0, "games": 0, "subscribed": True}
		guilds.insert_one(data)
		return Guild.from_guild_id(id)

	@classmethod
	def from_guild(cls,guild):
		d = Guild.from_guild_id(guild.id)
		if not d:
			return Guild.new(guild.id, guild.name)
		else:
			return d


def leaderboard(limit):
	return list(db.users.find().sort("rating",-1).limit(limit))

def local_leaderboard(limit, guild):

	guild_member_ids = [member.id for member in guild.members]

	return list(db.users.find({"id": {"$in": guild_member_ids}}).sort("rating",-1).limit(limit))

def date_ordered_games():
	return db.games.find().sort("timestamp",1)
