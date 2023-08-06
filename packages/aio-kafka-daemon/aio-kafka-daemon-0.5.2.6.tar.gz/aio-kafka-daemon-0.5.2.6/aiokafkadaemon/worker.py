import asyncio
import logging
import ssl
import traceback

import boto3
import simplejson
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

logger = logging.getLogger("aiokafkadaemon")


class Worker:

    _boto3_client = None

    def __init__(
        self,
        kafka_broker_addr=None,
        kafka_group_id="",
        consumer_topic="",
        producer_topic="",
        create_consumer=True,
        create_producer=False,
        on_run=None,
        sasl_opts={},
    ):
        loop = asyncio.get_event_loop()
        self._kafka_broker_addr = kafka_broker_addr
        self._kafka_group_id = kafka_group_id
        self._consumer_topic = consumer_topic
        self._producer_topic = producer_topic
        self._on_run = on_run
        if not producer_topic:
            self._producer_topic = consumer_topic
        self._consumer = None
        self._producer = None

        # Automatically reads environment variables
        #       AWS_ACCESS_KEY_ID
        #       AWS_SECRET_ACCESS_KEY
        #       AWS_SESSION_TOKEN (optional)
        #       AWS_DEFAULT_REGION
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#environment-variables
        try:
            self._boto3_client = boto3.client("stepfunctions")
        except Exception as e:
            logger.warning(f"Unable to connect to boto3 client for step functions: {e}")

        if create_consumer:
            self._consumer = Worker.make_consumer(
                loop, kafka_broker_addr, kafka_group_id, sasl_opts
            )
        if create_producer:
            self._producer = Worker.make_producer(loop, kafka_broker_addr, sasl_opts)

    @classmethod
    def make_consumer(cls, loop, broker_addr, group_id, sasl_opts={}):
        """
        Creates and connects Kafka  consumer to the broker
        :param loop:
        :param broker_addr:
        :return:
        """
        logger.debug("Creating instance of kafka consumer")
        if not sasl_opts:
            consumer = AIOKafkaConsumer(
                loop=loop,
                bootstrap_servers=broker_addr,
                group_id=group_id,
                session_timeout_ms=60000,
            )
        else:
            consumer = AIOKafkaConsumer(
                loop=loop,
                bootstrap_servers=broker_addr,
                group_id=group_id,
                session_timeout_ms=60000,
                sasl_mechanism="PLAIN",
                sasl_plain_username=sasl_opts["username"],
                sasl_plain_password=sasl_opts["password"],
                security_protocol="SASL_SSL",
                ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2),
            )

        logger.info("Connected consumer to kafka on {}".format(broker_addr))
        return consumer

    @classmethod
    def make_producer(cls, loop, broker_addr, sasl_opts={}):
        """
        Creates an instance of the AIOKafka producer
        :param loop:
        :param broker_addr:
        :return:
        """
        logger.debug("Creating instance of producer")
        if not sasl_opts:
            producer = AIOKafkaProducer(
                loop=loop, bootstrap_servers=broker_addr, compression_type="snappy"
            )
        else:
            producer = AIOKafkaProducer(
                loop=loop,
                bootstrap_servers=broker_addr,
                compression_type="snappy",
                sasl_mechanism="PLAIN",
                sasl_plain_username=sasl_opts["username"],
                sasl_plain_password=sasl_opts["password"],
                security_protocol="SASL_SSL",
                ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2),
            )

        logger.info("Producer connected to kafka on {}".format(broker_addr))
        return producer

    async def __aenter__(self):
        """
        Async iterator-enter coroutine
        :return:
        """
        return self

    async def __aexit__(self):
        """
        Async iterator-exit coroutine
        :return:
        """
        return await self.stop()

    async def start(self):
        if self._consumer_topic:
            self._consumer.subscribe([self._consumer_topic])
        if self._consumer:
            logger.info("Kafka consumer started")
            await self._consumer.start()
        if self._producer:
            logger.info("Kafka producer started")
            await self._producer.start()

    async def stop_kafka(self, stop_producer=False):
        if self._consumer:
            await self._consumer.stop()
            logger.warning("Consumer has been stopped")

        if stop_producer and self._producer:
            await self._producer.stop()
            logger.warning("Producer has been stopped")

    async def stop(self):
        logger.warning("System stopping, stopping consumer first")
        await self.stop_kafka(False)

    async def run(self):
        """
        Main method for the worker. Any child class can either
        overload it, or just implement on_run async callback,
        to perform specific tasks.
        :return:
        """
        try:
            await self.start()
            on_run = getattr(self, "on_run", None)
            if on_run and callable(on_run):
                await on_run()
        except Exception as exc:
            # Only deadling with generic and Kafka critical
            # errors here. ie, UnknownMemberIdError and any
            # heartbeat error, like RequestTimedOutError, is
            # logged only, not raised again
            # https://bit.ly/2IWG8Mn
            # https://bit.ly/2ZCNCtE
            logger.error(
                "Error causing system failure, "
                "{}:\n{}".format(exc, traceback.format_exc())
            )
        finally:
            # it's to better to stop kafka components, better
            # than keep it running with problems.
            await self.stop_kafka()

    def send_heartbeat(self, step_functions_task_id):
        """
        If being processed as part of an AWS Step Functions pipeline
        then send a regular heartbeat when processing to let Step Functions
        know and not kill the process.
        """
        if self._boto3_client is None or step_functions_task_id is None:
            return
        try:
            logger.info(
                f"Sending step functions heartbeat for {step_functions_task_id}"
            )
            self._boto3_client.send_task_heartbeat(taskToken=step_functions_task_id)
        except Exception as e:
            logger.error(f"Unable to send heartbeat {e}")
            return

    def send_step_functions_result(self, step_functions_task_id, result, result_data):
        """
        If being processed as part of an AWS Step Functions pipeline
        then send back a relevant result (success or failure) with useful
        data for processing.
        """
        if self._boto3_client is None or step_functions_task_id is None:
            return
        try:
            if result.get("error") is not None:
                logger.info(
                    f"Sending step functions task failure for {step_functions_task_id}"
                )
                self._boto3_client.send_task_failure(
                    taskToken=step_functions_task_id,
                    error=str(result.get("code")),
                    cause=str(result.get("error")),
                )
            else:
                logger.info(
                    f"Sending step functions task success for {step_functions_task_id}"
                )
                self._boto3_client.send_task_success(
                    taskToken=step_functions_task_id, output=str(result_data),
                )
        except Exception as e:
            logger.error(f"Unable to send step functions response: {e}")
            return

    async def send_result(self, result, context=None, kafka_result_topic=None):
        context_topic = None
        result_data = simplejson.dumps(result, ignore_nan=True).encode("utf-8")

        if context is not None and context.get("step_functions_task_id") is not None:
            self.send_step_functions_result(
                context.get("step_functions_task_id"), result, result_data
            )

        elif context and context.get("topic"):
            context_topic = context.get("topic")
            partition = context.get("partition")
            headers = context.get("headers")
            if headers:
                headers = [(k, v.encode("utf-8")) for k, v in headers.items()]
            logger.info(
                'Context with topic "{}" found, '
                "partition {}".format(context_topic, partition)
            )
            await self._producer.send(
                context_topic, result_data, partition=partition, headers=headers
            )

            logger.info(
                "pushing result with code {} "
                'to topic "{}"'.format(result.get("code", None), kafka_result_topic)
            )

            # if no step_functions_task_id then send to the main result topic
            # if not already published
            if context_topic is not None and context_topic != kafka_result_topic:
                await self._producer.send(kafka_result_topic, result_data)

        # unify error logging
        if result.get("error"):
            logger.error(result.get("error"))
