FCFS = '''

from typing import List, Tuple

def fcfs(jobs: List[Tuple[str, int, int]]):
    # Sort by arrival time
    jobs_sorted = sorted(jobs, key=lambda x: x[1])
    time = 0
    wt = {}
    tat = {}
    
    for pid, at, bt in jobs_sorted:
        if time < at:
            time = at
        start = time
        finish = start + bt
        tat[pid] = finish - at
        wt[pid] = start - at
        time = finish
    return wt, tat


if __name__ == '__main__':
    n = int(input("Enter number of processes: "))
    jobs = []
    
    for i in range(n):
        pid = input(f"Enter Process ID for process {i+1}: ")
        at = int(input(f"Enter Arrival Time for {pid}: "))
        bt = int(input(f"Enter Burst Time for {pid}: "))
        jobs.append((pid, at, bt))
    
    wt, tat = fcfs(jobs)
    
    print("\nProcess\tArrival\tBurst\tWaiting\tTurnaround")
    for pid, at, bt in sorted(jobs, key=lambda x: x[1]):
        print(f"{pid}\t{at}\t{bt}\t{wt[pid]}\t{tat[pid]}")
    
    avg_wt = sum(wt.values()) / len(wt)
    avg_tat = sum(tat.values()) / len(tat)
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

'''

Non_preemptive_SJF=  '''from typing import List, Tuple

def sjf(jobs: List[Tuple[str, int, int]]):
    # jobs: (pid, arrival, burst)
    jobs_sorted = sorted(jobs, key=lambda x: x[1])
    completed = []
    time = 0
    wt = {}
    tat = {}
    ready = []
    i = 0
    n = len(jobs_sorted)
    
    while len(completed) < n:
        # push arrived jobs
        while i < n and jobs_sorted[i][1] <= time:
            ready.append(jobs_sorted[i])
            i += 1
        if not ready:
            time = jobs_sorted[i][1]
            continue
        # pick shortest burst
        ready.sort(key=lambda x: x[2])
        pid, at, bt = ready.pop(0)
        start = time
        finish = start + bt
        wt[pid] = start - at
        tat[pid] = finish - at
        time = finish
        completed.append(pid)
    return wt, tat


if __name__ == '__main__':
    n = int(input("Enter number of processes: "))
    jobs = []

    for i in range(n):
        pid = input(f"Enter Process ID for process {i+1}: ")
        at = int(input(f"Enter Arrival Time for {pid}: "))
        bt = int(input(f"Enter Burst Time for {pid}: "))
        jobs.append((pid, at, bt))
    
    wt, tat = sjf(jobs)
    
    print("\nProcess\tArrival\tBurst\tWaiting\tTurnaround")
    for pid, at, bt in sorted(jobs, key=lambda x: x[1]):
        print(f"{pid}\t{at}\t{bt}\t{wt[pid]}\t{tat[pid]}")
    
    avg_wt = sum(wt.values()) / len(wt)
    avg_tat = sum(tat.values()) / len(tat)
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

'''

Round_Robin = '''

from typing import List, Tuple
from collections import deque

def rr(jobs: List[Tuple[str, int, int]], quantum: int):
    # jobs: (pid, arrival, burst)
    jobs_sorted = sorted(jobs, key=lambda x: x[1])
    time = 0
    q = deque()
    i = 0
    n = len(jobs_sorted)
    remaining = {pid: bt for pid, at, bt in jobs_sorted}
    start_times = {}
    finish_times = {}

    while len(finish_times) < n:
        # Add all processes that have arrived up to current time
        while i < n and jobs_sorted[i][1] <= time:
            pid, at, bt = jobs_sorted[i]
            q.append((pid, at))
            i += 1

        # If queue is empty, jump to next arrival time
        if not q:
            if i < n:
                time = jobs_sorted[i][1]
                continue
            else:
                break

        pid, at = q.popleft()

        if pid not in start_times:
            start_times[pid] = time

        run = min(quantum, remaining[pid])
        remaining[pid] -= run
        time += run

        # Enqueue any newly arrived jobs during this time slice
        while i < n and jobs_sorted[i][1] <= time:
            q.append((jobs_sorted[i][0], jobs_sorted[i][1]))
            i += 1

        # If process still has remaining burst, re-enqueue it
        if remaining[pid] > 0:
            q.append((pid, at))
        else:
            finish_times[pid] = time

    wt = {}
    tat = {}
    for pid, at, bt in jobs_sorted:
        tat[pid] = finish_times[pid] - at
        wt[pid] = tat[pid] - bt

    return wt, tat


if __name__ == '__main__':
    n = int(input("Enter number of processes: "))
    jobs = []

    for i in range(n):
        pid = input(f"Enter Process ID for process {i+1}: ")
        at = int(input(f"Enter Arrival Time for {pid}: "))
        bt = int(input(f"Enter Burst Time for {pid}: "))
        jobs.append((pid, at, bt))
    
    quantum = int(input("Enter Time Quantum: "))

    wt, tat = rr(jobs, quantum)

    print("\nProcess\tArrival\tBurst\tWaiting\tTurnaround")
    for pid, at, bt in sorted(jobs, key=lambda x: x[1]):
        print(f"{pid}\t{at}\t{bt}\t{wt[pid]}\t{tat[pid]}")

    avg_wt = sum(wt.values()) / len(wt)
    avg_tat = sum(tat.values()) / len(tat)
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
'''

Petersons_Algorithm = '''
from multiprocessing import Process, Value, Array
import time

def peterson_demo(iterations=5):
   
    flag = Array('i', [0, 0])  
    turn = Value('i', 0)       
    counter = Value('i', 0)   

    def proc(idx: int):
        other = 1 - idx
        for i in range(iterations):
           
            flag[idx] = 1
            turn.value = other

            
            while flag[other] == 1 and turn.value == other:
                time.sleep(0.0001)  

            
            with counter.get_lock():  
                tmp = counter.value
                tmp += 1
                counter.value = tmp

           
            flag[idx] = 0

   
    p0 = Process(target=proc, args=(0,))
    p1 = Process(target=proc, args=(1,))

    p0.start()
    p1.start()

    p0.join()
    p1.join()

   
    return counter.value


if __name__ == '__main__':
    print('Final counter:', peterson_demo(1000))
'''

Binary_Semaphore = '''
from multiprocessing import Value
import time


class BinarySemaphore:
    def __init__(self, initial=1):
        self.flag = Value('i', 1 if initial else 0)

    def acquire(self):
        while True:
            with self.flag.get_lock():  
                if self.flag.value == 1:
                    self.flag.value = 0  
                    return
            time.sleep(0.001) 

    def release(self):
        with self.flag.get_lock():
            self.flag.value = 1


if __name__ == '__main__':
    s = BinarySemaphore(1)
    s.acquire()
    print('acquired')
    s.release()
    print('released')
'''

Dining_Philosophers = '''
import threading
import time
import random


class Philosopher(threading.Thread):
    def __init__(self, idx, left_fork, right_fork):
        super().__init__()
        self.idx = idx
        self.left = left_fork
        self.right = right_fork

    def run(self):
        for _ in range(3):  
            self.think()
            self.eat()

    def think(self):
        print(f"Philosopher {self.idx} is thinking.")
        time.sleep(random.uniform(0.1, 0.3))

    def eat(self):
        first, second = (self.left, self.right) if id(self.left) < id(self.right) else (self.right, self.left)
        
        with first:
            with second:
                print(f"Philosopher {self.idx} starts eating.")
                time.sleep(random.uniform(0.1, 0.3))
                print(f"Philosopher {self.idx} finishes eating.")


def dining_philosophers_demo(n=5):
    forks = [threading.Lock() for _ in range(n)]
    philosophers = [Philosopher(i, forks[i], forks[(i + 1) % n]) for i in range(n)]

    for p in philosophers:
        p.start()
    for p in philosophers:
        p.join()

    print("Dinner is over.")


if __name__ == "__main__":
    dining_philosophers_demo(5)

'''
   
os_codes = {
    "FCFS.txt": FCFS,
    "Non_preemptive_SJF.txt": Non_preemptive_SJF,
    "Round_Robin.txt": Round_Robin,
    "Petersons_Algorithm.txt": Petersons_Algorithm,
    "Binary_Semaphore": Binary_Semaphore,
    "Dining_Philosophers": Dining_Philosophers
}      

def os_():
    for file,code in os_codes.items():
        print(file)
    filename = input("Enter filename: ")
    with open(filename, 'w') as f:
        f.write(os_codes[filename]) 