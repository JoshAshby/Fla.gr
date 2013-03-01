#!/usr/bin/env python
"""
fla.gr user model

given a userID or a username or a email, return the users couchdb ORM

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from couchdb.mapping import Document, TextField, DateTimeField, BooleanField
from datetime import datetime

import config.dbBase as db

import bcrypt


def findUserByID(userID):
    """
    Searches couchdb for the requested user, by the userID and returns
    a userORM object if a user is found

    :param userID: The userID to search for
    :return: The `userORM` instance if a user is found,
        `None` if no user is found
    """
    users = userORM.view(db.couchServer, 'typeViews/user', key=userID)
    if not users:
        return None
    elif len(users)>1:
        raise Exception("Multiple Users")
    else:
        return users.rows[0]

def findUserByUsername(username):
    """
    Searches couchdb for documents that have the requested username

    :param username: The username to search for
    :return: The `userORM` instance if a user is found,
        `None` if no user is found
    """
    users = userORM.view(db.couchServer, 'typeViews/user')
    if not users:
        return None
    foundUser = []
    for user in users:
        if user.username == username:
            foundUser.append(user)
    if len(foundUser)>1:
        raise Exception("Multiple Users")
    else:
        return foundUser[0]
    pass


class userORM(Document):
    username = TextField()
    email = TextField()
    about = TextField()
    alerts = TextField(default="")
    disable = BooleanField(default=False)
    emailVisibility = BooleanField(default=False)
    history = TextField()
    level = TextField(default="normal")
    loggedIn = BooleanField(default=False)
    redirect = BooleanField(default=False)
    password = TextField()
    joined = DateTimeField(default=datetime.now)
    sessionID = TextField()
    docType=TextField(default="user")

    @classmethod
    def new(cls, username, password):
        """
        Make a new user, checking for username conflicts. If no conflicts are
        found the password is encrypted with bcrypt and the resulting `userORM` returned.

        :param username: The username that should be used for the new user
        :param password: The plain text password that should be used for the password.
        :return: `userORM` if the username is available,
        """
        if not findUserByUsername(username):
            passwd = bcrypt.hashpw(password, bcrypt.gensalt())
            user = cls(username=username, password=passwd)
            return user
        else:
            raise Exception("That username is taken, please choose again.")

    def clearAlerts(self):
        self.alerts = ""

    def pushAlert(self, alert):
        self.alerts += alert

    @classmethod
    def login(cls, user, password, cookieID):
        """
        Atempt to find and then log in a user, if their passwords match

        :param user: The userID or username of the user to log in
        :param password: The plain text password which the user supplies, to be checked against the found password
        :return: The `userORM` instance if a user if found and the passwords match
        """
        foundUser = findUserByID(user) or findUserByUsername(user)
        if foundUser:
            if not foundUser.disable:
                if foundUser.password == bcrypt.hashpw(password, foundUser.password):
                    db.redisSessionServer.hset(cookieID, "userID", foundUser.id)
                    user = cls.load(db.couchServer, foundUser.id)
                    user.sessionID = cookieID
                    return user
                else:
                    raise Exception("Your password appears to be wrong.")
            else:
                raise Exception("Your user is currently disabled. Please contact an admin for additional information.")
        raise Exception("We can't find your user, are you sure you have the correct information?")

    def logout(self):
        """
        Sets the users loggedIn to False then removes the link between their
        session and their `userORM`

        :return: Nothing
        """
        self.loggedIn = False
        db.redisSessionServer.hdel(self.sessionID, "userID")
