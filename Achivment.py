class AchivmentController:

    def __init__(self, parent):
        self.parent = parent
        self.achivment_list = [

        ]

    def update(self):
        for achv in self.achivment_list:
            if not achv.reached:
                if achv.check():
                    self.parent.message = achv.message


class Achivment:
    def __init__(self, game):
        self.message = "How to get"
        self.game = game
        self.reached = False

    def check(self):
        return False
