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
