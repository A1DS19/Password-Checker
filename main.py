import requests
import argparse
import hashlib


class PasswordChecker:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.default_url = "https://api.pwnedpasswords.com/range/"
        self.hashed_password = ""
        self.count = 0

    def get_password(self):
        self.parser.add_argument("-p", "--password", help="Your password")
        arg = self.parser.parse_args()
        self.hashed_password = hashlib.sha1(str(arg.password).encode("utf-8")).hexdigest().upper()

    def get_password_response(self):
        first_5_chars, tail = self.hashed_password[:5], self.hashed_password[5:]

        res = requests.get(self.default_url + first_5_chars)
        if res.status_code != 200:
            raise RuntimeError(f"Error fetching: {res.status_code}")

        self.get_password_leaks_count(res, tail)

    def get_password_leaks_count(self, hashes, hash_to_check):
        hashes = (line.split(":") for line in hashes.text.splitlines())
        for hash, count in hashes:
            if hash == hash_to_check:
                self.count += count

            else:
                self.count = 0

    def final_response(self):
        pass

    def run(self):
        self.get_password()
        self.get_password_response()


check = PasswordChecker()
check.run()
