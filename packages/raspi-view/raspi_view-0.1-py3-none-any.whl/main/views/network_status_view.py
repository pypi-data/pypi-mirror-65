import time
from gpiozero import PingServer
from main.view import View
from main.controller import Controller
from threading import Thread

class NetworkStatusView(View):
    def __init__(self, controller: Controller):
        super().__init__(controller)
        self.pings = [
            ("Router", PingServer("10.0.1.1")),
            ("DNS", PingServer("10.0.1.6")),
            ("Google", PingServer("google.com"))
        ]

        self.status_cache = []
        self.global_status = False
        self.last_check = 0

    def get_warning_count(self):
        self._check_pings_in_background()

        red_count = 0
        for ping_cache in self.status_cache:
            red_count += (not ping_cache[1])

        return (red_count, 0)  # blue_count = 0

    def update_display(self, canvas, bounding_box):
        if len(self.status_cache) > 0:
            for index, ping_cache in enumerate(self.status_cache):
                canvas.text((0, index * 10), str(ping_cache[0]) +
                    " Status: " + self._get_status(ping_cache[1]), fill="white")
        else:
            canvas.text((0,0), "checking network\nstatus...", fill="white")

    def get_name(self) -> str:
        return "Network Status View"

    def _check_pings_in_background(self):
        if abs(self.last_check - time.time()) > 10: # 10 second
            self.last_check = time.time()
            Thread(group=None, target=self._check_pings, args=[]).start()

    def _check_pings(self):
            print("pinging network devices...")
            local_status_cache = []

            for ping_name, ping in self.pings:
                local_status_cache.append((ping_name, ping.value))

            self.status_cache = local_status_cache
            print("pinging has been finished")

    def _get_status(self, status: bool) -> str:
        if status:
            return "OK"
        else:
            return "Error"

