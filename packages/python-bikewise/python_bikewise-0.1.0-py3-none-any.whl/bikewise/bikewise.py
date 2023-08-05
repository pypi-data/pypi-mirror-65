"""A simple BikeWise API wrapper."""

import json
import requests


def api_method(method):
    """Decorator for using method signatures for generating url endpoint."""
    def wrapper(self, *args, **kwargs):
        method(self, *args, **kwargs)
        api = self.api
        parameters = self.parameters
        endpoint = '&'.join(['{}={}'.format(key, value) for key, value in parameters.items() if value])
        if not endpoint:
            api_endpoint = api
        else:
            api_endpoint = '{}?{}'.format(api, endpoint)
        response = self.get(api_endpoint)

        return response

    return wrapper


def assert_incident_type(incident_type):
    """Function to evaluate correct parameter for keyword argument incident_type."""
    incidents = ('', 'crash', 'hazard', 'theft', 'unconfirmed',
                 'infrastructure_issue', 'chop_shop')
    if not isinstance(incident_type, str):
        raise TypeError("must pass string type to incident_type")
    if not incident_type.lower() in incidents:
        raise ValueError("allowed kwargs for incident_type: {}".format(
            tuple(kwarg for kwarg in incidents)
        ))
    return incident_type.lower()


class BaseAPI():
    """Base wraper for individual BikeWise requests."""
    base_url = 'https://bikewise.org:443/api/v2'

    def __init__(self):
        """BikeWise does not require an api key"""
        pass

    def get(self, endpoint):
        """Get request from specified url endpoint."""
        url = '{}/{}'.format(self.base_url, endpoint)
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError("bad request: {}\n"
                                  "requested URL: {}".format(response.status_code, url))
        response_json = json.loads(response.content)

        return response_json


class Incidents(BaseAPI):
    """API for detailed information about bike incidents."""
    api = 'incidents'

    @api_method
    def __call__(self, page=0, per_page=25):
        self.parameters = {
            'page': page,
            'per_page': per_page
        }

    @api_method
    def id(self, id):
        self.parameters = {
            'id': id}

    @api_method
    def features(self, page=0, per_page=25, occurred_before=0, occurred_after=0,
                 incident_type="", proximity="", proximity_area=0, query=""):
        incident_type = assert_incident_type(incident_type)
        self.parameters = {
            'page': page,
            'per_page': per_page,
            'occurred_before': occurred_before,
            'occurred_after': occurred_after,
            'incident_type': incident_type,
            'proximity': proximity,
            'proximity_area': proximity_area,
            'query': query
        }


class Locations(BaseAPI):
    """API for detailed information about bike incidents
    with a valid geojson."""
    api = 'locations'

    @api_method
    def __call__(self, limit=100, all=False):
        self.parameters = {
            'limit': limit,
            'all': all
        }

    @api_method
    def features(self, occurred_before=0, occurred_after=0, incident_type="", proximity="",
                 proximity_area=0, query="", limit=100, all=False):
        incident_type = assert_incident_type(incident_type)
        self.parameters = {
            'occurred_before': occurred_before,
            'occurred_after': occurred_after,
            'incident_type': incident_type,
            'proximity': proximity,
            'proximity_area': proximity_area,
            'query': query,
            'limit': limit,
            'all': all
        }

    @api_method
    def markers(self, occurred_before=0, occurred_after=0, incident_type="", proximity="",
                proximity_area=0, query="", limit=100, all=False):
        incident_type = assert_incident_type(incident_type)
        self.api = 'locations/markers'
        self.parameters = {
            'occurred_before': occurred_before,
            'occurred_after': occurred_after,
            'incident_type': incident_type,
            'proximity': proximity,
            'proximity_area': proximity_area,
            'query': query,
            'limit': limit,
            'all': all
        }


class BikeWise():
    """General class for the BikeWise API."""
    incidents = None
    locations = None

    def __init__(self):
        self.incidents = Incidents()
        self.locations = Locations()
