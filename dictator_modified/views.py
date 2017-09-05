from . import models
from ._builtin import Page, WaitPage
from .models import Constants

def vars_for_all_templates(self):
    return {
            "round_number": self.round_number,
            "participant_id": self.player.id_in_group,
            "role": self.player.role
    }

class Introduction(Page):
    # this should only be shown at the start
    def is_displayed(self):
        return self.round_number <= 1

class Prediction(Page):
    form_model = models.Group
    form_fields = ["predicted"]
    def vars_for_template(self):
        return {
            "other_player": models.ACTIVE_PLAYER_ID,
            "image_path": 'dictator_modified/img{}.jpg'.format(models.ACTIVE_PLAYER_ID)
        }
    def is_displayed(self):
        return self.player.role() == "receiver"

class Offer(Page):
    form_model = models.Group
    form_fields = ["kept"]

    def is_displayed(self):
        # show only to active player
        return self.player.role() == "dictator" and self.player.is_active(models.ACTIVE_PLAYER_ID)


class ResultsWaitPage(WaitPage):
    """shown while players wait, calcs payoffs and toggles active player"""
    def after_all_players_arrive(self):
        # set payoffs
        self.group.set_payoffs()
        # toggle activity status of player for different dictator next round:
        models.ACTIVE_PLAYER_ID = models.toggle_player_id( models.ACTIVE_PLAYER_ID )

    def vars_for_template(self):
        # get activity status of players from tracking dictionary in models:
        # generate message for wait screen during testing:
        inputs = (self.player.id_in_group, self.player.role(), 
                self.player.is_active(models.ACTIVE_PLAYER_ID))
        body_text = """You are participant {0}. Your role is {1}.
                You are currently Active: {2}.
                Waiting for other participant to end the round.""".format(*inputs)
        # toggle activity status of player for different dictator next round:
        # models.ACTIVE_PLAYER_ID = models.toggle_player_id( models.ACTIVE_PLAYER_ID )
        # add extra msg to body_text for testing
        # body_text = body_text + " Toggled active player from {0} to {1}".format(inputs[2], models.ACTIVE_PLAYER_ID)
        return {"body_text": body_text}

class Results(Page):
    """shows results of game to each player"""
    # TODO: need to refactor this into one central offer function
    def offer(self):
        return Constants.endowment - self.group.kept

    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.kept,
        }
    def is_displayed(self): 
        # careful, don't want to show other people's results
        # TODO: check no timing error can lead to this
        return self.player.id_in_group == "dictator"

class Rating(Page):
    """gives receiver chance to rate fairness of offer"""
    form_model = models.Group
    form_fields = ["rating"]

    def other_player(self):
        # right now, only player ids are 1 & 2, making this function superfluous
        # but in large game may go up to >20
        """other_player_id = 2 if self.player.id_in_group == 1 else 1
        print(other_player_id)
        return other_player_id"""
        pass
        # return models.ACTIVE_PLAYER_ID
    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.kept,
        }

    def is_displayed(self):
        return self.player.role == "receiver"

class FinalPage(Page):
    """def vars_for_template(self):
        return {
            'round_number': self.round_number,
        }"""
    def is_displayed(self):
        # this is shown at the end of the round
        return self.round_number >= Constants.num_rounds

page_sequence = [
    Introduction,
    Prediction,
    Offer,
    ResultsWaitPage,
    Results,
    Rating,
    FinalPage
]
