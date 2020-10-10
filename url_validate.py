import requests
import base64


# check url via regex and then try to ping it
def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if url is not None and regex.search(url):
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except Exception as err:
            print("Host is unreachable: " + str(err))
            return False

        return True
    else:
        return False


# Encode url into base64
def base64_encoded_url(url):
    message_bytes = url.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_msg_str = base64_bytes.decode('ascii')
    return base64_msg_str