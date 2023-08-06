import requests
import os
import time
import pandas as pd

# GET OF COLUMNS
def get_form_columns(formID, apiKey, versionNumber = None):

    # Set Variables
    of_headers = {'X-API-KEY': apiKey}
    form_sections = []
    form_fields = []
    columns = []

    # API Call
    if versionNumber == None:
        meta_call = requests.get('https://api.us.openforms.com/api/v4/forms/' + str(formID) + '?loadStructure=true', headers=of_headers)
    else:
        meta_call = requests.get('https://api.us.openforms.com/api/v4/forms/' + str(formID) + '?versionNumber=' + str(versionNumber) + '&loadStructure=true', headers=of_headers)
    meta_data = meta_call.json()

    # Format Column IDs, Names, and Types
    for item in meta_data['sections']:
        for field in item['fields']:
            # Fields that collect text data
            if field['type'] == 'Textbox' or field['type'] == 'Dropdown' or field['type'] == 'Radio' or field['type'] == 'Checkbox' or field['type'] == 'Email':
                form_fields.append({'id': field['elementId'],
                                    'name': str(item['name']) + "." + str(field['name']),
                                    'type': 'text'
                                    })
            # Fields that collect number data
            elif field['type'] == 'Numberbox' or field['type'] == 'Calculator' or field['type'] == 'Rank':
                form_fields.append({'id': field['elementId'],
                                    'name': str(item['name']) + "." + str(field['name']),
                                    'type': 'number'})
            # Fields that collect date/time data
            elif field['type'] == 'Date':
                form_fields.append({'id': field['elementId'],
                                    'name': str(item['name']) + "." + str(field['name']),
                                    'type': 'date'})
            # Fields that collect files
            elif field['type'] == 'Upload' or field['type'] == 'Signature':
                form_fields.append({'id': field['elementId'],
                                    'name': str(item['name']) + "." + str(field['name']),
                                    'type': 'url'})
            # Fields that collect geographic data
            elif field['type'] == 'Location':
                form_fields.append({'id': field['elementId'],
                                    'name': str(item['name']) + "." + str(field['name']),
                                    'type': 'point'})

    # Add columns for Response ID and Date
    form_fields.append({'id': 'id',
                        'name': 'Response ID',
                        'type': 'text'})

    form_fields.append({'id': 10000,
                        'name': 'Response Receipt',
                        'type': 'number'})

    form_fields.append({'id': 20000,
                        'name': 'Date Submitted',
                        'type': 'date'})

    # Sort Columns by ID for easier matching with Responses
    form_fields.sort(key=id)

    # Format Column Names for Socrata Import
    for item in form_fields:
        columns.append({'name': item['name'],
                        'dataTypeName': item['type']})

    return form_fields

def get_form_responses(formID, apiKey, versionNumber = None, startDate = None):

    # Set Variables
    of_headers = {'X-API-KEY': apiKey}
    form_sections = []
    form_dict = {}
    columns = []

    # API Call
    if versionNumber == None:
        meta_call = requests.get('https://api.us.openforms.com/api/v4/forms/' + str(formID) + '?loadStructure=true', headers=of_headers)
    else:
        meta_call = requests.get('https://api.us.openforms.com/api/v4/forms/' + str(formID) + '?versionNumber=' + str(versionNumber) + '&loadStructure=true', headers=of_headers)

    meta_data = meta_call.json()

    # Format Column IDs, Names, and Types
    for item in meta_data['sections']:
        for field in item['fields']:
            # Fields that collect text data
            if field['type'] == 'Textbox' or field['type'] == 'Dropdown' or field['type'] == 'Radio' or field['type'] == 'Checkbox' or field['type'] == 'Email':
                form_dict[field['elementId']] = field['name']
            # Fields that collect number data
            elif field['type'] == 'Numberbox' or field['type'] == 'Calculator' or field['type'] == 'Rank':
                form_dict[field['elementId']] = field['name']
            # Fields that collect date/time data
            elif field['type'] == 'Date':
                form_dict[field['elementId']] = field['name']
            # Fields that collect files
            elif field['type'] == 'Upload' or field['type'] == 'Signature':
                form_dict[field['elementId']] = field['name']
            # Fields that collect geographic data
            elif field['type'] == 'Location':
                form_dict[field['elementId']] = field['name']

    # Set Variables
    of_headers = {'X-API-KEY': apiKey}
    data = []

    # API Call
    if versionNumber == None and startDate == None:
        data_call = requests.get('https://api.us.openforms.com/api/v4/responses?formId=' + str(formID) + '&loadAnswers=true&pageSize=1000', headers=of_headers)
    elif versionNumber == None and startDate != None:
        data_call = requests.get('https://api.us.openforms.com/api/v4/responses?formId=' + str(formID) + '&pageSize=1000&loadAnswers=true' + '&toDateTime=' + startDate, headers=of_headers)
    elif versionNumber != None and startDate == None:
        data_call = requests.get('https://api.us.openforms.com/api/v4/responses?formId=' + str(formID) + '&versionNumber=' + str(versionNumber) + '&pageSize=1000&loadAnswers=true', headers=of_headers)

    responses = data_call.json()

    if responses['totalItems'] > 1000:
        addl_queries = responses['totalPages']
        page = 2
        while page <= addl_queries:
            if versionNumber == None and startDate == None:
                data_call = requests.get(
                    'https://api.us.openforms.com/api/v4/responses?formId=' + str(formID) + '&loadAnswers=true&pageSize=1000&page=' + str(page),
                    headers=of_headers)
            elif versionNumber == None and startDate != None:
                data_call = requests.get(
                    'https://api.us.openforms.com/api/v4/responses?formId=' + str(formID) + '&pageSize=1000&page=' + str(page) + '&loadAnswers=true' + '&toDateTime=' + startDate,
                    headers=of_headers)
            elif versionNumber != None and startDate == None:
                data_call = requests.get(
                    'https://api.us.openforms.com/api/v4/responses?formId=' + str(formID) + '&versionNumber=' + str(versionNumber) + '&pageSize=1000&page=' + str(page) + '&loadAnswers=true',
                    headers=of_headers)
            new_page = data_call.json()
            for item in new_page['items']:
                responses['items'].append(item)
            page += 1

    for item in responses['items']:
        indiv_responses = {}
        indiv_responses['id']  = item['id']
        indiv_responses[10000] = item['receiptNumber']
        indiv_responses[20000] = item['submitDateTime']
        if 'answers' in item.keys():
            for answer in item['answers']:
                if 'value' in answer:
                    indiv_responses[answer['elementId']] = answer['value']
                elif 'multiValues' in answer:
                    indiv_responses[answer['elementId']] = answer['multiValues']
        data.append(indiv_responses)

    return data

def get_form_list(apiKey):
    # Get List of Forms
    forms_list = []
    of_headers = {'X-API-KEY': apiKey}
    forms_api = requests.get('https://api.us.openforms.com/api/v4/forms?status=Latest', headers=of_headers)
    forms_api = forms_api.json()

    for item in forms_api['items']:
        form_details = {}
        form_details['id'] = item['id']
        form_details['version'] = item['versionNumber']
        form_details['name'] = item['name'] \
            .replace(":", "") \
            .replace("<", "") \
            .replace(">", "") \
            .replace("\"", "") \
            .replace("\\", "") \
            .replace("/", "") \
            .replace("|", "") \
            .replace("?", "") \
            .replace("*", "").strip()
        if len(form_details['name'].split('-')) > 1:
            form_details['dept'] = form_details['name'].split('-')[0].strip()
        else:
            form_details['dept'] = 'Missing Department Name'
        forms_list.append(form_details)

    return forms_list


def get_response_ids(forms, apiKey, start_date=None, end_date=None, limit=1000):

    of_headers = {'X-API-KEY': apiKey}
    response_ids = []

    if isinstance(forms, list):

        for form in forms:

            if start_date != None and end_date != None:
                response_api = requests.get(
                    'https://api.us.openforms.com/api/v4/responses?formId=' + str(form['id']) + \
                    '&pageSize=' + str(limit) + \
                    '&fromDateTime=' + start_date + \
                    '&toDateTime=' + end_date,
                    headers=of_headers)
            elif start_date != None and end_date == None:
                response_api = requests.get(
                    'https://api.us.openforms.com/api/v4/responses?formId=' + str(form['id']) + \
                    '&pageSize=' + str(limit) + \
                    '&fromDateTime=' + start_date,
                    headers=of_headers)
            elif start_date == None and end_date != None:
                response_api = requests.get(
                    'https://api.us.openforms.com/api/v4/responses?formId=' + str(form['id']) + \
                    '&pageSize=' + str(limit) + \
                    '&toDateTime=' + end_date,
                    headers=of_headers)
            else:
                response_api = requests.get(
                    'https://api.us.openforms.com/api/v4/responses?formId=' + str(form['id']) + \
                    '&pageSize=' + str(limit),
                    headers=of_headers)
            response_api = response_api.json()

            if response_api['totalItems'] > 1000:

                addl_queries = response_api['totalPages']
                page = 2

                while page <= addl_queries:
                    if start_date != None and end_date != None:
                        new_page = requests.get(
                            'https://api.us.openforms.com/api/v4/responses?formId=' + str(form['id']) + \
                            '&pageSize=' + str(limit) + \
                            '&page=' + str(page) + \
                            '&fromDateTime=' + start_date + \
                            '&toDateTime=' + end_date,
                            headers=of_headers)
                    elif start_date != None and end_date == None:
                        new_page = requests.get(
                            'https://api.us.openforms.com/api/v4/responses?formId=' + str(form['id']) + \
                            '&pageSize=' + str(limit) + \
                            '&page=' + str(page) + \
                            '&fromDateTime=' + start_date,
                            headers=of_headers)
                    elif start_date == None and end_date != None:
                        new_page = requests.get(
                            'https://api.us.openforms.com/api/v4/responses?formId=' + str(form['id']) + \
                            '&pageSize=' + str(limit) + \
                            '&page=' + str(page) + \
                            '&toDateTime=' + end_date,
                            headers=of_headers)
                    else:
                        new_page = requests.get(
                            'https://api.us.openforms.com/api/v4/responses?formId=' + str(form['id']) + \
                            '&page=' + str(page) + \
                            '&pageSize=' + str(limit),
                            headers=of_headers)
                    new_page = new_page.json()
                    for item in new_page['items']:
                        response_api['items'].append(item)
                    page += 1

            if response_api['totalItems'] > 0:
                for item in response_api['items']:
                    response_details = {}
                    response_details['form'] = form['name']
                    response_details['dept'] = form['dept']
                    response_details['id'] = item['id']
                    response_details['receiptNumber'] = item['receiptNumber']
                    response_ids.append(response_details)

            print(form['name'] + ' Export Completed')

    return response_ids

def get_form_attachments(responses, directory, apiKey):
    of_headers = {'X-API-KEY': apiKey}

    # Download and Save Attachments
    if isinstance(responses, list):
        for response in responses:
            if not os.path.exists(directory):
                os.makedirs(directory)
            files_api = requests.get(
                'https://api.us.openforms.com/api/v4/responses/' + str(response['id']) + '/download?type=Attachments',
                headers=of_headers)
            if files_api.status_code == 200:
                file = open(directory + '\\' + str(response['receiptNumber']) + '.zip', 'wb')
                file.write(files_api.content)
                file.close()
                response.update({'files': 'yes'})
                print('COMPLETED: ' + str(response['form']) + '/' + str(response['id']) + '(Receipt Number: ' + str(
                    response['receiptNumber']) + ')')
            elif files_api.status_code == 429:
                print('API LIMIT REACHED: ' + str(response) + ' INDEX: ' + str(responses.index(response)))
                responses = responses[responses.index(response):]
                time.sleep(60 * 62)
            else:
                response.update({'files': 'no'})
                print('NO FILES: ' + str(response))
        print('Attachments Export Complete')
    else:
        # Download and Save Attachments
        if not os.path.exists(directory):
            os.makedirs(directory)
        files_api = requests.get(
            'https://api.us.openforms.com/api/v4/responses/' + str(responses['id']) + '/download?type=Attachments',
            headers=of_headers)
        if files_api.status_code == 200:
            file = open(directory + '\\' + str(responses['receiptNumber']) + '.zip', 'wb')
            file.write(files_api.content)
            file.close()
            responses.update({'files': 'yes'})
            print('COMPLETED: ' + str(responses['form']) + '/' + str(responses['id']) + '(Receipt Number: ' + str(
                responses['receiptNumber']) + ')')
        elif files_api.status_code == 429:
            print('API LIMIT REACHED: ' + str(responses) + ' INDEX: ' + str(responses.index(responses)))
            responses = responses[responses.index(responses):]
            time.sleep(60 * 62)
        else:
            responses.update({'files': 'no'})
            print('NO FILES: ' + str(responses))
        print('Attachments Export Complete')

def delete_form_responses(responses, apiKey):
    # Delete Responses with Attachments
    of_headers = {'X-API-KEY': apiKey}
    deletions = []

    if type(responses) == 'list':
        for response in responses:
            # Make Sure Responses and Files Saved
            del_api = requests.delete(
                'https://api.us.openforms.com/api/v4/responses/' + str(response),
                headers=of_headers)
            if del_api.status_code == 204:
                print('DELETED: Response #' + str(response))
                deletions.append(response)
            elif del_api.status_code == 429:
                print('API LIMIT REACHED: Response #' + str(response) + ' INDEX: ' + str(responses.index(response)))
                time.sleep(60 * 62)
            else:
                print('ERROR: Response#' + str(response) + 'was not deleted \nDETAILS: ' + del_api.text)
                break

        else:
            del_api = requests.delete(
                'https://api.us.openforms.com/api/v4/responses/' + str(responses),
                headers=of_headers)
            if del_api.status_code == 204:
                print('DELETED: Response #' + str(responses))
                deletions.append(responses)
            elif del_api.status_code == 429:
                print('API LIMIT REACHED: Response #' + str(responses))
                time.sleep(60 * 62)
            else:
                print('ERROR: Response#' + str(response) + 'was not deleted \nDETAILS: ' + del_api.text)


def export_form_responses(forms, apiKey, directory, versionNumber=None):

    if isinstance(forms, list):

        for form in forms:

            print(form['name'] + ' Export Started')

            # Create Directory for Given Form
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Get and Save Responses as CSV
            r = get_form_responses(form['id'], apiKey)
            c = get_form_columns(form['id'], apiKey)
            columns = {}

            for line in c:
                columns[line['id']] = line['name']

            responses         = pd.DataFrame(r)
            responses.columns = responses.columns.map(columns)

            responses.to_csv(directory + '\\Responses - ' + str(form['name']) + '.csv', index=False)

    else:
        raise Exception('List class with keys \'id\' and \'name\' for each form required')