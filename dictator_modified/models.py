from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random


doc = """
Iterated Dictator Game with 2-3 players
"""

class Constants(BaseConstants):
	name_in_url = "dictator_modified"
	players_per_group = 3
	# current variable round tactic as per Otree docs: high round number, with final screen selectively shown
	# not sure if it is 'legal' to modify num_rounds on the fly
	num_rounds = 3

	instructions_template = "dictator_modified/Instructions.html"

	# Initial amount allocated to the dictator
	endowment = c(100)

# ALTERNATIVE: simply toggle 1 variable
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
		p2 = self.get_player_by_id(2)
		p3 = self.get_player_by_id(3)
		p1.payoff = Constants.endowment - self.kept
		# not sure if I still need payoffs for player 2 / 3, if so will need to change below
		# p2.payoff = self.kept
		# p3.payoff = self.kept


class Player(BasePlayer):
	def is_active(self, active_player_id):
		return True if self.id_in_group == active_player_id else False
	def role(self):
		return "receiver" if self.id_in_group == 1 else "dictator"

