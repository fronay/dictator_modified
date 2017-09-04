from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Offer(Page):
    form_model = models.Group
    form_fields = ["kept"]

    def is_displayed(self):
        return self.player.id_in_group == 1

class Prediction(Page):
    form_model = models.Group
    form_fields = ["predicted"]
    def is_displayed(self):
        return self.player.id_in_group == 2

class ResultsWaitPage(WaitPage):
    """shown while players wait"""
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def vars_for_template(self):
        if self.player.id_in_group == 2:
            body_text = "You are participant 2. Waiting for participant 1 to decide."
        else:
            body_text = "Please wait"
        return {"body_text": body_text}


class Results(Page):
    """shows results of game to each player"""
    def offer(self):
        return Constants.endowment - self.group.kept

    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.kept,
        }

class Rating(Page):
    """gives receiver chance to rate fairness of offer"""
    form_model = models.Group
    form_fields = ["rating"]
    def is_displayed(self):
        return self.player.id_in_group == 2

page_sequence = [
    Introduction,
    Prediction,
    Offer,
    ResultsWaitPage,
    Results,
    Rating
]
