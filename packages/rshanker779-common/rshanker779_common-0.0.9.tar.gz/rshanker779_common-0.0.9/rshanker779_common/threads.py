import abc
import datetime
import logging
import threading
import time
from typing import Hashable, Optional, Set
import rshanker779_common as utils

logger = logging.getLogger(__name__)


class RegularRunnableThread(threading.Thread, abc.ABC):
    _process_map: Set[Hashable] = set()

    def __init__(
        self,
        interval: datetime.timedelta,
        daemon: bool = False,
        error_delay: datetime.timedelta = datetime.timedelta(seconds=5),
    ):
        abc.ABC.__init__(self)
        threading.Thread.__init__(self)

        self.daemon = daemon
        self.interval = interval
        self.last_run_time: Optional[datetime.datetime] = None

        self.error_delay = error_delay

        self.process_id = None
        self.stop = False
        self.do_task = utils.retry(
            self.do_task, number_retries=float("inf"), time_retry=self.error_delay
        )
        self.start()

    def run(self) -> None:
        while True:
            if self.stop:
                break
            now = datetime.datetime.now()
            if self.last_run_time is None or now - self.last_run_time > self.interval:
                self.do_task()
                self.last_run_time = now

    def stop_running(self):
        self.stop = True

    @abc.abstractmethod
    def do_task(self) -> None:
        pass
