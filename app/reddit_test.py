import time
from typing import Tuple

import praw
import reactivex
from praw.models import Submission
from reactivex import operators as ops

if __name__ == "__main__":
    reddit = praw.Reddit(
        client_id="",
        client_secret="",
        password="",
        user_agent="",
        username="",
    )

    subreddit = reddit.subreddit("CryptoCurrency")


    # def list_items(state, tick):
    #     for submission in list:
    #
    #     return ()

    # reactivex.interval(5).pipe(
    #     ops.scan(lambda state, tick: ))
    # list = list(subreddit.new())

    def print_fn(submission: Submission):
        print(submission.created)
        print(submission.title)
        # Output: the submission's title
        print(submission.score)
        # Output: the submission's score
        print(submission.id)
        # Output: the submission's ID
        print(submission.url)

    def scan_fn(tupl: Tuple[int, list], tick: int) -> Tuple[int, list]:
        last_timestamp = tupl[0]
        events = list(filter(lambda s: s.created > last_timestamp, subreddit.new()))

        if len(events) > 0:
            return events[0].created, events
        else:
            return tupl[0], []

    # (timestamp_of_news_event, news_events)
    reddit_news_stream = reactivex.interval(5).pipe(ops.scan(scan_fn, (0, [])),
                                      ops.flat_map(lambda tupl: reactivex.from_iterable(tupl[1])))
    (reddit_news_stream
     .subscribe(on_next=print_fn))

    time.sleep(10000000)

    # for submission in subreddit.new():
    #     print_fn(submission)

# async def main():
#     disposable = (connect(asyncio.get_running_loop())
#                   .pipe(price_processor.process,
#                         ops.do_action(on_next=print))
#                   .subscribe())
#
#     await asyncio.sleep(5)
#
#     disposable.dispose()
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#
#     # Schedule a call to hello_world()
#     loop.create_task(main())
#
#     # Blocking call interrupted by loop.stop()
#     try:
#         loop.run_forever()
#     finally:
#         loop.close()
