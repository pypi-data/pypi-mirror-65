from passlib.hash import bcrypt


class Helper():

    @staticmethod
    def verify_crypt(password, compare_password):
        return bcrypt.verify(password, compare_password)

    @staticmethod
    def set_crypt(password):
        return bcrypt.encrypt(password)
