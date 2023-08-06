#!/usr/bin/env python3

import asyncio

from gv_rpc.utils import TRAFFIC_DATA_TYPES
from gv_services.proto.archivist_pb2 import TrafficData
from gv_services.proto.common_pb2 import Ack
from gv_services.proto.geographer_pb2 import Locations, Mapping
from gv_services.proto.interface_grpc import InterfaceBase
from gv_services.archivist import Archivist
from gv_services.broadcaster import Broadcaster
from gv_services.geographer import Geographer
from gv_services.storage.dbstorage.dbstorage import DbStorage
from gv_utils import enums


DATA_POINTS = enums.DataTypeId.datapoints
MAPPING_ROADS_DATA_POINTS = enums.DataTypeId.mappingroadsdatapoints


class Interface(InterfaceBase):

    def __init__(self, logger, basedatapath, basecartopath, *dbcredentials):
        super().__init__()
        self.logger = logger
        self.dbstorage = DbStorage(*dbcredentials)
        self.archivist = Archivist(logger, basedatapath, self.dbstorage)
        self.broadcaster = Broadcaster(logger)
        self.geographer = Geographer(logger, basecartopath, self.dbstorage)

    async def async_init(self):
        await self.dbstorage.async_init()

    async def publish(self, stream):
        message = await stream.recv_message()
        coros = [self.broadcaster.publish(message), ]
        datatype = message.datatype.split('-')[0]
        if datatype in TRAFFIC_DATA_TYPES:
            pbdata = TrafficData()
            message.data.Unpack(pbdata)
            coros.append(self.archivist.store_data(pbdata, datatype, message.timestamp))
        elif datatype == DATA_POINTS:
            pbdata = Locations()
            message.data.Unpack(pbdata)
            coros.append(self.geographer.add_data_points(pbdata))
        elif datatype == MAPPING_ROADS_DATA_POINTS:
            pbdata = Mapping()
            message.data.Unpack(pbdata)
            coros.append(self.geographer.add_mapping_roads_data_points(pbdata))
        status = await asyncio.gather(*coros)
        await stream.send_message(Ack(success=bool(int(sum(status)/len(status)))))

    async def subscribe(self, stream):
        async for message in self.broadcaster.subscribe(await stream.recv_message()):
            await stream.send_message(message)

    async def get_data(self, stream):
        async for response in self.archivist.get_data(await stream.recv_message()):
            await stream.send_message(response)

    async def add_mapping_roads_data_points(self, stream):
        success = await self.geographer.add_mapping_roads_data_points(await stream.recv_message())
        await stream.send_message(Ack(success=success))

    async def add_data_points(self, stream):
        success = await self.geographer.add_data_points(await stream.recv_message())
        await stream.send_message(Ack(success=success))

    async def import_shapefile_to_db(self, stream):
        response = await self.geographer.import_shapefile_to_db()
        await stream.send_message(response)

    async def get_data_points(self, stream):
        response = await self.geographer.get_data_points(await stream.recv_message())
        await stream.send_message(response)

    async def get_roads(self, stream):
        response = await self.geographer.get_roads(await stream.recv_message())
        await stream.send_message(response)

    async def get_mapping_roads_data_points(self, stream):
        response = await self.geographer.get_mapping_roads_data_points(await stream.recv_message())
        await stream.send_message(response)

    async def update_roads_freeflow_speed(self, stream):
        response = await self.geographer.update_roads_freeflow_speed(await stream.recv_message())
        await stream.send_message(response)
