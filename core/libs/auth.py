import json

def verify_principal_header(principal_header):
    try:
        principal_data = json.loads(principal_header)
        user_id = principal_data.get('user_id')
        principal_id = principal_data.get('principal_id')
        # additional validation
        if user_id is None or principal_id is None:
            return False
        return True
    except json.JSONDecodeError:
        return False
