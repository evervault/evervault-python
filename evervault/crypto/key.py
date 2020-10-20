import re


class Key(object):
    def __init__(self, key):
        self.key = self.__format(key)

    def __format(self, key):
        key_header = "-----BEGIN PUBLIC KEY-----\n"
        key_footer = "-----END PUBLIC KEY-----"
        if key_header in key and key_footer in key:
            return key
        return key_header + "\n".join(re.findall(r".{0,64}", key)) + key_footer
