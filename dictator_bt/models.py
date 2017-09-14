from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random

# ------------------------
doc = """
Iterated Dictator Game with 2-3 players
"""

class Subsession(BaseSubsession):
	pass

class Constants(BaseConstants):
	# use_dictator_bots is used in rest of app to modify behavior
	use_dictator_bots = True 
	# use_dictator_bots = settings.SESSION_CONFIGS[0]["use_dictator_bots"]
	players_per_group = None
	# specific instructions template to load
	instructions_template = "dictator_modified/Instructions.html"
	# Initial amount allocated to the dictator
	### TODO: set via configs
	endowment = c(100)
	# name in url
	name_in_url = "dictator_bt"
	# for dictator bots, need to generate series of values to use
	# (for later experiments, can use text file if set in stone)
	def timeseries(rounds):
		"""returns series of values for dictator bots to present to player"""
		# define amounts the dictator
		fair, generous, mean = (50.0, 65.0, 20.0)
		# test case: just return 50 or 75 each time
		return [fair,generous,mean]*rounds
	# current variable round tactic as per Otree docs: high round number, with final screen selectively shown
	### TODO: set via configs - try using return_num_rounds function
	def return_num_rounds(self):
		"""returns round numbers from current session configs"""
		return self.session.config['num_rounds']
	# setting this to large number, actual round number set by config settings!
	# (Otree requires this to be set in Constants, hence putting in arbitrary default)
	num_rounds = 100 # settings.SESSION_CONFIGS[0]["num_rounds"]

class Group(BaseGroup):
	def active_bot_id(self):
		"""on even turns, bot 1 is active, otherwise bot 2"""
		bot_id = 1 if self.round_number % 2 != 0 else 2 
		### CAN ALSO DEFINE CUSTOM BOT ACTIVITY HERE
		### E.G. IF WANT TO PLAY SAME BOT TWICE IN ROW
		### DONT FORGET TO CHANGE BOT_OFFER() BELOW TO MATCH
		# also set bot_id in group data so that we can track it in results:
		self.active_bot_id = bot_id
		return bot_id

	def bot_offer(self):
		"""return value for either bot to play in a given round"""
		fair, generous, mean = (50.0, 65.0, 20.0)
		# define offer list for two different bots here:
		nice_bot_timeseries = [fair, generous]*int(Constants.return_num_rounds(self)/2)
		mean_bot_timeseries = [fair, mean]*int(Constants.return_num_rounds(self)/2)
		bot_id = self.active_bot_id()
		###
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
		return bot_offer

class Player(BasePlayer):
	def set_payoffs(self):
		# get applicable value of time series:
		# self.dictator_offer = Constants.timeseries(Constants.return_num_rounds(self))[self.round_number - 1]
		self.dictator_offer = self.group.bot_offer()
		self.payoff = self.dictator_offer

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
	def role(self):
		return "receiver" 


## test code: one time import to get settings, then remove path again to avoid dep problem
#import sys
#sys.path.append("/Users/franzr/Desktop/main_code/NBU_files/dictator_modified")
#import settings 
#sys.path.remove("/Users/franzr/Desktop/main_code/NBU_files/dictator_modified")

