from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class LandingPage(Page):
	"""an example mturk landing page with a comprehension check for grouping by wait time afterwards"""
	form_model = "player"
	form_fields = ["mturkID","age"]


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    LandingPage,
    #ResultsWaitPage,
    # Results
]
