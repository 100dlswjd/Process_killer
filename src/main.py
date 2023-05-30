import psutil
import time

Leauge_of_legends = ["RiotClientUx.exe", "RiotClientUxRender.exe", "LeagueClientUx.exe", "LeagueClientUxRender.exe"]

while True:
    time.sleep(10)
    for proc in psutil.process_iter():
        Process_name = proc.name()
        Process_id = proc.pid
        if Process_name in Leauge_of_legends:
            proc.kill()