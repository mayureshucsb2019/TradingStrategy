import base64

def make_encoded_header(username, password):
    """Encodes the authorization header."""
    auth_str = f"{username}:{password}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    return {
        "accept": "application/json",
        "authorization": f"Basic {encoded_auth}"
    }

def pretty_print(data):
    """
    Prints data in a structured format:
    - If data is a dictionary, prints key-value pairs.
    - If data is a list, tuple, or set, prints each element.
    - If elements in a list, tuple, or set are dictionaries, prints key-value pairs for each.
    
    Args:
        data: Dictionary, list, tuple, or set containing elements to print.
    """
    print("##############")
    
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
    elif isinstance(data, (list, tuple, set)):
        for item in data:
            if isinstance(item, dict):
                print("{ ")
                for key, value in item.items():
                    print(f"  {key}: {value}")
                print("}")
            else:
                print(item)
    else:
        print(data)
    
    print("##############\n")