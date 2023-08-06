import logging
import random
import time


def retry(action, termination_event):
    """
    Executes an action an infinite number of times, sleeping for a few seconds
    between the moment the action terminates and the next run. This number of
    seconds is:

     - Started with 2 seconds.
     - Increased at every run, the previous value being multiplied by 2.
     - Capped to 60 seconds.
     - Randomized by adding or removing 0.5 s.

    Example of a pause between the successive executions:

     -  2.1: original 2 s. + a random 0.1 s.
     -  4.0:  2 * 2 + 0.0.
     -  7.6:  4 * 2 - 0.4.
     - 16.3:  8 * 2 + 0.3.
     - 31.5: 16 * 2 - 0.5.
     - 60.1: capped 60 + 0.1.
     - 60.3: capped 60 + 0.3.
     - 59.8: capped 60 - 0.2.

    The multiplication per 2 is done to reduce the stress on a system which
    doesn't seem to go very well.

    The cap ensures that even if the problem is solved hours later, it wouldn't
    take much longer than a minute to restore the functionality.

    The random shift ensures all clients won't retry at the same time.
    """
    log = logging.getLogger("sslmqs")
    retry_after_seconds = 2
    max_seconds = 60

    while True:
        action()
        if termination_event.is_set():
            break

        # So that all clients don't reconnect at the same time.
        random_shift = random.randint(-5, 5)
        time_to_sleep = retry_after_seconds * 10 + random_shift

        log.info("Sleeping for {} seconds before retrying.".format(
            time_to_sleep / 10))

        for _ in range(time_to_sleep):
            time.sleep(0.1)
            if termination_event.is_set():
                break

        retry_after_seconds *= 2
        if retry_after_seconds > max_seconds:
            retry_after_seconds = max_seconds
