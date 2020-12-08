import pytest
from freezegun import freeze_time

from exrates.data import ExchangeRateData


@pytest.mark.download
def test_get_rates():
    sut = ExchangeRateData()
    rates = sut.get_rates(2020, 2, 1)
    assert 'AUD' in rates
    assert 'HKD' in rates


@pytest.mark.download
def test_get_rates_in_month():
    sut = ExchangeRateData()
    rates = sut.get_rates_in_month(2020, 2, 'AUD')
    assert len(rates) == 29


@pytest.mark.download
def test_get_best_rate_in_month():
    sut = ExchangeRateData()
    result = sut.get_best_rate_in_month(2019, 5, 'AUD')
    assert result[0] == '2019-05-19'
    assert result[1] == 1.6239


@pytest.mark.download
@freeze_time("2019-06-10")
def test_get_best_rate_in_previous_month():
    sut = ExchangeRateData()
    result = sut.get_best_rate_in_previous_month('AUD')
    assert result[0] == '2019-05-19'
    assert result[1] == 1.6239
