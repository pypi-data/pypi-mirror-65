import unittest
from kosmorrolib.ephemerides import EphemeridesComputer
from kosmorrolib.core import get_skf_objects
from kosmorrolib.data import Star, Position, MoonPhase
from datetime import date


class EphemeridesComputerTestCase(unittest.TestCase):
    def test_get_ephemerides_for_aster_returns_correct_hours(self):
        position = Position(0, 0)
        position.observation_planet = get_skf_objects()['earth']
        star = EphemeridesComputer.get_asters_ephemerides_for_aster(Star('Sun', skyfield_name='sun'),
                                                                    date=date(2019, 11, 18),
                                                                    position=position)

        self.assertRegex(star.ephemerides.rise_time.isoformat(), '^2019-11-18T05:41:')
        self.assertRegex(star.ephemerides.culmination_time.isoformat(), '^2019-11-18T11:45:')
        self.assertRegex(star.ephemerides.set_time.isoformat(), '^2019-11-18T17:48:')

    ###################################################################################################################
    ###                                             MOON PHASE TESTS                                                ###
    ###################################################################################################################

    def test_moon_phase_new_moon(self):
        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 25))
        self.assertEqual('WANING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 26))
        self.assertEqual('NEW_MOON', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-12-04T')

        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 27))
        self.assertEqual('WAXING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-12-04T')

    def test_moon_phase_first_crescent(self):
        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 3))
        self.assertEqual('WAXING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-04T')

        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 4))
        self.assertEqual('FIRST_QUARTER', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 5))
        self.assertEqual('WAXING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

    def test_moon_phase_full_moon(self):
        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 11))
        self.assertEqual('WAXING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 12))
        self.assertEqual('FULL_MOON', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 13))
        self.assertEqual('WANING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

    def test_moon_phase_last_quarter(self):
        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 18))
        self.assertEqual('WANING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 19))
        self.assertEqual('LAST_QUARTER', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

        phase = EphemeridesComputer.get_moon_phase(date(2019, 11, 20))
        self.assertEqual('WANING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

    def test_moon_phase_prediction(self):
        phase = MoonPhase('NEW_MOON', None, None)
        self.assertEqual('First Quarter', phase.get_next_phase())
        phase = MoonPhase('WAXING_CRESCENT', None, None)
        self.assertEqual('First Quarter', phase.get_next_phase())

        phase = MoonPhase('FIRST_QUARTER', None, None)
        self.assertEqual('Full Moon', phase.get_next_phase())
        phase = MoonPhase('WAXING_GIBBOUS', None, None)
        self.assertEqual('Full Moon', phase.get_next_phase())

        phase = MoonPhase('FULL_MOON', None, None)
        self.assertEqual('Last Quarter', phase.get_next_phase())
        phase = MoonPhase('WANING_GIBBOUS', None, None)
        self.assertEqual('Last Quarter', phase.get_next_phase())

        phase = MoonPhase('LAST_QUARTER', None, None)
        self.assertEqual('New Moon', phase.get_next_phase())
        phase = MoonPhase('WANING_CRESCENT', None, None)
        self.assertEqual('New Moon', phase.get_next_phase())


if __name__ == '__main__':
    unittest.main()
