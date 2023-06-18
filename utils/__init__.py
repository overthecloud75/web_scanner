from .custom_logging import setup_logger

def check_server_info(headers, results):
    if 'Server' in headers and headers['Server']:
        results['server'] = headers['Server']
    return results 