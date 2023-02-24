import requests

def get_all_data(url, items_per_page=20, max_items=None):
    offset = 0
    data = []
    
    while True:
        # Call the API with the current offset and limit
        response = requests.get(url, params={'limit': items_per_page, 'offset': offset})
        response_data = response.json()

        # If there are no more records, break out of the loop
        if len(response_data) == 0:
            break

        # Append the data to the data variable
        data.extend(response_data)

        # If the maximum number of items has been reached, break out of the loop
        if max_items is not None and len(data) >= max_items:
            break

        # Update the offset for the next API call
        offset += items_per_page

    # Trim the data array to match the maximum number of items requested
    if max_items is not None and len(data) > max_items:
        data = data[:max_items]

    return data
