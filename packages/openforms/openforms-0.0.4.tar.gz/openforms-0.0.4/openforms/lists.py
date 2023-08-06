import requests

# UPDATE LIST
def update(listNo, values, apiKey):
    formatted_list = []
    if isinstance(values, list):
        for item in values:
            if not isinstance(item, str):
                formatted_list.append(str(item))
            else:
                formatted_list.append(str(item))
    elif isinstance(values, str):
        formatted_list.append(str(values))

    header = {'X-API-KEY': apiKey,
              'Content-Type': 'application/json'}

    update_list = requests.put('https://api.us.openforms.com/api/v4/lookup-lists/' + listNo,
                               data = formatted_list,
                               headers=header)

    if '200' in update_list.text:
        return 'List updated successfully'
    else:
        return 'List not updated: ' + update_list.text