import contextlib                                                           # Gives utilities for writing context managers. We use it to make chdir() work with 'with'.
import os                                                                   # os.walk() to traverse dirs; os.path helpers; os.getcwd()/chdir() to change dirs.
import queue                                                                # Thread-safe queues. queue.Queue() to safely share work/results between threads. 
import requests                                                             # Send GET reqs to the target server.
import sys                                                                  # Access to stdout.
import threading                                                            # Lets us spawn threads to run test_remote() concurrently.
import time                                                                 # Against throttling.

FILTERED = [".jpg", ".gif", ".png", ".css"]                                 # A list of file extensions we don’t want to test remotely.
TARGET = "http://localhost:8080"                                            # The target web server we are mapping. 
THREADS = 10                                                                # Number of worker threads to spawn for remote testing.

# Shared queues
answers = queue.Queue()                                                     # Where we store successful(200) URLs.
web_paths = queue.Queue()                                                   # This one holds all the paths we plan to test, think of it as a wordlist. 

# Buils the wordlist from disk, collecting local file paths:
def gather_paths():
    # os.walk('.') recursively traverses the current directory: 
    # It yields tuples (root, dirs, files). 
    # We used _ to ignore dirs (don’t need the subdirectory list):
    for root, _, files in os.walk('.'):
        for fname in files:                                                 # Iterates each filename in the current dir.
            if os.path.splitext(fname)[1] in FILTERED:                      # Returns (name_without_ext, ext): [1] is the extension, like .png. If that extension is in FILTERED, it skips it.
                continue
            # Builds the full local path
            path = os.path.join(root, fname)
            # Removes the leading dot
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)                                             # Adds the path to the queue so threads can consume it later.



# chdir() — temporary directory change as a context manager. 
@contextlib.contextmanager                                                  # This decorator lets us write a generator that behaves like a context manager.
def chdir(path):
    '''
    First, follow the specified path. 
    At the end, return to the original directory.
    '''
    this_dir = os.getcwd()                                                  # Saves your current working directory so you can return later.
    os.chdir(path)                                                          # Moves into the directory we want (our WP file tree).
    try:
        yield                                                               # `yield` hands control back to the `with` block. Everything inside `with chdir(...)`: runs while you’re in that directory.
    finally:
        os.chdir(this_dir)                                                  # Always runs (even if an exception happens), restoring the original directory.



'''
test_remote() is a worker function(designed to be run by a thread) that checks paths against the target:
- Producer gather_paths(): creates tasks (paths) and puts them into web_paths.
- Worker test_remote(): repeatedly take one task from web_paths, do the HTTP request, and record results
'''
def test_remote():
    while not web_paths.empty():                                            # Loops while there is still work.
        path = web_paths.get()                                              # Takes one path from the queue.
        url = f'{TARGET}{path}'                                             # Builds the full URL string.
        time.sleep(2)                                                       # Pauses for 2 secs before each request.
        r = requests.get(url)                                               # Sends a GET request to the formed URL.
        if r.status_code == 200:                                            # Checks the status code.
            answers.put(url)                                                # If 200, store the URL in the found queue. 
            sys.stdout.write('+')                                           # Writes '+' for success, '-' for else. 
        else:
            sys.stdout.write('-')
        sys.stdout.flush()                                                  # Forces it to appear immediately. 


# Starts and join threads.
def run():
    mythreads = list()                                                      # Creates a list to keep thread objects so we can join them later.
    for i in range(THREADS):                                                # Loops 10 times.
        print(f'Spawning thread {i}')                                       # Prints a line for each thread we start.
        t = threading.Thread(target=test_remote)                            # Creates a thread that will run test_remote().
        mythreads.append(t)                                                 # Saves it in the list. 
        t.start()                                                           # Launch the thread.
    
    for thread in mythreads:                                                # As each thread is running test_remote(), it waits until all threads finish before continuing. 
        thread.join()



if __name__ == '__main__':
    # Temporarily switches into this directory:
    with chdir("/home/kali/Downloads/wordpress"):                       # Our local WP directory is functioning as a wordlist of potential web paths.
        gather_paths()                                                  # Builds the queue of web paths from our local WP directory, using it as a wordlist of candidate web paths.
    input('Press return to continue.')                                  # Pauses, giving us a chance to review the gathered paths before scanning starts.

    run()                                                               # Starts threads and tests all collected paths against the target.
    with open('myanswers.txt', 'w') as f:                               # Opens a file for writing. 
        while not answers.empty():
            f.write(f'{answers.get()}\n')                               # While the answers queue has items, it pops each UEL and writes it.
    print('done')