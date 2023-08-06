import asyncio
from pprint import pprint

import aioboto3
import time

from .aws_base import AWSBase
from .ddb_const import *


async def cardinality(response, *consumer_args):
    for _ in response["Items"]:
        pprint("current total = {}".format(str(consumer_args[0].increment())))


async def request(segment, exclusive_key, **config):
    if source := config.pop(SOURCE_TABLE, None):
        if exclusive_key:
            return await source.scan(
                Segment=segment, ExclusiveStartKey=exclusive_key, **config
            )
        else:
            return await source.scan(Segment=segment, **config)


def init_table(client, **schema):
    try:
        tables = client.list_tables()
        if schema["TableName"] in tables["TableNames"]:
            client.delete_table(TableName=schema["TableName"])
            time.sleep(2)
            while True:
                tables = client.list_tables()  # to change
                if schema["TableName"] in tables["TableNames"]:
                    time.sleep(3)
                else:
                    break
        client.create_table(**schema)
        waiter = client.get_waiter("table_exists")
        waiter.wait(TableName=schema["TableName"])
        return 0
    except:
        return 1


class DynamoDBTraverse(AWSBase):
    """db traverse execution"""
    def __init__(self, queue, local=True, **kwargs):
        super().__init__(**kwargs)
        self.local = local
        self.queue = queue

    def get_dynamodb_async(self):
        if self.local:
            return aioboto3.resource(DYNAMODB, endpoint_url=TEST_URL, region_name='us-east-1')
        else:
            return aioboto3.resource(
                DYNAMODB,
                aws_access_key_id=self.my_aws_access_key_id,
                aws_secret_access_key=self.my_aws_secret_access_key,
                region_name='us-east-1'
            )

    async def traverse(self, **config):
        ps = [
            asyncio.create_task(self.produce(i, **config.get(PRODUCER)))
            for i in range(config.get(PRODUCER)[THREAD_COUNT])
        ] + [
            asyncio.create_task(self.consume(i, **config.get(CONSUMER)))
            for i in range(config.get(CONSUMER)[THREAD_COUNT])
        ]

        await asyncio.gather(*ps)

        self.info("Traverse complete...")

    async def produce(self, segment, **config):
        _counter = iteration = 0
        cur = None
        while True:
            response = await request(segment, cur, **config)
            await self.queue.put(response)
            iteration += 1
            _counter += response["Count"]

            self.info(
                f"Producer #{segment} fetches {len(response['Items'])}"
                f" at iteration {iteration}, total count = {_counter}"
                f" q size ~ {self.queue.qsize()}"
            )

            if LAST_EVALUATED_KEY not in response:
                break
            else:
                cur = response[LAST_EVALUATED_KEY]
        self.info(f"Producer #{segment} fetched {_counter} items in total.")

    async def consume(self, segment, **config):
        while True:
            try:
                queued_item = await asyncio.wait_for(
                    self.queue.get(), timeout=config[TIMEOUT]
                )
                if queued_item is None:
                    break
            except asyncio.TimeoutError:
                self.error(f"consumer #{segment} timeout...")
                break
            try:
                await config[FUNCTION](queued_item, *config[ARGS])
            except Exception as e:
                self.error(str(e))
                continue
            finally:
                self.queue.task_done()
