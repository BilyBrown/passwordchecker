import requests
import hashlib
import sys

# the function that talks to the api and returns the goodies
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error Fetching: {res.status_code}, check the api and try again.")
    return res

# the function that iterates through the list of hashes and grabs the count for the password/hash we are interested in
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

# creating hashes and separating the hash so that we don't send our password over the internet
# get a response from the api and grab how many times it occurs via the get_password_leaks_count function
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

# primary function that ties it all together
def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times ...... You should '
            'probably change your password')
        else:
            print(f'{password} was not found, keep calm and carry on')
    return 'job\'s done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
