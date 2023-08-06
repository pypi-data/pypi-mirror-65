import requests
import json


# UPDATE LIST
def update(list_number, values, api_key):

    list_number = str(list_number)

    formatted_list = []
    if isinstance(values, list):
        for item in values:
            if not isinstance(item, str):
                formatted_list.append(str(item))
            else:
                formatted_list.append(str(item))
    elif isinstance(values, str):
        formatted_list.append(str(values))

    formatted_list = json.dumps(formatted_list)

    header = {'X-API-KEY': api_key,
              'Content-Type': 'application/json'}

    update_list = requests.put('https://api.us.openforms.com/api/v4/lookup-lists/' + list_number,
                               data=formatted_list,
                               headers=header)

    if '200' in update_list.text:
        return 'List updated successfully'
    else:
        return 'List not updated: ' + update_list.text
