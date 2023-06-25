from urllib.parse import urlparse, parse_qs

from .custom_logging import setup_logger

def check_server_info(headers, results):
    if 'Server' in headers and headers['Server']:
        results['server'] = headers['Server']
    return results 

def filter_url(url):
    parsed_url = urlparse(url)
    query = {}
    if parsed_url.query:
        query_params = parse_qs(parsed_url.query)
        for key, value in query_params.items():
            query[key] = value
    return parsed_url.path, query, parsed_url.fragment

def check_query_in_page(page, url, results):
    query_exists = False
    parsed_url = urlparse(url)
    query = results[parsed_url.path]['query']
    if query:
        for key in query:
            # key 값이 없는 경우 제외 
            if key:
                for value in query[key]:
                    if value in page:
                        query_exists = True
    results[parsed_url.path]['query_exists'] = query_exists
