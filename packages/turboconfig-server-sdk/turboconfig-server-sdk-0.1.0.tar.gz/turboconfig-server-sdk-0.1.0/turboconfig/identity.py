class TurboConfigIdentity:
    def __init__(
        self, user_id, name=None, email=None, phone_number=None, attributes={}
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.attributes = attributes

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        self.__user_id = str(value)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value if isinstance(value, str) else None

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value if isinstance(value, str) else None

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value if isinstance(value, str) else None

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, value):
        self.__attributes = value if isinstance(value, dict) else {}

    def set_attribute(self, key, value):
        self.__attributes[key] = value

    def __eq__(self, other):
        return (
            self.user_id == other.user_id
            and self.name == other.name
            and self.email == other.email
            and self.phone_number == other.phone_number
            and self.attributes == other.attributes
        )

    def get_request_json(self):
        req_json = {"user": {}}
        if self.name:
            req_json["name"] = self.name

        if self.email:
            req_json["email"] = self.email

        if self.phone_number:
            req_json["phoneNumber"] = self.phone_number

        if self.attributes:
            req_json["metadata"] = self.attributes

        return req_json
