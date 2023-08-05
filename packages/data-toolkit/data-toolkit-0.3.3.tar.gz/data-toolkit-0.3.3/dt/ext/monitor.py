import GPUtil
from threading import Thread
from sentry_sdk import capture_message
import time, os

class Monitor(Thread):
    def __init__(self, delay: int, alert_threshold: int):
        super(Monitor, self).__init__()
        self.stopped = False
        self.delay = delay # Time between calls to GPUtil
        # how many consecutive checks need to be 0 before an alert is sent
        self.alert_threshold = alert_threshold 
        self.start()

    def run(self):
        consec_idles = 0 
        
        while not self.stopped:
            idle_gpus = GPUtil.getAvailability(GPUtil.getGPUs())
            all_idle = set(idle_gpus) == {1}
            
            if all_idle: counter += 1 
            else: consec_idles = 0
                
            if consec_idles > self.alert_threshold:
                inst_private_ip = os.environ["SSH_CONNECTION"].split()[2]
                num_seconds = self.delay * self.alert_threshold
                print(f'{inst_private_ip} had {num_seconds} of no GPU activity.')
                capture_message(f'{inst_private_ip} had {num_seconds} of no GPU activity.')
                consec_idles = 0
            time.sleep(self.delay)

    def stop(self):
        self.stopped = True
        
# Instantiate monitor with a 10-second delay between updates
# monitor = Monitor(2)

# Train, etc.

# Close monitor
# monitor.stop()