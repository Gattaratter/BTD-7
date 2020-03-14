class Player:
    def __init__(self, lifepoints, money):
        self.lifepoints = lifepoints
        self.money = money

    def give_damage(self, damage):
        self.lifepoints -= damage
