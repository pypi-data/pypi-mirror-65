#!/usr/bin/env python3

#    Kosmorro - Compute The Next Ephemerides
#    Copyright (C) 2019  Jérôme Deuchnord <jerome@deuchnord.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
from typing import Union

from skyfield import almanac
from skyfield.searchlib import find_discrete, find_maxima
from skyfield.timelib import Time
from skyfield.constants import tau

from .data import Object, Position, AsterEphemerides, MoonPhase, ASTERS, skyfield_to_moon_phase
from .core import get_skf_objects, get_timescale, get_iau2000b

RISEN_ANGLE = -0.8333


class EphemeridesComputer:
    def __init__(self, position: Union[Position, None]):
        if position is not None:
            position.observation_planet = get_skf_objects()['earth']
        self.position = position

    def get_sun(self, start_time, end_time) -> dict:
        times, is_risen = find_discrete(start_time,
                                        end_time,
                                        almanac.sunrise_sunset(get_skf_objects(), self.position))

        sunrise = times[0] if is_risen[0] else times[1]
        sunset = times[1] if not is_risen[1] else times[0]

        return {'rise': sunrise, 'set': sunset}

    @staticmethod
    def get_moon_phase(compute_date: datetime.date) -> MoonPhase:
        earth = get_skf_objects()['earth']
        moon = get_skf_objects()['moon']
        sun = get_skf_objects()['sun']

        def moon_phase_at(time: Time):
            time._nutation_angles = get_iau2000b(time)
            current_earth = earth.at(time)
            _, mlon, _ = current_earth.observe(moon).apparent().ecliptic_latlon('date')
            _, slon, _ = current_earth.observe(sun).apparent().ecliptic_latlon('date')
            return (((mlon.radians - slon.radians) // (tau / 8)) % 8).astype(int)

        moon_phase_at.rough_period = 7.0  # one lunar phase per week

        today = get_timescale().utc(compute_date.year, compute_date.month, compute_date.day)
        time1 = get_timescale().utc(compute_date.year, compute_date.month, compute_date.day - 10)
        time2 = get_timescale().utc(compute_date.year, compute_date.month, compute_date.day + 10)

        times, phase = find_discrete(time1, time2, moon_phase_at)

        return skyfield_to_moon_phase(times, phase, today)

    @staticmethod
    def get_asters_ephemerides_for_aster(aster, date: datetime.date, position: Position) -> Object:
        skyfield_aster = get_skf_objects()[aster.skyfield_name]

        def get_angle(time: Time) -> float:
            return position.get_planet_topos().at(time).observe(skyfield_aster).apparent().altaz()[0].degrees

        def is_risen(time: Time) -> bool:
            return get_angle(time) > RISEN_ANGLE

        get_angle.rough_period = 1.0
        is_risen.rough_period = 0.5

        start_time = get_timescale().utc(date.year, date.month, date.day)
        end_time = get_timescale().utc(date.year, date.month, date.day, 23, 59, 59)

        rise_times, arr = find_discrete(start_time, end_time, is_risen)
        try:
            culmination_time, _ = find_maxima(start_time, end_time, f=get_angle, epsilon=1./3600/24, num=12)
            culmination_time = culmination_time[0] if len(culmination_time) > 0 else None
        except ValueError:
            culmination_time = None

        if len(rise_times) == 2:
            rise_time = rise_times[0 if arr[0] else 1]
            set_time = rise_times[1 if not arr[1] else 0]
        else:
            rise_time = rise_times[0] if arr[0] else None
            set_time = rise_times[0] if not arr[0] else None

        # Convert the Time instances to Python datetime objects
        if rise_time is not None:
            rise_time = rise_time.utc_datetime().replace(microsecond=0)

        if culmination_time is not None:
            culmination_time = culmination_time.utc_datetime().replace(microsecond=0)

        if set_time is not None:
            set_time = set_time.utc_datetime().replace(microsecond=0) if set_time is not None else None

        aster.ephemerides = AsterEphemerides(rise_time, culmination_time, set_time)
        return aster

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return (year % 4 == 0 and year % 100 > 0) or (year % 400 == 0)

    def compute_ephemerides(self, compute_date: datetime.date) -> dict:
        return {'moon_phase': self.get_moon_phase(compute_date),
                'details': [self.get_asters_ephemerides_for_aster(aster, compute_date, self.position)
                            for aster in ASTERS] if self.position is not None else []}

    @staticmethod
    def get_seasons(year: int) -> dict:
        start_time = get_timescale().utc(year, 1, 1)
        end_time = get_timescale().utc(year, 12, 31)
        times, almanac_seasons = find_discrete(start_time, end_time, almanac.seasons(get_skf_objects()))

        seasons = {}
        for time, almanac_season in zip(times, almanac_seasons):
            if almanac_season == 0:
                season = 'MARCH'
            elif almanac_season == 1:
                season = 'JUNE'
            elif almanac_season == 2:
                season = 'SEPTEMBER'
            elif almanac_season == 3:
                season = 'DECEMBER'
            else:
                raise AssertionError

            seasons[season] = time.utc_iso()

        return seasons
