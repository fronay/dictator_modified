from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random

# ------------------------
doc = """
Iterated Dictator Game (version with 2 players, one player incentivised)
"""

class Subsession(BaseSubsession):
	pass

class Constants(BaseConstants):
	# use_dictator_bots is used in rest of app to modify behavior
	use_dictator_bots = False 
	# use_dictator_bots = settings.SESSION_CONFIGS[0]["use_dictator_bots"]
	# define players per group depending on use of bots
	players_per_group = 2
	# specific instructions template to load
	instructions_template = "dictator_sp/Instructions.html"
	# Initial amount allocated to the dictator
	endowment = c(100)
	# name in url
	name_in_url = "dictator_sp"
	# for dictator bots, need to generate series of values to use
	# (for later experiments, can use text file if set in stone)
	def timeseries(rounds):
		"""returns series of values for dictator bots to present to player"""
		# define amounts the dictator
		fair, generous, mean = (50.0, 65.0, 20.0)
		# test case: just return 50 each time
		return [fair, generous, mean]*rounds
	# current variable round tactic as per Otree docs: high round number, with final screen selectively shown
	def return_num_rounds(self):
		"""returns round numbers from current session configs"""
		return self.session.config['num_rounds']
	# setting this to large number, actual round number set by config settings!
	# (Otree requires this to be set in Constants, hence putting in arbitrary default)
	num_rounds = 100 # settings.SESSION_CONFIGS[0]["num_rounds"]

class Group(BaseGroup):
	kept = models.CurrencyField(
		doc="""Amount allocator decided to keep for himself""",
		min=0, max=Constants.endowment,
		verbose_name="I will keep (from 0 to {})".format(Constants.endowment)
	)
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

	rejected = models.PositiveIntegerField(
    choices=[
        [1, 'Accept'],
        [0, 'Reject'],
    ], widget=widgets.RadioSelectHorizontal
	)

	def active_player_id(self):
		# hardcoded to preserve structure from 3 player version 
		active_player_id = 2 # if self.round_number % 2 != 0 else 3 
		return active_player_id

	def set_payoffs(self):
		receiver = self.get_player_by_id(1)
		dictator = self.get_player_by_id(self.active_player_id())
		receiver.payoff = Constants.endowment - self.kept
		dictator.payoff = self.kept

class Player(BasePlayer):
	def is_active(self):
		return True if self.id_in_group == self.group.active_player_id() else False
	def role(self):
		return "receiver" if self.id_in_group == 1 else "dictator"

