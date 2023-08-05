"""All Customer methods are housed here"""
from tuneuptechnology.client import Client

class Customers(Client):
    """Customer methods"""
    @classmethod
    def create_customer(cls, data):
        """Create a customer based on the data passed"""
        endpoint = f'{Client.API_BASE_URL}customers/create'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def retrieve_customers(cls, data):
        """Retrieve all customers"""
        endpoint = f'{Client.API_BASE_URL}customers'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def retrieve_customer(cls, data):
        """Retrieve a single customer"""
        endpoint = f'{Client.API_BASE_URL}customers/{data["id"]}'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def update_customer(cls, data):
        """Update a customer with the passed params"""
        endpoint = f'{Client.API_BASE_URL}customers/{data["id"]}/update'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def delete_customer(cls, data):
        """Delete a customer with the ID passed"""
        endpoint = f'{Client.API_BASE_URL}customers/{data["id"]}/delete'
        response = Client.response(data, endpoint)
        return response.json()
