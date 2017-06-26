
class User():
    """
    A User class used to create instances for the application users
    Attributes:
                username = string for the user's username
                password = string that stores the user's password
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password


class BucketList():
    """
    A BucketList class used to create instances of bucketlist(s)
    Attributes:
                title = string for the bucketlist title
                description = string for the bucketlist description
                owner = string for the owner's(user who creates the bucketlist) username
    """

    def __init__(self, title, description, owner):
        self.title = title
        self.description = description
        self.owner = owner


class BucketListItem():
    """
    A BucketList class used to create instances of bucketlist(s)
    Attributes:
                name = string for the bucketlist item name
                bucket = string for the bucketlist title that the item belongs to
                achieved = boolean for marking an item as achieved in the bucketlist
    """

    def __init__(self, name, bucket, achieved=False):
        self.name = name
        self.bucket = bucket
        self.achieved = achieved
