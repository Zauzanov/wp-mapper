import contextlib 
import os 
import queue 
import random                                                           # To randomize sleep time
import requests 
import sys
import threading
import time
from queue import Empty                                                 # Exception raised by Queue.get_nowait() when the queue is empty.
from urllib.parse import urljoin                                        # Correctly join base URL + path (handles slashes safely).

FILTERED = {".jpg", ".gif", ".png", ".css"}
TARGET = "http://localhost:8080"
THREADS = 10

answers = queue.Queue()
web_paths = queue.Queue()


def gather_paths():
    """
    Walks the current directory recursively and pushes all file paths 
    into the web_paths queue. This makes the local WP directory act like a wordlist.
    """
    for root, _, files in os.walk("."):
        for fname in files:
            if os.path.splitext(fname)[1].lower() in FILTERED:
                continue

            path = os.path.join(root, fname)

            # Strip leading: './wp-content/...' becomes '/wp-content/...'
            if path.startswith("."):
                path = path[1:]

            # Normalizes to URL separators.
            path = path.replace(os.sep, "/")

            web_paths.put(path)


@contextlib.contextmanager
def chdir(path):
    """
    Temporarily changes the working directory for the duration of a 'with' block,
    then always returns to the original directory afterward.
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)


def test_remote():
    """
    Worker function (runs in each thread):
    - Pulls a path from web_paths;
    - Builds a full URL;
    - Request it;
    - Records URLs that return 200 OK.
    """
    # One session per thread keeps connection alive.
    session = requests.Session()

    while True:
        try:
            path = web_paths.get_nowait()                               # No blocking: grabs next job from queue immediately.
        except Empty:
            return                                                      # Exits the worker, if no more jobs left.

        # Safely joins base + path, preventing missing/double slashes).
        # Removes specified characters from the left (leading) and right (trailing) ends of a string:
        url = urljoin(TARGET.rstrip("/") + "/", path.lstrip("/"))

        # Sleeps betwwen 0.2 and 0.6 seconds. 
        # Randomness prevents bursty 'all threads at once' traffic.
        time.sleep(0.2 + random.random() * 0.4)

        try:
            r = session.get(url, timeout=5)                             # Send HTTP GET. timeout prevents hangs.
            if r.status_code == 200:
                answers.put(url)
                sys.stdout.write("+")
            else:
                sys.stdout.write("-")
        except requests.RequestException:
            sys.stdout.write("!")                                       # Print '!' for network errors/timeouts.
        finally:
            sys.stdout.flush()
            web_paths.task_done()                                       # Marks this queue item as fully processed.


def run():
    """
    Start THREADS worker threads, then wait until the web_paths queue is fully processed.
    """
    threads = []
    for i in range(THREADS):                                            # Spawns the requested number of workers.
        t = threading.Thread(target=test_remote, daemon=True)           # daemon=True: thread will not block program exit.
                                                                        # daemon=True means our worker threads are “background” threads that will be stopped automatically 
                                                                        # when the main program exits, so they won’t keep the program running. 
        threads.append(t)
        t.start()

    web_paths.join()                                                    # Block until every queued path gets task_done().


if __name__ == "__main__":
    with chdir("/home/kali/Downloads/wordpress"):
        gather_paths()

    input("Press return to continue.")                                  # Pause before sending requests (safety checkpoint).
    run()                                                               # Perform the remote enumeration.

    # Write all discovered 200-OK URLs to a file:
    with open("myanswers.txt", "w") as f:
        while not answers.empty():
            f.write(f"{answers.get()}\n")

    print("\ndone")
