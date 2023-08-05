from main.view import View
from main.controller import Controller

class TestView(View):
    def __init__(self, controller: Controller):
        super().__init__(controller)

    def update_display(self, canvas, bounding_box):
        canvas.text((30, 40), "Status: OK", fill="white")

    def get_name(self):
        return "Test View"
