import os
from typing import Iterable

from prometheus_client import (
    REGISTRY,
    PROCESS_COLLECTOR,
    PLATFORM_COLLECTOR,
    GC_COLLECTOR,
    start_http_server,
)
from prometheus_client.metrics_core import Metric, GaugeMetricFamily
from prometheus_client.registry import Collector

from lichess import LichessAPI, MissingLichessTokenError

APP_PORT = int(os.getenv("APP_PORT", "9000"))


class LichessCollector(Collector):
    def __init__(self, token: str):
        self.api = LichessAPI(token)

    def _gauge(self, sink: list, metric, value):
        sink.append(GaugeMetricFamily(metric, metric, value=float(value)))

    def collect(self) -> Iterable[Metric]:
        metrics = []

        self._gauge(metrics, "puzzle_daily_count", self.api.get_puzzle_count(1))
        self._gauge(metrics, "puzzle_weekly_count", self.api.get_puzzle_count(7))
        self._gauge(metrics, "puzzle_monthly_count", self.api.get_puzzle_count(30))
        self._gauge(metrics, "puzzle_total_count", self.api.get_puzzle_count(99999))

        user_perfs = self.api.get_user_perfs()
        for mode, value in user_perfs.items():
            self._gauge(metrics, mode, value)

        return metrics


def main():
    if not (lichess_token := os.getenv("LICHESS_TOKEN")):
        raise MissingLichessTokenError

    # Unregister default metrics
    REGISTRY.unregister(PROCESS_COLLECTOR)
    REGISTRY.unregister(PLATFORM_COLLECTOR)
    REGISTRY.unregister(GC_COLLECTOR)

    REGISTRY.register(LichessCollector(lichess_token))

    _, thread = start_http_server(APP_PORT)
    thread.join()


if __name__ == "__main__":
    main()
