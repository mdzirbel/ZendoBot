
import time

def log(to_log: str):
    if to_log[-1] != "\n":
        to_log += "\n"
    with open("Saved/logs.txt", "a") as file:
        file.write(str(time.ctime()) + ": " + to_log)