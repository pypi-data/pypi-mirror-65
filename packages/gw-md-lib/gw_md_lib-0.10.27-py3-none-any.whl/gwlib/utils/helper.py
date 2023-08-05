from passlib.hash import pbkdf2_sha256


class Helper:

    @staticmethod
    def verify_crypt(password, compare_password):
        return pbkdf2_sha256.verify(password, compare_password)

    @staticmethod
    def set_crypt(password):
        return pbkdf2_sha256.hash(password)
