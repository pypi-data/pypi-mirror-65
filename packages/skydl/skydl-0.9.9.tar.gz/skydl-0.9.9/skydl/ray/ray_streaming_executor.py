# -*- coding: utf-8 -*-
import ray
import logging
import traceback
import time
from py_common_util.common.date_utils import DateUtils
from skydl.ray.streaming_0_8_2.python.streaming import Environment, DataStream
from skydl.ray.ray_streaming_util import DefaultStreamingSource, DefaultStreamingEnvConfigV082

# define logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RayStreamingExecutor:
    """
    ray流计算执行器，子类可以重写build_stream()方法
    """
    @property
    def args_parser(self):
        return self._args_parser

    def __init__(self, args_parser=None):
        self._args_parser = args_parser
        logger.info("starting a streaming executor...")

    def execute(self, env=None, show_logic_dataflow_graph=False, loop_idle_seconds=1):
        try:
            if not env:
                env = Environment(DefaultStreamingEnvConfigV082(parallelism=self.args_parser.streaming_parallelism))
            stream = self.build_stream(env=env)
            self.execute_forever(env, stream, show_logic_dataflow_graph, loop_idle_seconds)
        except Exception as e:
            logger.error(f"RayStreamingExecutor fail on execute(): {e}")
            traceback.print_exc()

    def execute_forever(self, env, stream, show_logic_dataflow_graph=False, loop_idle_seconds=1):
        while True:
            try:
                if show_logic_dataflow_graph:
                    env.print_logical_graph()
                # stream to stdout
                start = time.time()
                ray.get(env.execute())  # Stay alive until execution finishes
                env.wait_finish()
                end = time.time()
                logger.info("Streaming Elapsed time: {} secs".format(end - start))
                logger.debug("Output stream id: {}".format(stream.id))
            except Exception as e:
                logger.error(f"Error Occurred on Ray Streaming: {e}")
                traceback.print_exc()
                # TODO 发送异常运维警报
            finally:
                time.sleep(loop_idle_seconds)  # 等待所有算子的数据都执行完，然后休息1秒后再继续重新执行同一个stream计算图

    def build_stream(self, env: Environment) -> DataStream:
        """
        子类需要重写该方法构建具体的业务stream
        注意streaming算子类必须要预先install在所有节点中，或者都在该方法内部定义，尝试了importlib的方式会报错
        @:param env
        """
        class FooStreamingSource(DefaultStreamingSource):
            def __init__(self):
                logger.info("FooStreamingSource init...(init func only be executed 1 time in a stream graph!!!)")
                self._count = 0

            def get_next(self):
                self._count += 1
                logger.info("get_next:" + str(self._count))
                if self._count % 2 == 0:
                    time.sleep(5)  # with env config background_flush=True, even if it sleep ever, it also success to auto flush。but can not kill current stream until return None。
                    # return None
                    return str(self._count) + "-aaa\nbbb*"+DateUtils.now_to_str()
                else:
                    return str(self._count) + "-ccc*"+DateUtils.now_to_str()

        def splitter_fn(record):
            """convert record to another record list, e.g. [record]"""
            logger.info("splitter: " + record)
            # return [record+"-splitter-" + str(i) for i in range(20)]
            return [record+"-splitter-" + DateUtils.now_to_str()]

        def handle_record_fn(record):
            """处理回测的逻辑"""
            logger.info("args_parser=" + str(self.args_parser))
            logger.info("record=" + record)
            time.sleep(10)
            logger.info(record + ", finished:" + DateUtils.now_to_str())

        stream = env.source(
            FooStreamingSource()
        ).round_robin().set_parallelism(2).flat_map(
            flatmap_fn=splitter_fn
        ).set_parallelism(1).map(
            map_fn=handle_record_fn,
            name="nocode_backtest_map"
        )
        return stream










