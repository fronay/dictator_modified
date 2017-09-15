from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random
import gc

# ------------------------
doc = """
Iterated Dictator Game with 2-3 players
"""

class Subsession(BaseSubsession):
	pass

class Constants(BaseConstants):
	# define custom bot sequence for use by active_bot_id method
	bot_sequence = (2,2,1,2,1,1,2,2,1,2)
	# single player version, hence only 1 player per group
	players_per_group = None
	# specific instructions template to load
	instructions_template = "dictator_modified/Instructions.html"
	# Initial amount allocated to the dictator
	endowment = c(100)
	# name in url
	name_in_url = "dictator_bt"
	# current variable round tactic as per Otree docs: high round number, with final screen selectively shown
	def return_num_rounds(self):
		"""returns actual round numbers from current session configs"""
		# remember that player will only play half of this number against each bot
		return self.session.config['num_rounds']
	# initialising this to large number, actual round number set by config settings!
	# (Otree requires this to be set in Constants, hence putting in arbitrary default)
	num_rounds = 50 # settings.SESSION_CONFIGS[0]["num_rounds"]

class Group(BaseGroup):
	def active_bot_id(self):
		"""returns active bot id, either alternating or based on custom sequence"""
		use_custom_sequence = True
		if not use_custom_sequence:
			## SIMPLE version - bots just alternate:
			bot_id = 1 if self.round_number % 2 != 0 else 2 
		else:
			## CUSTOM version - bots can sometimes play 2 rounds in a row
			# fetch order in which they play from Constants
			bs = Constants.bot_sequence
			# careful that this matches the intended round number set in configs!
			assert len(bs) >= self.session.config['num_rounds'], \
			"length of bot sequence appears to be smaller than the configured max round number"
			bot_id = bs[self.round_number-1]
		return bot_id

	def bot_offer(self):
		"""return value for either bot to play in a given round"""
		use_custom_sequence = True
		# define offer list for two different bots here:
		fair, generous, mean = (50.0, 65.0, 20.0)
		nice_bot_timeseries = [fair, generous]*int(Constants.return_num_rounds(self)/2)
		mean_bot_timeseries = [fair, mean]*int(Constants.return_num_rounds(self)/2)
		bot_id = self.active_bot_id()
		if not use_custom_sequence:
			## SIMPLE VERSION with alternating bots:
			# bot 1 is active in odd rounds (1,3,5) etc and bot 2 is active in even rounds (2,4,6) etc.
			# hence must index their timeseries with round_number/2 and round_number/2 -1, respectively:
			if bot_id == 1:
				# active in odd rounds
				bot_offer = nice_bot_timeseries[int((self.round_number-1)/2)]
			elif bot_id == 2:
				# active in even rounds
				bot_offer = mean_bot_timeseries[int((self.round_number/2) - 1)]
			else: 
				raise ValueError
		else:
			## CUSTOM version, if bots follow custom bot sequence
			ts = nice_bot_timeseries if bot_id == 1 else mean_bot_timeseries
			# count which turn (1st, 2nd, nth) of the bot it is, and return appropriate value from timeseries
			bot_turn_number = Constants.bot_sequence[:self.round_number].count(bot_id)
			# lists are zero-indexed so subtract 1 from turn for actual offer:
			bot_offer = ts[bot_turn_number - 1]
		return bot_offer

class Player(BasePlayer):
	def set_payoffs(self):
		# get applicable value of time series:
		# self.dictator_offer = Constants.timeseries(Constants.return_num_rounds(self))[self.round_number - 1]
		self.dictator_offer = self.group.bot_offer()
		self.payoff = self.dictator_offer
		self.played_against = self.group.active_bot_id()

	predicted = models.CurrencyField(
		doc="""Amount receiver predicted they would receive from allocator""",
		min=0, max=Constants.endowment,
		verbose_name="I will most likely receive (from 0 to {})".format(Constants.endowment)
	)

	rating = models.PositiveIntegerField(
	choices=[
		[1, 'Fair'],
		[0, 'Unfair'],
		]
	)
	# test var, see if this shows up in data as well:
	played_against = models.PositiveIntegerField(
		doc="""id of bot that player was paired off with in current round""",
		# this is set in set_payoffs method right now
		)

	def role(self):
		return "receiver" 


## test code: one time import to get settings, then remove path again to avoid dep problem
#import sys
#sys.path.append("/Users/franzr/Desktop/main_code/NBU_files/dictator_modified")
#import settings 
#sys.path.remove("/Users/franzr/Desktop/main_code/NBU_files/dictator_modified")

