"""Unit testing for bikewise module in ../bikewise."""

from bikewise import BikeWise
import os
from pathlib import Path
import sys
import unittest
os.chdir(Path(__file__).parent)
os.chdir('../bikewise')
sys.path.append(os.getcwd())  # required for relative file fetching - run in 'test' directory


class TestBikeWise(unittest.TestCase):
    # page
    page = (1, 2, 55, 5)
    page_test = (-1, 4.2)

    # per_page
    per_page = (1, 23, 44)
    per_page_test = (0, -2, 4.5)

    # occurred_before
    occurred_before = (1480444800, 1480444800.0, '1480444800')
    occurred_before_test = ('2020-03-31', 'noon')

    # occurred_after
    occurred_after = (1440444800, 1440444800.0, '1440444800')
    occurred_after_test = ('2020-04-01', 'afternoon')

    # incident_type
    default_incidents = ('', 'crash', 'hazard', 'theft', 'unconfirmed',
                         'infrastructure_issue', 'chop_shop')
    correct_incidents = ('', 'CRASH', 'HazARd', 'CHOP_shOP')
    incorrect_incidents = ('x', 3, -4.9, True, None, 'hazardd', 'thefts')

    # proximity
    proximity = ('70.210.133.87', '210 NW 11th Ave, Portland, OR', '60647',
                 'Chicago, IL', '45.521728, -122.67326')
    proximity_test = ('1311 Curtis St, Berkeley, CA', 94536, '94702', 'San Francisco, CA')

    # proximity_area
    proximity_area = (1, 5, 10, 55)
    proximity_area_test = (0, -3, 3.3)

    # query
    query = ('Trek',)
    query_test = (3.4,)

    # limit
    limit = (1, 100, 250)
    limit_test = (0, -1)

    # all
    all = (False, 0, 'false', None)  # True and 1 work, but they overload the request.
    all_test = ('xx',)

    def setUp(self):
        # comment out if you want to view instance influence on methods
        self.bikewise = BikeWise()

    def test_id(self):
        incidents = self.bikewise.incidents.id(113424)
        self.assertIsInstance(incidents, dict)

    def test_page(self):
        for _page in self.page:
            incidents = self.bikewise.incidents(page=_page, per_page=self.per_page[0])
            self.assertIsInstance(incidents, dict)
            incidents = self.bikewise.incidents.features(page=_page, per_page=self.per_page[0])
            self.assertIsInstance(incidents, dict)
        for t_page in self.page_test:
            incidents = self.bikewise.incidents(page=t_page, per_page=self.per_page[0])
            self.assertIsInstance(incidents, dict)
            incidents = self.bikewise.incidents.features(page=t_page, per_page=self.per_page[0])
            self.assertIsInstance(incidents, dict)

    def test_per_page(self):
        for _per_page in self.per_page:
            incidents = self.bikewise.incidents(page=self.page[0], per_page=_per_page)
            self.assertIsInstance(incidents, dict)
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=_per_page)
            self.assertIsInstance(incidents, dict)
        for _per_page_t in self.per_page_test:
            incidents = self.bikewise.incidents(page=self.page[0], per_page=_per_page_t)
            self.assertIsInstance(incidents, dict)
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=_per_page_t)
            self.assertIsInstance(incidents, dict)

    def test_occurred_before(self):
        for _occur_b in self.occurred_before:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         occurred_before=_occur_b)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_before=_occur_b)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_before=_occur_b)
            self.assertIsInstance(locations, dict)
        for _occur_b_t in self.occurred_before_test:
            with self.assertRaises(ConnectionError):
                self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                 occurred_before=_occur_b_t)
                self.bikewise.locations.features(occurred_before=_occur_b_t)
                self.bikewise.locations.markers(occurred_before=_occur_b_t)

    def test_occurred_after(self):
        for _occur_a in self.occurred_after:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         occurred_after=_occur_a)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=_occur_a)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=_occur_a)
            self.assertIsInstance(locations, dict)
        for _occur_a_t in self.occurred_after_test:
            with self.assertRaises(ConnectionError):
                self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                 occurred_after=_occur_a_t)
                self.bikewise.locations.features(occurred_after=_occur_a_t)
                self.bikewise.locations.markers(occurred_after=_occur_a_t)

    def test_incident_type(self):
        for _incident_d in self.default_incidents:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         incident_type=_incident_d)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type=_incident_d)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type=_incident_d)
            self.assertIsInstance(locations, dict)
        for _incident_c in self.correct_incidents:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         incident_type=_incident_c)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type=_incident_c)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type=_incident_c)
            self.assertIsInstance(locations, dict)
        for _incident_i in self.incorrect_incidents:
            with self.assertRaises(Exception):
                self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                 incident_type=_incident_i)
                self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                 incident_type=_incident_i)
                self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                incident_type=_incident_i)

    def test_proximity(self):
        for _proximity_c in self.proximity:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         incident_type='theft', proximity=_proximity_c)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type='theft', proximity=_proximity_c)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type='theft', proximity=_proximity_c)
            self.assertIsInstance(locations, dict)
        for _proximity_t in self.proximity_test:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         incident_type='theft', proximity=_proximity_t)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type='theft', proximity=_proximity_t)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type='theft', proximity=_proximity_t)
            self.assertIsInstance(locations, dict)

    def test_proximity_area(self):
        for _proximity_area_c in self.proximity_area:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         incident_type='theft', proximity=self.proximity[0],
                                                         proximity_area=_proximity_area_c)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type='theft', proximity_area=_proximity_area_c)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type='theft', proximity_area=_proximity_area_c)
            self.assertIsInstance(locations, dict)
        for _proximity_area_t in self.proximity_area_test:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         incident_type='theft', proximity=self.proximity[0],
                                                         proximity_area=_proximity_area_t)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type='theft', proximity_area=_proximity_area_t)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type='theft', proximity=_proximity_area_t)
            self.assertIsInstance(locations, dict)

    def test_query(self):
        for _query in self.query:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         incident_type='theft', proximity=self.proximity[0],
                                                         query=_query)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type='theft', query=_query)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type='theft', query=_query)
            self.assertIsInstance(locations, dict)
        for _query_t in self.query_test:
            incidents = self.bikewise.incidents.features(page=self.page[0], per_page=self.page[0],
                                                         incident_type='theft', proximity=self.proximity[0],
                                                         query=_query_t)
            self.assertIsInstance(incidents, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type='theft', query=_query_t)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type='theft', query=_query_t)
            self.assertIsInstance(locations, dict)

    def test_limit(self):
        for _limit in self.limit:
            locations = self.bikewise.locations(limit=_limit)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type='theft', limit=_limit)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type='theft', limit=_limit)
            self.assertIsInstance(locations, dict)
        for _limit_t in self.limit_test:
            if _limit_t < 0:
                with self.assertRaises(ConnectionError):
                    self.bikewise.locations(limit=_limit_t)
            else:
                locations = self.bikewise.locations(limit=_limit_t)
                self.assertIsInstance(locations, dict)
                locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                             incident_type='theft', limit=_limit_t)
                self.assertIsInstance(locations, dict)
                locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                            incident_type='theft', limit=_limit_t)
                self.assertIsInstance(locations, dict)

    def test_all(self):
        for _all in self.all:
            locations = self.bikewise.locations(all=_all)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.features(occurred_after=self.occurred_after[0],
                                                         incident_type='theft', all=_all)
            self.assertIsInstance(locations, dict)
            locations = self.bikewise.locations.markers(occurred_after=self.occurred_after[0],
                                                        incident_type='theft', all=_all)
            self.assertIsInstance(locations, dict)
        for _all_t in self.all_test:
            with self.assertRaises(ConnectionError):
                self.bikewise.locations(all=_all_t)


if __name__ == '__main__':
    unittest.main()
