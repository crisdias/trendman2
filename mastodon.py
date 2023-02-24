import requests
# import json


def get_all_data(url, limit):
    offset = 0

    # grabs first page only, too much info these days
    response = requests.get(url, params={'limit': limit, 'offset': offset})
    return response.json()
    

    data = []
    while True:
        # Call the API with the current offset and limit
        response = requests.get(url, params={'limit': limit, 'offset': offset})
        response_data = response.json()

        # If there are no more records, break out of the loop
        if len(response_data) == 0:
            break

        # Append the data to the data variable
        data.extend(response_data)

        # Update the offset for the next API call
        offset += limit
    return data