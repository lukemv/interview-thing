import pytest
import datetime
import dateutil.parser

from spacex.data import SpaceXData


# This test covers enough of the original class methods
# to establish a working baseline
def test_payloads_when_id_1_returns_expected():
    sut = SpaceXData()
    pl = sut.get_payloads(1)
    assert len(pl) == 1
    assert pl[0]['payload_id'] == 'FalconSAT-2'


def test_get_lauchdate_when_dates_valid():
    sut = SpaceXData()

    # These dates are assumed to be aligned
    # with the UTC timezone.
    start = '2019-01-01'
    end = '2019-06-25'

    results = sut.get_launch_date_range(start, end)

    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    # for now we'll just handle the live data.
    assert results is not None
    assert len(results) > 0

    # and add some smoke test to check that all dates are within
    # our specified range.
    for launch in results:
        assert 'launch_date_utc' in launch
        launch_date = dateutil.parser.isoparse(launch['launch_date_utc']).date()
        assert launch_date >= start_date
        assert launch_date <= end_date


def test_get_lauchdate_when_date_invalid():
    sut = SpaceXData()

    start_date = 'INVALID_STR'
    end_date = 'INVALID_STR'

    # The default behaviour of the SpaceX API when given
    # the above invalid date is to return a 200 with an empty
    # list i.e.
    r1 = sut.get_launches(path='', start=start_date, end=end_date)
    assert r1 == []

    # Our method will parse the date string to fail fast.
    with pytest.raises(ValueError):
        r2 = sut.get_launch_date_range(start_date=start_date, end_date=end_date)
