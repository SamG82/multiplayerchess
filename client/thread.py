import threading

# decorator for running func in a thread
def threaded(func):
    def runner(*args):
        thread = threading.Thread(target = func, args=args, daemon=True)
        thread.start()
        return thread
    return runner