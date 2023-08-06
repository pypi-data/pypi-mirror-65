# ##############################################################################
#  EnerPy (_types.py)
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

import pandas as pd

import enerpy


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


class EIASeries(UserDict):
    id: str

    def __init__(self, name, units, frequency, id):
        freq = Frequency.from_code(frequency)
        super().__init__(name=name, units=units, frequency=freq, id=id)

    # region Properties
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

    @property
    def msn(self):
        if self.id.startswith('SEDS.'):
            return self.id[5:10]
        else:
            raise enerpy.SeriesTypeError(f'"{self.id}" is not a SEDS series')

    # endregion

    @classmethod
    def from_series_json(cls, ser_json):
        """Converts data returned from EIA series endpoint to instances of EIASeries

        Args:
            ser_json:

        Returns:

        """
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

    @staticmethod
    def _parse_date(date: str):
        if date.find('Q') == 4:
            return datetime(int(date[:4]), int(date[5]) * 3, 1), Frequency.QUARTERLY
        fmt, freq = DATE_FORMATS[len(date)]
        return datetime.strptime(date, fmt), freq
