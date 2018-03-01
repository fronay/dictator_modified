from . import models
from ._builtin import Page, WaitPage
from .models import Constants

"""
TODO: NEW LAYOUT for 2P-Version

Player 1 sees:
Welcome 
Rules
*Here's your offer + CUSTOM OPTION
OPTION 1: FAIR?
OPTION 2: REJECT? 
OPTION 3: NO_OP
End


Player 2 sees: 
Welcome 
Rules
*What are you going to offer? + CUSTOM INSTRUCTION
FeedbackPage
End
"""


def vars_for_all_templates(self):
	return {
			"round_number": self.round_number,
			"participant_id": self.player.id_in_group,
			"role": self.player.role
	}

class Introduction(Page):
	"""intro page with instructions, should show for all players"""
	# this should only be shown at the start
	def vars_for_template(self):
		return {
			"test_message": " "#Constants.return_num_rounds(self),
		}
	def is_displayed(self):
		return self.round_number <= 1

class Prediction(Page):
	"""prediction page for potential amount received, should only show for receiver"""
	form_model = models.Group
	form_fields = ["predicted"]
	def vars_for_template(self):
		active_player_id = self.group.active_player_id()
		return {
			"other_player": active_player_id,
			# TODO: implement more general photo file structure for larger participant list
			"image_path": 'dictator_sp/img{}.jpg'.format(active_player_id)
		}
	def is_displayed(self):
		return self.player.role() == "receiver"

class Offer(Page):
	"""offer page for dictator to decide how much to share with receiver
	...should only be seen by active dictator"""
	form_model = models.Group
	form_fields = ["kept"]
	def is_displayed(self):
		# show only to active dictator
		return self.player.role() == "dictator" and self.player.is_active()
	def before_next_page(self):
		self.group.set_payoffs()

class WaitForOffer(WaitPage):
	def vars_for_template(self):
		return {
			"body_text": "Waiting for other player's offer"
		}
	def is_displayed(self):
		return self.player.role() == "receiver"

class NoActionResult(Page):
	"""receiver sees results of allocation but has no action option """
	def vars_for_template(self):
		offer = Constants.endowment - self.group.kept
		return {
			'endowment': Constants.endowment,
			'offer': offer,
		}
	def is_displayed(self):
		return self.player.role() == "receiver"

class Rating(NoActionResult):
	"""receiver rates fairness of offer"""
	form_model = models.Group
	form_fields = ["rating"]


class RejectionOption(NoActionResult):
	"""receiver sees offer and has option of rejecting or accepting """
	form_model = models.Group
	form_fields = ["rejected"]

class FeedbackPage(Page):
	def vars_for_template(self):
		active_player_id = self.group.active_player_id()
		rating = self.group.in_round(self.round_number -1).get_rating_display()
		rejected = self.group.in_round(self.round_number - 1).get_rejected_display()
		kept = self.group.in_round(self.round_number - 1).kept
		offer = Constants.endowment - kept
		return {
			'other_player': active_player_id,
			# TODO: implement more general photo file structure for larger participant list
			'image_path': 'dictator_sp/img{}.jpg'.format(active_player_id),
			'endowment': Constants.endowment,
			'kept': kept,
			'offer': offer,
			'rating': rating,
			'rejected': rejected
		}
	def is_displayed(self):
		# show only to active dictator
		return self.player.role() == "dictator" and self.player.is_active() and self.round_number >= 2 

class ToggleWaitPage(WaitPage):
	"""shown when ready to switch dictators - functionally, this is the end of the round"""
	def after_all_players_arrive(self):
		# set payoffs here if in 3-person game
		# TODO: migrate to before_next_page on offer page, since all info there already!
		self.group.set_payoffs()

	def vars_for_template(self):
		# get activity status of players from tracking dictionary in models:
		# generate message for wait screen during testing:
		inputs = (self.player.id_in_group, self.player.role()) 
				# self.player.is_active(models.ACTIVE_PLAYER_ID))
		body_text = """Thanks for your patience, participant {0}. Your role is (still) {1}.\n \n
				Waiting for the other 2 participants to end their turn.""".format(*inputs)
		# conditionally add a message about the dictator's sharing choice if they were active last round:
		if self.player.role() == "dictator" and self.player.is_active():
			choice_message = "You completed your turn. You kept {0} out of {1} off the payoff. \n \n".format(self.group.kept, Constants.endowment)
			body_text = choice_message + body_text
		return {"body_text": body_text}

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
	FeedbackPage,
	Offer,
	WaitForOffer,
	Rating,
	NoActionResult,
	RejectionOption,
	ToggleWaitPage,
	FinalPage
]
