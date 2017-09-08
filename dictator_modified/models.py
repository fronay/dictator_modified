from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random


doc = """
Iterated Dictator Game with 2-3 players
"""

class Constants(BaseConstants):
	# use_dictator_bots is used in rest of app to modify behavior
	use_dictator_bots = True
	# define players per group depending on use of bots
	players_per_group = None if use_dictator_bots else 3
	# specific instructions template to load
	instructions_template = "dictator_modified/Instructions.html"
	# Initial amount allocated to the dictator
	endowment = c(100)
	# name in url
	name_in_url = "dictator_modified"
	# for dictator bots, need to generate series of values to use
	# (for later experiments, can use text file if set in stone)
	def timeseries(rounds):
		"""returns series of values for dictator bots to present to player"""
		# define amounts the dictator
		fair, generous, mean = (50.0, 65.0, 20.0)
		# test case: just return 50 each time
		return [fair]*rounds
	# current variable round tactic as per Otree docs: high round number, with final screen selectively shown
	num_rounds = 3

# Active player id used to toggle between roles for human dictator players
# player_2 active means that player_3 (i.e. the other dictator) sees waitscreen
# then toggled, and player_3 is active while player_2 waits
ACTIVE_PLAYER_ID = 2


def toggle_player_id(id):
	"""set active_player_id equal to this function when switching between dictators"""
	if id == 2:
		return 3
	elif id == 3:
		return 2
	else:
		raise ValueError("Unexpected player id, expecting id to be 2 or 3")

class Subsession(BaseSubsession):
	pass

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

	def set_payoffs(self):
		p1 = self.get_player_by_id(1)
		if not Constants.use_dictator_bots:
			p2 = self.get_player_by_id(2)
			p3 = self.get_player_by_id(3)
			p1.payoff = Constants.endowment - self.kept
			# not sure if I still need payoffs for player 2 / 3, if so will need to change below
			# p2.payoff = self.kept
			# p3.payoff = self.kept
		elif Constants.use_dictator_bots:
			# get time series:
			dictator_offer = Constants.timeseries(Constants.num_rounds)[self.round_number - 1]
			print('*******offer value is', dictator_offer)
			p1.bot_money_earned = Constants.endowment - c(dictator_offer)




class Player(BasePlayer):
	# TODO: refactor this test var 
	bot_money_earned = models.CurrencyField(
		doc="""money earned in 1v2 human bot game""",
		min=0, max=Constants.endowment,
		verbose_name="I will keep (from 0 to {})".format(Constants.endowment)
	)
	def is_active(self, active_player_id):
		return True if self.id_in_group == active_player_id else False
	def role(self):
		return "receiver" if self.id_in_group == 1 else "dictator"

