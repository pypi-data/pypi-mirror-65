import argparse
import logging
import time
import ray
from ray.streaming import StreamingContext
from ray.streaming.config import Config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--titles-file",
    required=True,
    help="the file containing the wikipedia titles to lookup")

# Splits input line into words and
# outputs records of the form (word,1)
def splitter(line):
    return [(word, 1) for word in line.split()]


if __name__ == "__main__":
    # Get program parameters
    args = parser.parse_args()
    titles_file = str(args.titles_file)
    ######################################
    # import ray
    # import time
    # ray.init(address="auto")
    # @ray.remote
    # def f(i):
    #     print("remote function....")
    #     time.sleep(10)
    #     return i
    # futures = [f.remote(i) for i in range(20)]
    # print(ray.get(futures))
    # ray.shutdown()
    import ray
    import time
    ray.init()
    @ray.remote
    def f():
        return b""
    n = 1000
    f_direct = f.options(is_direct_call=True)
    while True:
        start = time.time()
        ray.get([f_direct.remote() for _ in range(n)])
        print(n / (time.time() - start), "calls per second")
    ######################################
    # ray.init(address="auto", load_code_from_local=True, include_java=True)
    # ctx = StreamingContext.Builder() \
    #     .option(Config.CHANNEL_TYPE, Config.NATIVE_CHANNEL) \
    #     .build()
    # # A Ray streaming environment with the default configuration
    # ctx.set_parallelism(1)  # Each operator will be executed by two actors
    #
    # # Reads articles from wikipedia, splits them in words,
    # # shuffles words, and counts the occurrences of each word.
    # # stream = ctx.source(Wikipedia(titles_file)) \
    # # stream = ctx.source(ctx.read_text_file(titles_file)) \
    # stream = ctx.read_text_file(titles_file) \
    #     .flat_map(splitter) \
    #     .key_by(lambda x: x[0]) \
    #     .reduce(lambda old_value, new_value:
    #             (old_value[0], old_value[1] + new_value[1])) \
    #     .sink(print)
    # start = time.time()
    # ctx.execute("wordcount")
    # end = time.time()
    # logger.info("Elapsed time: {} secs".format(end - start))