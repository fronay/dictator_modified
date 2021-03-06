from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import random
from time import sleep

def vars_for_all_templates(self):
	return {
			"current_round": self.round_number,
			"max_rounds" : Constants.return_num_rounds(self),
			"participant_id": self.player.id_in_group,
			"role": self.player.role,
	}

class Introduction(Page):
	"""intro page with instructions, should show for all players"""
	# this should only be shown at the start
	def vars_for_template(self):
		pass
	def is_displayed(self):
		return self.round_number <= 1

class Prediction(Page):
	"""prediction page for potential amount received, should only show for receiver"""
	form_model = models.Player
	form_fields = ["predicted"]
	def vars_for_template(self):
		active_bot = self.group.active_bot_id()
		return {
			"other_player": active_bot,
			# TODO: implement more general photo file structure for larger participant list
			"image_path": "dictator_modified/img{}.jpg".format(active_bot),
		}
	def before_next_page(self):
		self.player.set_payoffs()


class SimulatedWaitPage(Page):
	def vars_for_template(self):
		return {
			"other_player": self.group.active_bot_id(),
		}
	def get_timeout_seconds(self):
		min_delay = 1
		return random.random()*3 + min_delay

class Rating(Page):
	"""receiver rates fairness of offer"""
	form_model = models.Player
	form_fields = ["rating"]
	def vars_for_template(self):
		offer = self.player.payoff
		return {
			'endowment': Constants.endowment,
			'offer': offer,
		}

class FinalPage(Page):
	"""def vars_for_template(self):
		return {
			'round_number': self.round_number,
		}"""
	def is_displayed(self):
		# this is shown at the end of the round
		return self.round_number >= Constants.return_num_rounds(self)

page_sequence = [
	Introduction,
	Prediction,
	SimulatedWaitPage,
	Rating,
	FinalPage,
]
