class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target):
        self.x = target.rect.x - 400
        self.y = target.rect.y - 250