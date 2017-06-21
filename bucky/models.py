from flask-login import UserMixin

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    @property
    def id(self):
        return self.username


class BucketList():
    def __init__(self, title, description, owner):
        self.title = title
        self.description = description
        self.owner = owner


class BucketListItem():
    def __init__(self, name, bucket, achieved=False):
        self.name = name
        self.bucket = bucket
        self.achieved = achieved