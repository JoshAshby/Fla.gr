#!/usr/bin/env python2

from whoosh.index import create_in
from whoosh.fields import *
import redis
import flagr.models.flagModel as fm
import os

r = redis.Redis(db=2)

schema = Schema(title=TEXT,
                id=ID(stored=True, unique=True),
                description=TEXT,
                labels=KEYWORD,
                url=TEXT,
                author=TEXT,
                time=TEXT,
                userID=TEXT)

if not os.path.exists(".searchIndex"):
        os.mkdir(".searchIndex")

ix = create_in(".searchIndex", schema)
writer = ix.writer()

for key in r.keys("flag:*:id"):
        flag = fm.flag(key.strip(":id"))
        labels = ""
        for label in flag["labels"]:
                labels += "%s ,"%label

        labels = labels.strip(", ")

        url = u""

        for field in flag.fields:
                name = field[0] if type(field) != str else field
                if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                        if name in ["url"]:
                                url = flag["url"]

        writer.add_document(title=flag["title"],
                        id=unicode(flag.id),
                        description=flag["description"],
                        labels=labels,
                        url=url,
                        author=flag["author"],
                        userID=unicode(flag["userID"]),
                        time=flag["time"])

writer.commit()
