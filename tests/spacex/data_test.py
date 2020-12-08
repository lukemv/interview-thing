import pytest
from unittest.mock import Mock, patch

import sys
import datetime
import dateutil.parser
import requests

from spacex.data import SpaceXData


# This test covers enough of the original class methods
# to establish a working baseline
@pytest.mark.download
def test_payloads_when_id_1_returns_expected():
    sut = SpaceXData()
    pl = sut.get_payloads(1)
    assert len(pl) == 1
    assert pl[0]['payload_id'] == 'FalconSAT-2'


@pytest.mark.download
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


@pytest.mark.download
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


@pytest.mark.download
def test_all_launch_data_size():
    # Our API call to find the flight with the largest payload will
    # currently download all of the data unpaged, this test will report
    # the current size of all of the launch documents and print the
    # results
    sut = SpaceXData()
    resp = requests.get(f"{sut.url}/launches", stream=True)
    total_records = resp.headers["Spacex-Api-Count"]
    # The Content-Length header is missing so this is approximate
    total_size_kb = round(sys.getsizeof(resp.text) / 1024)

    print('Summary of launch data:')
    print(f'Total launch records: {total_records}')
    print(f'Total approx launch records size (uncompressed): {total_size_kb} kB')


class MockJsonSuccessResponse(object):
    def __init__(self, payload):
        self.payload = payload
        self.status_code = 200

    def json(self):
        return self.payload


class FlightStub(object):

    def __init__(self, flight_id):
        self.data = {
            'flight_id': flight_id,
            'rocket': {
                'second_stage': {
                    'payloads': []
                }
            }
        }

    def append_payload(self, payload_mass_kg):
        new_payload = {'payload_mass_kg': payload_mass_kg}
        self.data['rocket']['second_stage']['payloads'].append(new_payload)
        return self

    def asdict(self):
        return self.data


@patch('spacex.data.requests.Session')
def test_get_largest_payload_flight_in_date_range(mock_session):
    sut = SpaceXData()

    start = '2019-01-01'
    end = '2019-06-25'

    data = [
        FlightStub(1).append_payload(1).asdict(),
        FlightStub(2).append_payload(500).asdict(),
        FlightStub(3).append_payload(10).asdict()
    ]

    mock_session.return_value.request.return_value = MockJsonSuccessResponse(data)
    result = sut.get_largest_payload_flight_in_date_range(start, end)

    assert "flight_id" in result
    assert result.get('flight_id') == 2


@patch('spacex.data.requests.Session')
def test_get_largest_total_mass_flight_in_date_range(mock_session):
    sut = SpaceXData()

    start = '2019-01-01'
    end = '2019-06-25'

    data = [
        FlightStub(1).append_payload(10).append_payload(1).append_payload(1).asdict(),
        FlightStub(2).append_payload(10).append_payload(10).append_payload(10).asdict(),  # heavy.
        FlightStub(3).append_payload(1).append_payload(1).append_payload(1).asdict(),
    ]

    mock_session.return_value.request.return_value = MockJsonSuccessResponse(data)
    result = sut.get_largest_total_mass_flight_in_date_range(start, end)

    assert "flight_id" in result
    assert result.get('flight_id') == 2
