import sys
from multiprocessing import Process, Queue

import time
import os
import random
import math
from datetime import datetime

queuesOfProcess = []


starting_time = 0
NP = 0
MINT = 0
MAXT = 0
AVG = 0
NR = 0


def broadcast(pid, LC, max, ospid, reqcount):

    for index in range(0, max):
        if index != pid:
            queuesOfProcess[index].put(LC)
    deliver(pid, ospid, reqcount, LC)
    LC += 1
    return LC


def deliver(pid, ospid, req_count, LC):

    file = str(pid) + ".txt"
    with open(file, "a+", ) as f:
        now = datetime.now()
        msg = "pid=" + str(pid) + ", ospid=" + str(ospid) + ", reqid=" + str(req_count) + ", ts=" + str(
            LC) + ":" + str(pid)
        msg += ", rt=" + str(now.time()) + "\n"
        print(msg)
        f.write(msg)


def receive(LC, pid):
    rLC = 0

    while not queuesOfProcess[pid].empty():
        rLC = queuesOfProcess[pid].get_nowait()

    if rLC > LC:
        LC = rLC


    return LC


def task(pid):
    os_pid = os.getpid()

    while time.time() * 1000 < starting_time:
        continue

    local_random = random.Random()
    random.seed(round(time.time() * 1000) + pid)

    LC = 0
    time_since_last_delivery = time.time() * 1000

    x = local_random.randint(MINT, MAXT)
    y = 1 / AVG
    remaining_time = y * math.exp((-y) * x)

    sendCount = 0
    while sendCount < NR:
        LC = receive(LC, pid)
        remaining_time -= (time.time() * 1000) - time_since_last_delivery

        if remaining_time <= 0:

            LC = receive(LC, pid)
            sendCount += 1
            LC = broadcast(pid, LC, NP, os_pid, sendCount)

            x = local_random.randint(0, 60000)
            y = 1 / AVG
            remaining_time = y * math.exp((-y) * x)
            time_since_last_delivery = time.time() * 1000


if __name__ == '__main__':
    start_time = round(time.time() * 1000)
    starting_time = start_time + 5000 #unify time
    timeArr = []

    NP = int(sys.argv[1])
    MINT = int(sys.argv[2])
    MAXT = int(sys.argv[3])
    AVG = int(sys.argv[4])
    NR = int(sys.argv[5])

    for i in range(0, NP):
        qTemp = Queue()
        queuesOfProcess.insert(i, qTemp)
        timeArr.insert(i, 0)

    for i in range(0, NP):
        process = Process(target=task, args=(i, ))
        process.start()

