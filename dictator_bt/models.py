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
		return [50,75]*10
	# current variable round tactic as per Otree docs: high round number, with final screen selectively shown
	### TODO: set via configs - try using return_num_rounds function
	def return_num_rounds(self):
		"""returns round numbers from current session configs"""
		return self.session.config['num_rounds']
	# setting this to large number, actual round number set by config settings!
	# (Otree requires this to be set in Constants, hence putting in arbitrary default)
	num_rounds = 100 # settings.SESSION_CONFIGS[0]["num_rounds"]

# Active player id used to toggle between roles for human dictator players
# player_2 active means that player_3 (i.e. the other dictator) sees waitscreen
# then toggled, and player_3 is active while player_2 waits
ACTIVE_BOT_ID = 2


def toggle_bot_id(id):
	"""set active_player_id equal to this function when switching between dictators"""
	if id == 2:
		return 3
	elif id == 3:
		return 2
	else:
		raise ValueError("Unexpected player id, expecting id to be 2 or 3")

class Group(BaseGroup):
	pass

class Player(BasePlayer):
	def set_payoffs(self):
		# get applicable value of time series:
		self.dictator_offer = Constants.timeseries(Constants.return_num_rounds(self))[self.round_number - 1]
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

