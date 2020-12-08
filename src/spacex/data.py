import json
import datetime
import requests
import copy
from urllib.parse import urljoin


class SpaceXData(object):

    def __init__(self, host='https://api.spacexdata.com', version='v3'):
        """
        Instantiate a new API client.
        Args:
            host (str): Hostname of the factomd instance.
            version (str): API version to use. This should remain 'v2'.

        """
        self.version = version
        self.host = host

        # Initialize the session.
        self.session = requests.Session()

    # Convenience method for building request URLs.
    @property
    def url(self):
        return urljoin(self.host, self.version)

    def handle_error_response(self, resp):
        print(resp)
        raise RuntimeError("Response code not 200 go check code")

    # Perform an API request.
    def _request(self, path, params=None):
        fullpath = self.url + '/' + path
        resp = self.session.request('GET', fullpath, params=params)

        # If something goes wrong, we'll pass the response
        # off to the error-handling code
        if resp.status_code >= 400:
            self.handle_error_response(resp)

        # Otherwise return the result dictionary.
        return resp.json()

    # API methods
    def get_launches(self, **kwargs):
        return self._request('launches/'. format(kwargs.get('path', '')), kwargs)

    def get_payloads(self, flight_number):
        """ Fetch Payloads """
        flight = self.get_launches(path='upcoming', flight_number=flight_number)[0]
        payloads = flight.get('rocket').get('second_stage').get('payloads')
        return payloads

    def get_launch_date_range(self, start_date, end_date):
        # Input validation throws if invalid
        datetime.datetime.strptime(start_date, '%Y-%m-%d')
        datetime.datetime.strptime(end_date, '%Y-%m-%d')

        # Didn't paginate this, currently the API has a rate limit of
        # 50 req/sec and the total size of all launches (end 2020) was
        # about 815kB
        launches = self.get_launches(path='', start=start_date, end=end_date)
        return launches

    def get_largest_payload_flight_in_date_range(self, start_date, end_date):
        launches = self.get_launch_date_range(start_date, end_date)
        # Assuming that we're trying to find the largest payload of any
        # flight here rather than the flight with the largest sum of payloads.
        largest = -1
        result = None
        for flight in launches:
            payloads = flight.get('rocket').get('second_stage').get('payloads')
            max_payload = max([payload['payload_mass_kg'] for payload in payloads])
            if max_payload > largest:
                largest = max_payload
                result = flight

        return result

    def get_largest_total_mass_flight_in_date_range(self, start_date, end_date):
        launches = self.get_launch_date_range(start_date, end_date)
        # Assuming that we're taking the sum of all of the payloads in a given
        # flight and returning the flight with the largest sum
        largest = -1
        result = None
        for flight in launches:
            payloads = flight.get('rocket').get('second_stage').get('payloads')
            total_payloads = sum([payload['payload_mass_kg'] for payload in payloads])
            if total_payloads > largest:
                largest = total_payloads
                result = flight

        return result
