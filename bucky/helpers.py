"""
Module contains helper functions
"""

def get_user(username,  db):
    """
        Usage: queries through and database and returns user
                object with passed username argument
        :return: User object or None if no such user
    """
    for user in db:
        if user.username.lower() == username.lower():
            return user
    return None

def get_bucket(title, db, current_user):
    """
        Usage: queries through and database and returns bucket
                object with passed title argument
        :return: Bucket object or None if no such Bucket
    """
    for bucket in db:
        if bucket.title.lower() == title.lower():
            return bucket
    return None
