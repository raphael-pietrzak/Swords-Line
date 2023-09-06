
import time


counter = 0
start_time = time.time()

def ping():
    global counter, start_time
    counter += 1
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= 1.0:
        rps = counter / elapsed_time
        # print(f"Réceptions par seconde : {rps:.2f}")
        counter = 0
        start_time = current_time