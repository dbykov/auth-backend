class Gender:
    """
    Пол
    """
    MALE = 1
    FEMALE = 2

    values = {
        MALE: 'Мужской',
        FEMALE: 'Женский',
    }

    @classmethod
    def choices(cls):
        return list(cls.values.items())
