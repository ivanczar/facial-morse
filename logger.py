import queue
import threading


class Logger:
    def __init__(self, log_file_path="./game_logs.txt"):
        self.log_file_path = log_file_path
        self.log_queue = queue.Queue()
        self.consumer_thread = threading.Thread(target=self.write_logs)
        self.consumer_thread.start()

    def log(self, message):
        self.log_queue.put(message)

    def write_logs(self):
        with open(self.log_file_path, "a") as log_file:
            while True:
                log_message = self.log_queue.get()
                if log_message is None:
                    break
                log_file.write(log_message + "\n")
                self.log_queue.task_done()

    def close(self):
        self.log_queue.put(None)
        self.consumer_thread.join()
