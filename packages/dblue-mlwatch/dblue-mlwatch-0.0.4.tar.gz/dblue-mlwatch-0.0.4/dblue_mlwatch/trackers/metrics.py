from dblue_mlwatch import config
from dblue_mlwatch.constants import EventType
from dblue_mlwatch.core.func_thread import FuncThread
from dblue_mlwatch.logger import logger
from dblue_mlwatch.trackers.base import BaseTracker


class MetricsTracker(BaseTracker):

    def __init__(self, *args, **kwargs):
        super(MetricsTracker, self).__init__(*args, **kwargs)

        self.thread = None

    def track_system_metrics(self, interval=config.METRICS_TRACKING_INTERVAL):
        self.track_system_info()
        self.track_system_usage(interval=interval)

    def track_system_info(self) -> bool:
        """
        Track system info such as operating system and hardware details
        :return: Emit status
        """

        from dblue_mlwatch import system

        event = {
            'event_type': EventType.SYSTEM_INFO,
            'os': system.get_os_info(),
            'hardware': system.get_hardware_info(),
        }

        statuses = self.emit(events=[event])
        return statuses[0]

    def _track_system_usage(self) -> bool:
        """
        Emit system usage event
        :return: Emit status
        """

        from dblue_mlwatch import system

        event = {
            'event_type': EventType.SYSTEM_USAGE,
            'cpu': system.get_cpu_usage(),
            'memory': system.get_memory_usage(),
            'disk': system.get_disk_usage(),
            'network': system.get_network_usage(),
            'gpu': system.get_gpu_usage(),
        }

        statuses = self.emit(events=[event])
        return statuses[0]

    def track_system_usage(self, interval):
        """
        Track system usage at interval
        :return:
        """
        try:
            self.thread = FuncThread(delay=interval, func=self._track_system_usage)
        except Exception as e:
            logger.exception(e)

    def stop(self):
        """
        Stop metrics monitoring thread
        :return:
        """
        if self.thread:
            self.thread.stop()
