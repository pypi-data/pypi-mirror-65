import time
from gpiozero import PingServer
from main.view import View
from main.controller import Controller
from threading import Thread
import subprocess

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

            canvas.line([(0,37), (127,37)], fill="white", width=1)

            for index, interface in enumerate(["wlan0", "eth0"]):
                ip_address = self._get_ip_address(interface) 
                interface_short = interface[0:4]
                canvas.text((0, 44 + (index * 10)), "%s: %s" % (interface_short, ip_address), fill="white")
        else:
            canvas.text((0,0), "checking network\nstatus...", fill="white")

    def get_name(self) -> str:
        return "Network Status View"

    def get_update_frequence(self):
        return 10

    def _check_pings_in_background(self):
        if abs(self.last_check - time.time()) > 60: # 60 second
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
    
    @staticmethod
    def _get_ip_address(interface):
        print("cheking ip address for %s..." % interface)
        try:
            if NetworkStatusView._get_network_interface_state(interface) == 'down':
                return None
            cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\\.){3}[0-9]*' | grep -Eo '([0-9]*\\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface
            return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]
        except:
            return None 

    @staticmethod
    def _get_network_interface_state(interface):
        try:
            with open('/sys/class/net/%s/operstate' % interface, 'r') as f:
                return f.read()
        except:
            return 'down' # default to down

