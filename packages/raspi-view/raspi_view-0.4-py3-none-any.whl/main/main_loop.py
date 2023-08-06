from main.controller import Controller
from main.views.default_view import DefaultView
from main.views.load_view import LoadView
from main.views.network_status_view import NetworkStatusView
from time import sleep, time

DEFAULT_VIEW_CLASSES = [
    LoadView,
    NetworkStatusView
]

class MainLoop:
    def __init__(self, view_classes=None):
        if view_classes is None:
            view_classes = DEFAULT_VIEW_CLASSES
        
        self.controller = Controller(self._activate_next_view)

        self.views = self._init_view_classes(self.controller, view_classes)
        self.current_view_index = 0

        self.last_display_update = 0

    def spin(self):
        print("starting main loop...")
        try:
            while True:
                self._update_display()
                self._update_leds()

                sleep(0.1)
        except KeyboardInterrupt:
            print("\nshutting down...")

    def _init_view_classes(self, controller: Controller, view_classes):
        views = []
        for view_class in view_classes:
            print("adding view " + str(view_class) + "...")
            views.append(view_class(controller))

        return views

    def _activate_next_view(self):
        if self.current_view_index + 1 >= len(self.views):
            self.current_view_index = 0
        else: 
            self.current_view_index += 1

        self.last_display_update = 0

        print("view activated: '" + self._get_current_view().get_name() + "'")

    def _get_current_view(self):
        return self.views[self.current_view_index]

    def _update_display(self):
        current_update_delay = abs(self.last_display_update - time()) 
        if self._get_current_view() is not None and current_update_delay >= self._get_current_view().get_update_frequence():
            self.last_display_update = time()
            with self.controller.get_canvas() as canvas:
                bounding_box = self.controller.get_device_bounding_box()
                self._get_current_view().update_display(canvas, bounding_box)

    def _update_leds(self):
        red_count = 0
        blue_count = 0

        for view in self.views:
            view_count = view.get_warning_count() 
            red_count += view_count[0]
            blue_count += view_count[1]

        self.controller.flash(red_count, blue_count)

if __name__ == "__main__":
    # tracemalloc.start()
    MainLoop().spin()





