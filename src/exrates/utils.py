import datetime
import calendar

import requests


class ExchangeRateData(object):

    def __init__(self, host='https://api.exchangeratesapi.io'):
        """
        Instantiate a new API client.
        Args:
            host (str): Hostname of the API endpoint.

        """
        self.host = host

        # Initialize the session.
        self.session = requests.Session()

    @property
    def url(self):
        return self.host

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

    def get_rates(self, year, month, day):
        path = f"{year}-{month:02d}-{day:02d}"
        resp = self._request(path)
        assert 'rates' in resp
        return resp['rates']

    def get_rates_in_month(self, year, month, symbol):
        num_days = calendar.monthrange(year, month)[1]
        aggregate = []

        for day in range(1, num_days + 1):
            resp = self.get_rates(year, month, day)

            date = f"{year}-{month:02d}-{day:02d}"
            rate = resp[symbol]

            aggregate.append((date, rate))

        return aggregate

    def get_best_rate_in_month(self, year, month, symbol):
        rates = self.get_rates_in_month(year, month, symbol)
        high = -1
        result = None
        for i in rates:
            if high <= i[1]:
                high = i[1]
                result = i

        return result

    def get_best_rate_in_previous_month(self, symbol):
        today = datetime.date.today()
        first = today.replace(day=1)
        prev = first - datetime.timedelta(days=1)
        return self.get_best_rate_in_month(prev.year, prev.month, symbol)
