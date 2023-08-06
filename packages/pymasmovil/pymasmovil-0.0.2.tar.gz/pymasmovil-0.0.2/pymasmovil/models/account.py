from pymasmovil.client import Client


class Account():
    _route = '/v0/accounts'

    town = ""
    surname = ""
    stair = ""
    roadType = ""
    roadNumber = ""
    roadName = ""
    region = ""
    province = ""
    postalCode = ""
    phone = ""
    name = ""
    id = ""
    flat = ""
    email = ""
    door = ""
    donorCountry = ""
    documentType = ""
    documentNumber = ""
    corporateName = ""
    buildingPortal = ""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(Account, key):
                setattr(self, key, value)

    @classmethod
    def get(cls, session, account_id):
        """
        Returns a account instance obtained by id.

        :param id:
        :return: Account:
        """

        account_response = Client(session).get(
            route='{}/{}'.format(cls._route, account_id))

        return Account(**account_response)

    @classmethod
    def create(cls, session, **new_account):
        """
            Creates an account instance.

            :param **new_account:
            :return:
        """

        new_account_id = Client(session).post(cls._route, (), new_account)

        return Account(id=new_account_id, **new_account)
