import random, string

def generate_token(length=10):
    sequence = string.ascii_letters + string.digits
    token = ''
    for _ in range(length):
        token += random.choice(sequence)
    return token