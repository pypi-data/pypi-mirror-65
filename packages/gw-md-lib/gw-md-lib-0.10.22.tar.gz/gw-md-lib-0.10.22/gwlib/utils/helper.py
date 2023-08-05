from passlib.hash import bcrypt


class Helper():

    @staticmethod
    def verify_crypt(password, compare_password):
        print("disque la valido", password, compare_password)
        try:
            result = bcrypt.verify(password, compare_password)
            print("disque la valido", result)
        except Exception as e:
            print("ERRROR CRYPT", e)
        return bcrypt.verify(password, compare_password)

    @staticmethod
    def set_crypt(password):
        return bcrypt.encrypt(password)
