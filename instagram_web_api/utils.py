from datetime import datetime
def generate_csrf_token():
    import string,random
    chars = string.digits+string.ascii_lowercase+string.ascii_uppercase
    csrf_token = ''.join(random.choice(chars) for _ in range(32))
    return csrf_token
def get_id() :
    return int(datetime.now().timestamp())