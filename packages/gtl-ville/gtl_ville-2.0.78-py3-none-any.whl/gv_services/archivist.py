#!/usr/bin/env python3

import traceback

from gv_services.proto.archivist_pb2 import TrafficData
from gv_services.storage import filestorage
from gv_utils import datetime, enums, geometry
from gv_utils.csv import ENCODING

METROPME = enums.DataTypeId.metropme
TOMTOMFCD = enums.DataTypeId.tomtomfcd
ROADS = enums.DataTypeId.roads
ZONES = enums.DataTypeId.zones


class Archivist:

    def __init__(self, logger, basedatapath, dbstorage):
        super().__init__()
        self.logger = logger
        self.basedatapath = basedatapath
        self.dbstorage = dbstorage

    async def store_data(self, pbtrafficdata, datatype, pbtimestamp):
        success = False
        try:
            await filestorage.write_data(self.basedatapath, pbtrafficdata.trafficdata, datatype,
                                         datetime.from_timestamp(pbtimestamp.ToSeconds()))
            success = True
            self.logger.debug('Archivist stored {} data.'.format(datatype))
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while storing {} data.'.format(datatype))
        finally:
            return success

    async def get_data(self, request):
        datatype = request.datatype
        fromdate, todate = datetime.from_timestamp(request.fromdate.ToSeconds()), \
                           datetime.from_timestamp(request.todate.ToSeconds())
        freq = request.freq
        noeids = request.noeids
        geom = request.geom
        if freq < 1:
            freq = 1
        try:
            geom = geometry.decode_geometry(geom)
        except:
            geom = None

        try:
            if datatype not in (METROPME, TOMTOMFCD, ROADS, ZONES):
                raise ValueError('Unknown data type')

            if noeids or geom is not None:
                trafficeids = ''
                try:
                    trafficeids = await self.dbstorage.get_data_eids(datatype, fromdate, todate, geom)
                except:
                    self.logger.error(traceback.format_exc())
                    self.logger.error('An error occurred while getting {} eids between {} and {}.'
                                      .format(datatype, datetime.to_string(fromdate), datetime.to_string(todate)))
                finally:
                    yield TrafficData(trafficdata=trafficeids.encode(ENCODING), applyto='header')

            for startday, endday in datetime.split_in_days(fromdate, todate):
                try:
                    async for data in filestorage.get_data(datatype, startday, endday, self.basedatapath, freq):
                        yield TrafficData(trafficdata=data, applyto='minute')
                        self.logger.debug('Archivist served {} data.'.format(datatype))
                except:
                    self.logger.error(traceback.format_exc())
                    self.logger.error('An error occurred while getting {} data for day {}.'
                                      .format(datatype, startday))
                    yield TrafficData(trafficdata=b'', applyto='day')
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while getting {} data between {} and {}.'
                              .format(datatype, datetime.to_string(fromdate), datetime.to_string(todate)))
            yield TrafficData(trafficdata=b'', applyto='all')
