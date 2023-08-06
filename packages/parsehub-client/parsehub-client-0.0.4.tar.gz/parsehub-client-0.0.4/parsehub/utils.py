from csv import DictReader

def _parse_response_data(response, format):

    if format not in ['csv', 'json']:
        raise ValueError('Format must be one of: csv, json')
    
    if format == 'json':
        return response.json()
    else:
        data = DictReader(response.text.splitlines())
        return list(data)