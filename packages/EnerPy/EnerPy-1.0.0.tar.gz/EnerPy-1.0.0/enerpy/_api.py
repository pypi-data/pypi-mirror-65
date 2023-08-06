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

from datetime import datetime
from itertools import count
from pprint import pformat
from typing import Dict, Union, Any, List, Optional, Callable

import requests
from logger_mixin import LoggerMixin

import enerpy
from enerpy._types import EIASeries

ROWS_PER_PAGE = 5000
# region Constants
INVALID_SERIES_ID = 'invalid series_id. For key registration, ' \
                    'documentation, and examples see'

INVALID_API_KEY = 'invalid or missing api_key. For key registration, ' \
                  'documentation, and examples see'

EIA_BASE_URL = 'http://api.eia.gov/'
EIA_CATEGORY = 'category/'
EIA_SEARCH = 'search/'
EIA_SERIES = 'series/'

# TODO: Important! Don't kill the EIA!
EIA_UPDATES = 'updates/'

# TODO: Geoset/relation not implemented
EIA_GEOSET = 'geoset/'
EIA_RELATION = 'relation/'

# TODO: Not implemented.
#   Gets a list of category names and IDs the series is a member of.
EIA_SERIES_CATEGORIES = 'series/categories'


# endregion

class API(LoggerMixin, object):
    def __init__(self, token: str):
        """

        Args:
            token: EIA Token, obtainable from https://www.eia.gov/opendata/
        """
        super().__init__()
        self._session = requests.session()
        self._base_params = dict(api_key=token, out='json')

    def _query(self, url_path: str, params: Dict[str, object]) -> requests.Response:
        params.update(self._base_params)
        params = {k: v for k, v in params.items() if v is not None}
        r = self._session.get(EIA_BASE_URL + url_path, params=params)
        return r

    def _search(self, url_path: str, params: Dict[str, object]) -> Dict[Any, Any]:
        """

        Args:
            url_path:
            params:

        Returns:
           JSON decoded dictionary of returned value

        """
        r = self._query(url_path, params)
        js = r.json()
        if 'data' in js:
            if js['data'].get('error').startswith(INVALID_API_KEY):
                self.log_and_raise(enerpy.APIKeyError(js['data']['error']))
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
        json = self._search(EIA_CATEGORY,
                            dict(
                                category_id=category,
                                rows_per_page=ROWS_PER_PAGE
                            ))
        categories_dict = {}
        if 'data' in json and json['data'].get('error') == 'No result found.':
            self.log_and_raise(enerpy.NoResultsError("No Result Found. Try A Different Category ID"))

        if 'category' in json:
            if 'childseries' in json['category']:
                for k in json['category']['childseries']:
                    categories_dict[k['series_id']] = EIASeries(k['name'], k['units'], k['f'], k['series_id'])
            if 'childcategories' in json['category']:
                # print(json['category']['childcategories'])
                md = max_depth - 1
                if md <= 0:
                    self.log_and_raise(
                        enerpy.BroadCategory('Category ID is Too Broad. Try Narrowing '
                                             'Your Search with a Child Category.'
                                             ))
                for k in json['category']['childcategories']:
                    self.logger.debug(f'Category Search depth: {md}')
                    categories_dict.update(self.search_by_category(k['category_id'], max_depth=md))
        return categories_dict

    def _search_data_query(self, search_term, search_value, data_set):
        params = dict(
            search_term=search_term,
            search_value=search_value,
            rows_per_page=ROWS_PER_PAGE,
            data_set=data_set
        )
        categories_dict = {}
        for pn in count(0, 1):
            params['page_num'] = pn
            json = self._search(EIA_SEARCH, params)
            if 'response' not in json:
                break
            if ('docs' not in json['response'] or not json['response']['docs']) \
                    and json['response']['numFound'] == 0:
                self.logger.error(pformat(json['response']))
                self.log_and_raise(enerpy.NoResultsError('No Results Found'))
            for k in json['response']['docs']:
                categories_dict[k['series_id']] = EIASeries(k['name'][0], k['units'], k['frequency'], k['series_id'])
            if len(json['response']['docs']) < ROWS_PER_PAGE:
                break
        return categories_dict

    def search_by_series_id(self,
                            series_id: str,
                            data_set: Optional[str] = None):
        """API Search Data Query - Series ID

        Args:
            series_id:
            data_set:

        Returns:

        """
        return self._search_data_query('series_id', series_id, data_set)

    def search_by_keyword(self,
                          keyword: Union[List[str], str],
                          data_set: Optional[str] = None):
        """API Search Data Query - Keyword

        Args:
            keyword:
            data_set:

        Returns:

        """
        if isinstance(keyword, list):
            keyword = ' '.join(keyword)
        return self._search_data_query('name', keyword, data_set)

    def search_by_date(self,
                       start_date: datetime,
                       end_date: datetime,
                       data_set: Optional[str] = None):
        """API Search Data Query - Date Search

        Args:
            start_date:
            end_date:
            data_set:

        Returns:

        """
        return self._search_data_query(
            'last_updated',
            f'[{start_date.isoformat(timespec="seconds")}Z TO {end_date.isoformat(timespec="seconds")}Z]',
            data_set)

    def updated_series(self, updated_after: datetime,
                       starting_category: int = None,
                       deep: bool = True,
                       series_filter: Callable[[str], bool] = lambda x: True):
        """Finds series that have been updated

        Args:
            updated_after:
            starting_category:
            deep:
            series_filter:

        Returns:

        """
        if updated_after.tzinfo is None:
            updated_after = updated_after.astimezone()
        updated_series = []
        for start_row in count(1, ROWS_PER_PAGE):
            r = self._query(EIA_UPDATES,
                            dict(
                                category_id=starting_category,
                                deep=deep,
                                rows=ROWS_PER_PAGE,
                                firstrow=start_row
                            ))
            r = r.json()
            for s_update in r['updates']:
                updated = datetime.strptime(s_update['updated'], '%Y-%m-%dT%H:%M:%S%z')
                if updated >= updated_after:
                    if series_filter(s_update['series_id']):
                        updated_series.append(s_update['series_id'])
                else:
                    return updated_series
            if r['data']['rows_returned'] < ROWS_PER_PAGE:
                break
        return updated_series

    def _get_data(self, params):
        r = self._query(EIA_SERIES, params)
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
                s_data = EIASeries.from_series_json(s)
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
                        data_set: str = None):
        """API Search Data Query - Keyword

        Args:
            keyword:
            data_set:

        Returns:

        """
        categories_dict = self.search_by_keyword(keyword,
                                                 data_set=data_set)

        return self._get_series_data(categories_dict.keys())

    def data_by_date(self,
                     start_date, end_date):
        """API Search Data Query - Date Search

        Args:
            start_date: Start date of data
            end_date: End date of data

        Returns:

        """
        """
        :param rows: string
        :return: Returns eia data series in dictionary form
        (name, units, frequency, and series ID) based on last update date.
        """
        categories_dict = self.search_by_date(start_date=start_date, end_date=end_date)
        return self._get_series_data(categories_dict.keys())

    def data_by_series(self,
                       series: str):
        """API EIASeries Query

        Args:
            series:

        Returns:

        """
        return self._get_series_data((series,))
