import click
import json
from spacex.data import SpaceXData
from exrates.data import ExchangeRateData


@click.group()
def main():
    pass


@main.command()
@click.argument('date-start')
@click.argument('date-end')
def spacex_launches_by_date(date_start, date_end):
    data = SpaceXData()
    results = data.get_launch_date_range(date_start, date_end)
    print(json.dumps(results))


@main.command()
@click.argument('date-start')
@click.argument('date-end')
def spacex_biggest_payload_flight(date_start, date_end):
    data = SpaceXData()
    results = data.get_largest_payload_flight_in_date_range(date_start, date_end)
    print(json.dumps(results))


@main.command()
@click.argument('year')
@click.argument('month')
@click.argument('symbol')
def exrates_rates_in_month(year, month, symbol):
    data = ExchangeRateData()
    results = data.get_rates_in_month(int(year), int(month), symbol)
    for item in results:
        print(f'{item[0]} {item[1]}')


@main.command()
@click.argument('year')
@click.argument('month')
@click.argument('symbol')
def exrates_best_rate_in_month(year, month, symbol):
    data = ExchangeRateData()
    result = data.get_best_rate_in_month(int(year), int(month), symbol)
    print(f'{result[0]} {result[1]}')


@main.command()
@click.argument('symbol')
def exrates_best_rate_in_prev_month(symbol):
    data = ExchangeRateData()
    result = data.get_best_rate_in_previous_month(symbol)
    print(f'{result[0]} {result[1]}')


if __name__ == '__main__':
    main()
