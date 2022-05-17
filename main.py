# API for receiving organisations from Cordra instance with ROR
import requests
from itertools import islice
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Union


# Cordra endpoint
cordra_endpoint = 'https://nsidr.org//objects/'


def request_organisation_data() -> dict:
    """ Function for requesting organisations data from Cordra instance
        Saves organisations names and ROR ids in new dictionary
        :return: Returns organisations data as organisations_data
    """

    # Creating query for receiving all organisation information,
    # String building because of double quotes messing with requests url
    query = '?query=type:\"Organisation\"'
    response = requests.get(cordra_endpoint + query).json()

    organisations_list: list = []
    organisations_data: dict = {}

    # For each organisation, append data
    for value in islice(response.values(), 3, 4):
        for organisation in value:
            organisation_content = organisation['content']
            organisations_list.append(organisation_content['organisation_name'])

            if organisation_content['externalIdentifiers'].get('ROR'):
                organisations_data[organisation_content['organisation_name']] = {
                    'ROR_id': organisation_content['externalIdentifiers']['ROR']['identifier'],
                    'ROR_url': organisation_content['externalIdentifiers']['ROR']['url']
                }
            else:
                organisations_data[organisation_content['organisation_name']] = {
                    'ROR_id': None,
                    'ROR_url': None
                }

    # organisations_data['organisations_list'] = organisations_list

    return organisations_data


# Create endpoint for requesting the organisations data
api = Flask(__name__)
CORS(api)


@api.route('/get_organisations', methods=['GET'])
def get_organisations() -> Union[object, bool]:
    """ Function that calls for Cordra organisations
        Call on request_organisations_data function
        :return: Returns organisations data as json or False on no GET
    """

    # Check if request is GET
    if request.method == 'GET':
        # Receive organisations data
        organisations_data = request_organisation_data()

        # Return organisations data to client
        return jsonify(organisations_data)
    else:
        return False


if __name__ == '__main__':
    api.run()
