import math
from threading import Thread

from ioflow.performance_metrics import HttpPerformanceMetrics
from tf_summary_reader.read_summary_data_periodically import (
    read_summary_data_periodically,
)


class TensorFlowSummaryWatcher(HttpPerformanceMetrics):
    def start_watch(self):
        tf_summary_dir = self.config["tf_summary_dir"]
        interval = self.config["interval"]

        for result in read_summary_data_periodically(tf_summary_dir, interval):
            for timestamp, item in result.iterrows():
                step = item["step"]
                del item["step"]
                for metric_name, metric_value in item.items():
                    if math.isnan(metric_value):
                        continue
                    # metric = Metric(metric_name, metric_value, timestamp, step)
                    # self.send_metrics(metric)
                    self.log_metric(metric_name, metric_value, timestamp, step)

    def start_watch_in_other_thread(self):
        t = Thread(target=self.start_watch)
        t.setDaemon(True)
        t.start()


if __name__ == "__main__":
    import time

    config = {
        "tf_summary_dir": "/home/howl/PycharmProjects/tf_summary_reader/data",
        "interval": 10,
        "metrics_report_url": "http://10.43.17.53:25005/savedrawingdata",
        "task_id": "123456",
    }
    tf_summary_watcher = TensorFlowSummaryWatcher(config)

    tf_summary_watcher.start_watch_in_other_thread()

    for _ in range(600):
        print("I am in main thread")
        time.sleep(1)
