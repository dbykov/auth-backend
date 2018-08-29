class AddressType:
    """
    Типы адресов
    """
    JUR = 1
    FACT = 2

    values = {
        JUR: 'Юридический',
        FACT: 'Фактический'
    }

    @classmethod
    def choices(cls):
        return list(cls.values.items())
