from main.controller import Controller
from PIL import ImageDraw

class View:
    def __init__(self, controller: Controller):
        self.controller = controller

    def get_name(self) -> str:
        return "No name"

    def get_warning_count(self) -> tuple:
        return (0, 0) # red, blue

    def update_display(self, canvas: ImageDraw):
        pass
