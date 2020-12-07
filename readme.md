# IMC SE Trading – Python Coding Questions

We have a class that provides an easier way to retrieve data from the internet. In this example we have chosen to use SpaceX as they offer up to date data. In the class shown above we want to extend some features.

API Documentation: [https://docs.spacexdata.com/?version=latest](https://docs.spacexdata.com/?version=latest)


## Question 1

While debugging any issue’s that may arise, we want to add a new method to allow us to specify date specific launches and returns a list . The output should be something like:

```
>>> spacex.get_launch_date_range('2019-01-01', '2019-06-25')

[{'details': "SpaceX's first flight of 2019 will be the eighth and final "
             'launch of its planned Iridium flights. Delivering 10 satellites '
             'to low earth orbit, this brings the total up to 75 and completes '
             'the Iridium NEXT constellation. This mission launches from '
             'SLC-4E at Vandenberg AFB. The booster is expected to land on '
             'JRTI.',
  'flight_number': 74,
  'is_tentative': False,
  'launch_date_local': '2019-01-11T07:31:00-08:00',
  'launch_date_unix': 1547220660,
  'launch_date_utc': '2019-01-11T15:31:00.000Z',
  'launch_site': {'site_id': 'vafb_slc_4e',
                  'site_name': 'VAFB SLC 4E',
                  'site_name_long': 'Vandenberg Air Force Base Space Launch '
                                    'Complex 4E'},
```


## Question 2

Continuation from the previous question we want to build another method to return a flight with the heaviest payload given a date range. The output should be something like

```
{'details': 'SpaceX will launch Arabsat 6A to a geostationary transfer orbit '
            'from SLC-39A, KSC. The satellite is a geostationary '
            'telecommunications satellite built by Lockheed Martin for the '
            'Saudi Arabian company Arabsat. This will be the first operational '
            'flight of Falcon Heavy, and also the first Block 5 Falcon Heavy. '
            'All three cores will be new Block 5 cores. The side cores are '
            'expected to land at LZ-1 and LZ-2, and the center core is '
            'expected to land on OCISLY.',
 'flight_number': 77,
 'is_tentative': False,
 'launch_date_local': '2019-04-11T18:35:00-04:00',
 'launch_date_unix': 1555022100,
 'launch_date_utc': '2019-04-11T22:35:00.000Z',
 'launch_site': {'site_id': 'ksc_lc_39a',
                 'site_name': 'KSC LC 39A',
                 'site_name_long': 'Kennedy Space Center Historic Launch '
                                   'Complex 39A'},
 'launch_success': True,
 'launch_window': 7020,
 'launch_year': '2019',
...
                                       'second_stage': {'block': 5,
                                                        'payloads': [{'customers': ['Arabsat'],
                                                                      'manufacturer': 'Lockheed Martin',
                                                                      'nationality': 'Saudi Arabia',
                                                                      'norad_id': [44186],
                                                                      'payload_id': 'ArabSat 6A',
                                                                      'payload_mass_kg': 6000,
                                                                      'payload_mass_lbs': 13227.74,
                                                                      'payload_type': 'Satellite',
                                                                      'reused': False}]}},
```

## Question 3

In the following example determine the date where the Australian dollar had the best exchange rate for the previous month.  You will need to fetch data for each day in that month, extract the Australian dollar rate (AUD).  Write a function to return as a tuple the date and best rate.
 
The daily data (for example May 1st 2019) can be fetched from [https://api.exchangeratesapi.io/2019-05-01](https://api.exchangeratesapi.io/2019-05-01), and the requests library is recommended. Return the latest date if there are multiple dates with the same highest exchange rate.
 
For example where May 5th had the highest AUD value the result would look something like:

```
>>>best_rate()
'2019-05-19', 1.6239
```