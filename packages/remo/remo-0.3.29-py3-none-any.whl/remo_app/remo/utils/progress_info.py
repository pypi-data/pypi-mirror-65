from datetime import datetime, timedelta


class ProgressInfo:

    def __init__(self, total: int, items: str = 'items'):
        self.total = total
        self.count = 0
        self.start = datetime.now()
        self.reported = -1
        self.items = items

    def report(self, count: int = 1, **kwargs):
        self.count += count

        percentage = int(self.count / self.total * 100)
        if percentage > self.reported:
            self._report(percentage, **kwargs)

    def _report(self, percentage: int, **kwargs):
        elapsed = (datetime.now() - self.start).seconds + 1e-3
        avg_speed = self.count / elapsed
        eta = timedelta(seconds=int((self.total - self.count) / avg_speed))
        self.reported = percentage
        msg = (f'Progress {percentage}% - {self.count}/{self.total} - '
               f'elapsed {timedelta(seconds=int(elapsed))} - speed: {"%.2f" % avg_speed} {self.items}/s')
        if eta:
            msg = f'{msg}, ETA: {eta}'
        if kwargs:
            msg = f'{msg} {kwargs}'
        self._print(msg)

    def _print(self, text):
        end = '\n' if self.reported == 100 else '\r'
        print(text, end=end)
