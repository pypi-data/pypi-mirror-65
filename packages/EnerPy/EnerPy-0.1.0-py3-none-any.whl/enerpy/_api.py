# ##############################################################################
#  EnerPy (_api.py)
#  Copyright (C) 2020 Daniel Sullivan <daniel.sullivan@state.mn.us>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ##############################################################################

import enum
from collections import UserDict
from datetime import datetime
from typing import Dict, Union, Any, List, Optional

import pandas as pd
import requests
from logger_mixin import LoggerMixin

# global variable for default row count parameter
NUM_OF_ROWS = 1000

# global variables with error messages from eia API
INVALID_SERIES_ID = 'invalid series_id. For key registration, ' \
                    'documentation, and examples see'

INVALID_API_KEY = 'invalid or missing api_key. For key registration, ' \
                  'documentation, and examples see'


class Frequency(enum.Enum):
    ANNUAL = 1
    QUARTERLY = 4
    MONTHLY = 12
    DAILY = 365
    HOURLY = 8760

    @classmethod
    def from_code(cls, code):
        codes = {
            'A': cls.ANNUAL,
            'Q': cls.QUARTERLY,
            'M': cls.MONTHLY,
            'D': cls.DAILY,
            'H': cls.HOURLY
        }
        return codes[code.upper()]


DATE_FORMATS = {
    4: ('%Y', Frequency.ANNUAL),
    6: ('%Y%m', Frequency.MONTHLY),
    8: ('%Y%m%d', Frequency.DAILY),
    12: ('%Y%m%dT%HZ', Frequency.HOURLY)
}


# region Exceptions
class APIKeyError(Exception):
    pass


class NoResultsError(Exception):
    pass


class BroadCategory(Exception):
    pass


class DateFormatError(Exception):
    pass


class InvalidSeries(Exception):
    pass


class UndefinedError(Exception):
    pass


class SeriesTypeError(Exception):
    pass


# endregion

class Series(UserDict):
    id: str

    def __init__(self, name, units, frequency, id):
        freq = Frequency.from_code(frequency)
        super().__init__(name=name, units=units, frequency=freq, id=id)

    @property
    def name(self):
        return self['name']

    @property
    def units(self):
        return self['units']

    @property
    def frequency(self):
        return self['frequency']

    @property
    def id(self):
        return self['id']

    @property
    def data_points(self):
        return self['data_points']

    @classmethod
    def from_series_json(cls, ser_json):
        ret = cls(ser_json.pop('name'),
                  ser_json.pop('units'),
                  ser_json.pop('f'),
                  ser_json.pop('series_id'))

        data = ser_json.pop('data')
        ret.update(ser_json)
        pts = ((cls._parse_date(k)[0], v) for k, v in data)

        df = pd.DataFrame(pts, columns=['date', 'value'])
        ret['data_points'] = df.set_index('date')
        return ret

    @property
    def msn(self):
        if self.id.startswith('SEDS.'):
            return self.id[5:10]
        else:
            raise SeriesTypeError(f'"{self.id}" is not a SEDS series')

    @staticmethod
    def _parse_date(date: str):
        if date.find('Q') == 4:
            return datetime(int(date[:4]), int(date[5]) * 3, 1), Frequency.QUARTERLY
        fmt, freq = DATE_FORMATS[len(date)]
        return datetime.strptime(date, fmt), freq


class API(LoggerMixin, object):
    def __init__(self, token: str):
        """

        Args:
            token: EIA Token, obtainable from https://www.eia.gov/opendata/
        """
        super().__init__()
        self._session = requests.session()
        self._base_params = dict(api_key=token, out='json')

    def _search(self, base_url: str, params: Dict[str, object]) -> Dict[Any, Any]:
        """

        Args:
            base_url:
            params:

        Returns:
           JSON decoded dictionary of returned value

        """
        params.update(self._base_params)
        params = {k: v for k, v in params.items() if v is not None}
        r = self._session.get(base_url, params=params)
        self.logger.debug(r.url)
        js = r.json()
        if 'data' in js:
            if js['data'].get('error').startswith(INVALID_API_KEY):
                self.log_and_raise(APIKeyError(js['data']['error']))
        return js

    def search_by_category(self,
                           category: int,
                           max_depth: int = 5):
        """API Category Query

        Args:
            category: EIA Category number
            max_depth: Max depth to recurse in child categories

        Returns:
            Dictionary of series found keyed by series id

        Raises:
            BroadCategory: Recursed to deep, probably should try a child category or increase depth
            NoResultsError: No results found

        """
        search_url = 'http://api.eia.gov/category/'
        json = self._search(search_url,
                            dict(
                                category_id=category
                            ))
        categories_dict = {}
        if 'data' in json and json['data'].get('error') == 'No result found.':
            self.log_and_raise(NoResultsError("No Result Found. Try A Different Category ID"))

        if 'category' in json:
            if 'childseries' in json['category']:
                for k in json['category']['childseries']:
                    categories_dict[k['series_id']] = Series(k['name'], k['units'], k['f'], k['series_id'])
            if 'childcategories' in json['category']:
                # print(json['category']['childcategories'])
                md = max_depth - 1
                if md <= 0:
                    self.log_and_raise(
                        BroadCategory('Category ID is Too Broad. Try Narrowing '
                                      'Your Search with a Child Category.'
                                      ))
                for k in json['category']['childcategories']:
                    self.logger.debug(f'Category Search depth: {md}')
                    categories_dict.update(self.search_by_category(k['category_id'], max_depth=md))
        return categories_dict

    def search_by_keyword(self,
                          keyword: Union[List[str], str],
                          rows: int = NUM_OF_ROWS,
                          data_set: Optional[str] = None):
        """API Search Data Query - Keyword

        Args:
            keyword:
            rows:
            data_set:

        Returns:

        """
        """
        API Search Data Query - Keyword
        :param keyword: list or string
        :param rows: string
        :param data_set: string
        :return: If return_list is false, returns a dictionary of search results
        (name, units, frequency, and series ID) based on keyword.
        If return_list is true, returns a list of search results (name, only).
        """
        if isinstance(keyword, list):
            keyword = ' '.join(keyword)
        search_url = 'http://api.eia.gov/search/'
        json = self._search(search_url,
                            dict(
                                search_term='name',
                                search_value=keyword,
                                rows_per_page=rows,
                                data_set=data_set
                            ))
        categories_dict = {}

        if 'response' in json:
            if 'docs' not in json['response'] or not json['response']['docs']:
                self.log_and_raise(NoResultsError('No Results Found'))
            for k in json['response']['docs']:
                categories_dict[k['series_id']] = Series(k['name'][0], k['units'], k['frequency'], k['series_id'])

        return categories_dict

    def search_by_date(self,
                       start_date: datetime,
                       end_date: datetime,
                       rows: int = NUM_OF_ROWS):
        """API Search Data Query - Date Search

        Args:
            start_date:
            end_date:
            rows:

        Returns:

        """
        search_url = 'http://api.eia.gov/search/'
        json = self._search(search_url,
                            dict(
                                search_term='last_updated',
                                search_value=f'[{start_date.isoformat(timespec="seconds")}Z '
                                             f'TO {end_date.isoformat(timespec="seconds")}Z]',
                                rows_per_page=rows))
        categories_dict = {}
        if 'error' in json and json['error'] == 'solr connection failed.':
            self.log_and_raise(DateFormatError("Connection Failed. Check date format. "
                                               "Date should be in the following format:"
                                               "'2014-01-01T00:00:00Z TO "
                                               "2015-01-01T23:59:59Z'"))
        if 'response' in json:
            if 'docs' not in json['response'] or not json['response']['docs']:
                self.log_and_raise(NoResultsError('No Results Found'))
            for k in json['response']['docs']:
                categories_dict[k['series_id']] = Series(k['name'][0], k['units'], k['frequency'], k['series_id'])

        return categories_dict

    def _get_data(self, params):
        url = 'http://api.eia.gov/series/'
        params.update(self._base_params)
        r = self._session.get(url, params=params)
        js = r.json()
        if 'data' in js and 'error' in js['data'] and js['data']['error'].startswith(INVALID_SERIES_ID):
            return None
        return js

    def _get_series_data(self, series_list):
        values_dict = {}
        for series_id in series_list:
            data = self._get_data(dict(series_id=series_id))
            if data is None:
                continue
            for s in data['series']:
                s_data = Series.from_series_json(s)
                values_dict[s_data.id] = s_data
        return values_dict

    def data_by_category(self,
                         category: int):
        """API Category Query

        Args:
            category:

        Returns:

        """
        categories_dict = self.search_by_category(category)
        return self._get_series_data(categories_dict.keys())

    def data_by_keyword(self,
                        keyword: Union[str, List[str]],
                        rows: int = NUM_OF_ROWS,
                        data_set: str = None):
        """API Search Data Query - Keyword

        Args:
            keyword:
            rows:
            data_set:

        Returns:

        """
        categories_dict = self.search_by_keyword(keyword,
                                                 rows,
                                                 data_set=data_set)

        return self._get_series_data(categories_dict.keys())

    def data_by_date(self,
                     start_date, end_date, rows=NUM_OF_ROWS):
        """API Search Data Query - Date Search

        Args:
            start_date: Start date of data
            end_date: End date of data
            rows: Number of rows to return

        Returns:

        """
        """
        :param rows: string
        :return: Returns eia data series in dictionary form
        (name, units, frequency, and series ID) based on last update date.
        """
        categories_dict = self.search_by_date(start_date=start_date, end_date=end_date, rows=rows)
        return self._get_series_data(categories_dict.keys())

    def data_by_series(self,
                       series: str):
        """API Series Query

        Args:
            series:

        Returns:

        """
        return self._get_series_data((series,))
