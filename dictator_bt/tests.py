from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
	def dictator_time_series(round_num):
		"""generates time series for dictator bot to follow when being
		fair or unfair in allocation"""
		pass

	def play_round(self, simulate_receiver=True, simulate_dictator=True):
		"""main bot method, specifies how bots acts to each view"""
		## Introduction Page - advance to next page
		if views.Introduction.is_displayed(self):
			yield (views.Introduction) 
		if simulate_receiver:
			# it is expected that receiver will usually be human participant
			## Prediction Page - 
			if views.Prediction.is_displayed(self):
				yield (views.Prediction, {"predicted": c(10)})
			## Rating Page - 
			if views.Rating.is_displayed(self):
				yield (views.Rating, {"rating": 1})
		if simulate_dictator:
			# dictator may be either bot or incentivised human participant
			## Introduction Page - advance to next page

			## Offer Page - use constant value or time series to submit offer
			if views.Offer.is_displayed(self):
				yield (views.Offer, {"kept": c(50)})
		## WaitForOffer Page - don't have to specify bot/waitpage behavior, is built in
		## FinalPage - similar, no next-button hence no method needed
