class UIElement:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def draw(self, window):
        assert False, "Fehler, UI Element muss draw() überschreiben"

    def update(self):
        assert False, "Fehler, UI Element muss update() überschreiben"
