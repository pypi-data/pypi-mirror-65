import time

import fortmatic


def epoch_time_now():
    return int(time.time())


def apply_nbf_grace_period(timestamp):
    return timestamp - fortmatic.didt_nbf_grace_period_s
