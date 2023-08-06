##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import pytest
import random
import uuid
import timeit

import flatbuffers
from txaio import with_twisted  # noqa

from txaio import time_ns
from autobahn import util
import zlmdb

from cfxdb.eventstore import Session

zlmdb.TABLES_BY_UUID = {}


def fill_session(session):
    session.session = util.id()
    session.joined_at = time_ns() - 723 * 10**9
    session.left_at = time_ns()
    session.realm = 'realm-{}'.format(uuid.uuid4())
    session.authid = util.generate_serial_number()
    session.authrole = random.choice(['admin', 'user*', 'guest', 'anon*'])


@pytest.fixture(scope='function')
def builder():
    _builder = flatbuffers.Builder(0)
    return _builder


@pytest.fixture(scope='function')
def session():
    _session = Session()
    fill_session(_session)
    return _session


def test_session_roundtrip(session, builder):
    # serialize to bytes (flatbuffers) from python object
    obj = session.build(builder)
    builder.Finish(obj)
    data = builder.Output()
    assert len(data) == 160

    # create python object from bytes (flatbuffes)
    _session = Session.cast(data)

    assert _session.session == session.session
    assert _session.joined_at == session.joined_at
    assert _session.left_at == session.left_at
    assert _session.realm == session.realm
    assert _session.authid == session.authid
    assert _session.authrole == session.authrole


def test_session_roundtrip_perf(session, builder):
    obj = session.build(builder)
    builder.Finish(obj)
    data = builder.Output()
    scratch = {'joined_at': 0}

    def loop():
        _session = Session.cast(data)
        if True:
            assert _session.session == session.session
            assert _session.joined_at == session.joined_at
            assert _session.left_at == session.left_at
            assert _session.realm == session.realm
            assert _session.authid == session.authid
            assert _session.authrole == session.authrole

            scratch['joined_at'] += session.joined_at

    N = 5
    M = 100000
    samples = []
    print('measuring:')
    for i in range(N):
        secs = timeit.timeit(loop, number=M)
        ops = round(float(M) / secs, 1)
        samples.append(ops)
        print('{} objects/sec performance'.format(ops))

    samples = sorted(samples)
    ops50 = samples[int(len(samples) / 2)]
    print('RESULT: {} objects/sec median performance'.format(ops50))

    assert ops50 > 1000
    assert scratch['joined_at'] > 0
