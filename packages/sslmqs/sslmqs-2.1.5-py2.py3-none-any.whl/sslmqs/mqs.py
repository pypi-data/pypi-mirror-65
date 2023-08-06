import baseconfig
import logging
import multiprocessing
import sslmqs
import queue

from .mqs_async import MqsAsync


class Mqs:
    def __init__(self, app_config, exchange, exit_event):
        self._app_config = app_config
        self._exchange = exchange
        self._exit_event = exit_event

        self._routing_keys_of_queues = []
        self._bundle_publish_queues = []
        self._publish_queue = multiprocessing.Queue()
        self._log = logging.getLogger("sslmqs")

        self._subscriptions = []
        self._subscribe_queue = multiprocessing.Queue()
        self._instructions_queue = multiprocessing.Queue()

    def subscribe(self, queue_name, durable, mp_queue):
        subscription_index = len(self._subscriptions)
        self._subscriptions.append(mp_queue)
        instruction = ("subscribe", queue_name, durable, subscription_index)
        self._instructions_queue.put(instruction)

    def add_routing(self, queue_name, routing_key):
        instruction = ("add-routing", queue_name, routing_key)
        self._instructions_queue.put(instruction)

    def publish_from(self, mp_queue, routing_key=None):
        if routing_key is None:
            self._bundle_publish_queues.append(mp_queue)
        else:
            entry = (mp_queue, routing_key)
            self._routing_keys_of_queues.append(entry)

    def count_pending_publish(self):
        return self._publish_queue.qsize()

    def tick(self):
        self._flush_publish()
        self._flush_subscribe()

    def start(self, process_name="sslmqs.async"):
        def start_async(
                app_config,
                exchange,
                exit_event,
                publish_queue,
                subscribe_queue,
                instructions_queue):
            logger = logging.getLogger("sslmqs")
            try:
                mqs = MqsAsync(
                    app_config,
                    exchange,
                    exit_event,
                    publish_queue,
                    subscribe_queue,
                    instructions_queue)
                mqs.start()
            except Exception:
                logger.error("Unhandled exception:", exc_info=True)
                raise

        self._p = multiprocessing.Process(
            name=process_name,
            target=start_async,
            args=(
                self._app_config,
                self._exchange,
                self._exit_event,
                self._publish_queue,
                self._subscribe_queue,
                self._instructions_queue)
        )
        self._p.start()

    def stop(self, timeout=2):
        multiwatch.terminate_process(self._p, timeout=timeout)

    def _flush_publish(self):
        # Start with the queues where each message is associated with a routing
        # key.
        for mq_queue in self._bundle_publish_queues:
            try:
                message_bundle = mq_queue.get_nowait()
                if message_bundle:
                    message, routing_key = message_bundle
                    self._publish_queue.put((message, routing_key))
            except queue.Empty:
                pass

        # Then continue with the queues where all messages from the same queue
        # share the same routing key.
        for mq_queue, routing_key in self._routing_keys_of_queues:
            try:
                message = mq_queue.get_nowait()
                if message:
                    self._publish_queue.put((message, routing_key))
            except queue.Empty:
                pass

    def _flush_subscribe(self):
        try:
            info = self._subscribe_queue.get_nowait()
        except queue.Empty:
            info = None

        if info:
            subscription_index, body = info
            mp_queue = self._subscriptions[subscription_index]
            mp_queue.put(body)
