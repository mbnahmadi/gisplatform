from copy import deepcopy

SENSITIVE_FIELDS = {
    'password',
    'confirm_password',
    'old_password', 'new_password', 'otp', 'otp_code'
}

def senetize_data(data):
    """
    Remove sensitive fields from user data before logging.
    """
    if not isinstance(data, dict):
        return data

    cleaned = deepcopy(data)
    for key in cleaned.keys():
        if key in SENSITIVE_FIELDS:
            value = cleaned.get(key)
            