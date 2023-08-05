"""All Location methods are housed here"""
from tuneuptechnology.client import Client

class Locations(Client):
    """Location methods"""
    @classmethod
    def create_location(cls, data):
        """Create a location based on the data passed"""
        endpoint = f'{Client.API_BASE_URL}locations/create'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def retrieve_locations(cls, data):
        """Retrieve all locations"""
        endpoint = f'{Client.API_BASE_URL}locations'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def retrieve_location(cls, data):
        """Retrieve a single location"""
        endpoint = f'{Client.API_BASE_URL}locations/{data["id"]}'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def update_location(cls, data):
        """Update a location with the passed params"""
        endpoint = f'{Client.API_BASE_URL}locations/{data["id"]}/update'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def delete_location(cls, data):
        """Delete a location with the ID passed"""
        endpoint = f'{Client.API_BASE_URL}locations/{data["id"]}/delete'
        response = Client.response(data, endpoint)
        return response.json()
