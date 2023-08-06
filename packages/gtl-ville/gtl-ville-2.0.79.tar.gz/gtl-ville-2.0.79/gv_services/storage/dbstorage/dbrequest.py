#!/usr/bin/env python3

import ujson

from gv_utils.csv import CSVSEP
import gv_utils.geometry as geometry


async def insert_data_type(dbpool, datatype):
    query = 'INSERT INTO data_type (eid) VALUES ($1) RETURNING id, eid;'
    return (await _run_fetch_request(dbpool, query, (datatype,)))[0]


async def insert_data_points(dbpool, datapoints):
    query = 'INSERT INTO data_point (eid, data_type, geom) ' \
            '(SELECT r.eid, r.data_type, r.geom FROM unnest($1::data_point[]) as r) ' \
            'RETURNING id, eid;'
    return _run_cursor_request(dbpool, query, (datapoints,), codecs=('geometry',))


async def insert_roads(dbpool, roads):
    query = 'INSERT INTO road (eid, att, web_att, geom) ' \
            '(SELECT r.eid, r.att, r.web_att, r.geom FROM unnest($1::road[]) as r) ' \
            'RETURNING id, eid;'
    return _run_cursor_request(dbpool, query, (roads,), codecs=('geometry', 'json'))


async def insert_roads_data_points(dbpool, roaddatapoints):
    await _run_copy_request(dbpool, 'road_data_point', roaddatapoints, ('road', 'data_point', 'valid_from'))


async def insert_data_points_indicators(dbpool, datapointsindicators):
    await _run_copy_request(dbpool, 'data_point_indicator', datapointsindicators,
                            ('data_point', 'sample_timestamp', 'sample'), codecs=('json',))


async def insert_roads_indicators(dbpool, roadsindicators):
    await _run_copy_request(dbpool, 'road_indicator', roadsindicators, ('road', 'sample_timestamp', 'sample'),
                            codecs=('json',))


async def update_roads_ffspeeds(dbpool, eidsffspeeds):
    query = 'UPDATE road SET att = att || $1 WHERE eid=$2;'
    await _run_executemany_request(dbpool, query, [({'ffspeed': v}, k) for k, v in eidsffspeeds.items()],
                                   codecs=('geometry', 'json'))


async def select_data_types_ids(dbpool, eids=None):
    query = 'SELECT jsonb_object_agg(eid, id) AS res FROM data_type'

    whereclause = ''
    whereparams = ()
    if eids is not None:
        whereclause, whereparams = _add_where_condition(' WHERE ', whereparams,
                                                        _build_where_clause_for_eids_fields, (eids, 'eid'))
    query += whereclause + ';'
    return (await _run_fetch_request(dbpool, query, whereparams, codecs=('json',)))[0]['res']


async def select_data_points_ids(dbpool, eids=None, datatypeseids=None, geom=None):
    query = 'SELECT jsonb_object_agg(data_point.eid, data_point.id) AS res ' \
            'FROM data_point INNER JOIN data_type ON data_point.data_type = data_type.id'

    whereclause = ''
    whereparams = ()
    if eids is not None or datatypeseids is not None or geom is not None:
        whereclause = ' WHERE '
        if eids is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_eids_fields,
                                                            (eids, 'data_point.eid'))
        if datatypeseids is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_eids_fields,
                                                            (datatypeseids, 'data_type.eid'))
        if geom is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_geom, (geom, 'geom'))
    query += whereclause + ';'
    return (await _run_fetch_request(dbpool, query, whereparams, codecs=('geometry', 'json')))[0]['res']


async def select_data_points(dbpool, eids=None, datatypeseids=None, geom=None):
    query = 'SELECT jsonb_object_agg(data_point.eid, json_build_object(\'id\', data_point.id, \'eid\', ' \
            'data_point.eid, \'datatypeeid\', data_type.eid, \'geom\', ST_AsText(data_point.geom))) AS res ' \
            'FROM data_point INNER JOIN data_type ON data_point.data_type = data_type.id'

    whereclause = ''
    whereparams = ()
    if eids is not None or datatypeseids is not None or geom is not None:
        whereclause = ' WHERE '
        if eids is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_eids_fields,
                                                            (eids, 'data_point.eid'))
        if datatypeseids is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_eids_fields,
                                                            (datatypeseids, 'data_type.eid'))
        if geom is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_geom, (geom, 'geom'))
    query += whereclause + ';'
    return (await _run_fetch_request(dbpool, query, whereparams, codecs=('geometry', 'json')))[0]['res']


async def select_roads_ids(dbpool, eids=None, geom=None):
    query = 'SELECT jsonb_object_agg(eid, id) AS res FROM road'

    whereclause = ''
    whereparams = ()
    if eids is not None or geom is not None:
        whereclause = ' WHERE '
        if eids is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_eids_fields, (eids, 'eid'))
        if geom is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_geom, (geom, 'geom'))
    query += whereclause + ';'
    return (await _run_fetch_request(dbpool, query, whereparams, codecs=('geometry', 'json')))[0]['res']


async def select_roads(dbpool, eids=None, geom=None):
    query = 'SELECT jsonb_object_agg(eid, json_build_object(\'id\', id, \'eid\', eid, \'geom\', ST_AsText(geom), ' \
            '\'webatt\', web_att, \'att\', att)) AS res ' \
            'FROM road'

    whereclause = ''
    whereparams = ()
    if eids is not None or geom is not None:
        whereclause = ' WHERE '
        if eids is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_eids_fields, (eids, 'eid'))
        if geom is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_geom, (geom, 'geom'))
    query += whereclause + ';'
    return (await _run_fetch_request(dbpool, query, whereparams, codecs=('geometry', 'json')))[0]['res']


async def select_roads_data_points_eids(dbpool, reids=None, dpeids=None, validat=None):
    query = 'SELECT road.eid AS reid, array_agg(data_point.eid) AS dpeid ' \
            'FROM road_data_point ' \
            'INNER JOIN road ON road_data_point.road = road.id ' \
            'INNER JOIN data_point ON road_data_point.data_point = data_point.id '

    whereclause = ''
    whereparams = ()
    if reids is not None or dpeids is not None or validat is not None:
        whereclause = ' WHERE '
        if reids is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_eids_fields, (reids, 'road.eid'))
        if dpeids is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_eids_fields,
                                                            (dpeids, 'data_point.eid'))
        if validat is not None:
            whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                            _build_where_clause_for_valids_fields,
                                                            (None, None, validat))
    query = 'SELECT jsonb_object_agg(agg.reid, agg.dpeid) AS res FROM ( ' + query + whereclause + \
            ' GROUP BY road.eid) AS agg;'
    return (await _run_fetch_request(dbpool, query, whereparams))[0]['res']


async def select_data_points_indicators_eids(dbpool, datatypeid, fromdate, todate, geom=None):
    query = 'SELECT COALESCE(string_agg(DISTINCT data_point.eid, $1), \'\') AS res ' \
            'FROM data_point ' \
            'INNER JOIN road_data_point ON road_data_point.data_point = data_point.id '

    whereclause, whereparams = _add_where_condition(' WHERE ', (CSVSEP,), _build_where_clause_for_eids_fields,
                                                    (datatypeid, 'data_point.data_type'), 2)
    whereclause, whereparams = _add_where_condition(whereclause, whereparams, _build_where_clause_for_valids_fields,
                                                    (fromdate, todate, None))
    if geom is not None:
        whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                        _build_where_clause_for_geom, (geom, 'data_point.geom'))
    query += whereclause + ';'
    return (await _run_fetch_request(dbpool, query, whereparams, codecs=('geometry',)))[0]['res']


async def select_roads_indicators_eids(dbpool, fromdate, todate, geom=None):
    query = 'SELECT COALESCE(string_agg(DISTINCT road.eid, $1), \'\') AS res ' \
            'FROM road ' \
            'INNER JOIN road_data_point ON road_data_point.road = road.id ' \

    whereclause, whereparams = _add_where_condition(' WHERE ', (CSVSEP,), _build_where_clause_for_valids_fields,
                                                    (fromdate, todate, None), 2)
    if geom is not None:
        whereclause, whereparams = _add_where_condition(whereclause, whereparams,
                                                        _build_where_clause_for_geom, (geom, 'road.geom'))
    query += whereclause + ';'
    return (await _run_fetch_request(dbpool, query, whereparams, codecs=('geometry',)))[0]['res']


def _add_where_condition(whereclause, whereparams, build_func, funcparams, paramindex=None):
    if paramindex is None:
        paramindex = len(whereparams) + 1
        if paramindex > 1:
            whereclause += ' AND '
    condition, params = build_func(*funcparams, paramindex)
    whereclause += condition
    whereparams += params
    return whereclause, whereparams


def _build_where_clause_for_eids_fields(eids, fieldname, paramindex):
    if (isinstance(eids, set) or isinstance(eids, tuple) or isinstance(eids, list)) and len(eids) == 1:
        eids = eids[0]
    if isinstance(eids, str) or isinstance(eids, int):
        wherequery = fieldname + '=$' + str(paramindex)
        whereparams = (eids,)
    else:
        wherequery = fieldname + '=any($' + str(paramindex) + '::varchar[])'
        whereparams = (eids,)
    return wherequery, whereparams


def _build_where_clause_for_geom(geomval, fieldname, paramindex):
    wherequery = 'ST_Intersects(' + fieldname + ', $' + str(paramindex) + '::geometry)'
    whereparams = (geomval,)
    return wherequery, whereparams


def _build_where_clause_for_valids_fields(validfrom, validto, validat, paramindex):
    wherequery = 'road_data_point.valid_to IS NULL'
    whereparams = ()
    if validfrom is not None and validfrom is not None:
        wherequery = 'road_data_point.valid_from<=$' + str(paramindex) + ' AND (road_data_point.valid_to IS NULL OR' + \
                     ' road_data_point.valid_to>=$' + str(paramindex+1) + ')'
        whereparams = (validto, validfrom)
    elif validat is not None:
        wherequery = 'road_data_point.valid_from<=$' + str(paramindex) + ' AND (road_data_point.valid_to IS NULL OR' + \
                     ' road_data_point.valid_to>=$' + str(paramindex) + ')'
        whereparams = (validat,)
    return wherequery, whereparams


async def _run_copy_request(dbpool, tablename, records, columns, codecs=()):
    async with dbpool.acquire() as conn:
        await _set_codecs(conn, codecs)
        async with conn.transaction():
            await conn.copy_records_to_table(tablename, records=records, columns=columns)


async def _run_executemany_request(dbpool, query, params, codecs=()):
    async with dbpool.acquire() as conn:
        await _set_codecs(conn, codecs)
        async with conn.transaction():
            await conn.executemany(query, params)


async def _run_cursor_request(dbpool, query, params, codecs=()):
    async with dbpool.acquire() as conn:
        await _set_codecs(conn, codecs)
        async with conn.transaction():
            async for record in conn.cursor(query, *params):
                yield record


async def _run_fetch_request(dbpool, query, params, codecs=()):
    async with dbpool.acquire() as conn:
        await _set_codecs(conn, codecs)
        async with conn.transaction():
            return await conn.fetch(query, *params)


async def _set_codecs(conn, codecs):
    for codec in codecs:
        if codec == 'geometry':
            await _set_geom_codec(conn)
        elif codec == 'json':
            await _set_json_codec(conn)


async def _set_geom_codec(conn):
    await conn.set_type_codec(
        'geometry',
        encoder=geometry.encode_geometry,
        decoder=geometry.decode_geometry,
        format='binary',
    )


async def _set_json_codec(conn):
    await conn.set_type_codec(
        'jsonb',
        encoder=lambda value: b'\x01' + ujson.dumps(value).encode('utf-8'),
        decoder=lambda value: ujson.loads(value[1:].decode('utf-8')),
        schema='pg_catalog',
        format='binary'
    )
