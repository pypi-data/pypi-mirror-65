import time
from gpiozero import DiskUsage, LoadAverage, CPUTemperature
from main.view import View
from main.controller import Controller
from threading import Thread

class LoadView(View):
    def __init__(self, controller: Controller):
        super().__init__(controller)

        self.cpu_temperature = CPUTemperature()
        self.cpu_load = LoadAverage()
        self.disk_usage = DiskUsage()

        self.cpu_load_cache = []
        self.last_check = 0

    def get_warning_count(self):
        cpu_load_in_percent = self.cpu_load.load_average / 4.0 * 100
        if abs(self.last_check - time.time()) > self.get_update_frequence():
            self.cpu_load_cache.append(cpu_load_in_percent)
            self.last_check = time.time()

        if len(self.cpu_load_cache) > 128:
            self.cpu_load_cache.pop(0)

        return (0, 0)

    def update_display(self, canvas, bounding_box):
        if len(self.cpu_load_cache) > 0:
            current_cpu_load = self.cpu_load_cache[-1]
        else:
            current_cpu_load = 0

        canvas.text((0,0), "CPU Load: %.2f %%" % (current_cpu_load) , fill="white")
        canvas.text((0,10), "CPU Temp: %.2f °C" % self.cpu_temperature.temperature , fill="white")
        canvas.text((0,20), "Disk Usage: %.2f %%" % self.disk_usage.usage, fill="white")

        for index, load in enumerate(self.cpu_load_cache):
            canvas.line([(index, 63 - int(load/100.0 * 34.0)), (index, 63)], width=1, fill="white")

    def get_update_frequence(self):
        return 5

    def get_name(self) -> str:
        return "Load View"
