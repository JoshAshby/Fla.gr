#!/usr/bin/env python2

from whoosh.index import create_in
from whoosh.fields import *
import redis
import flagr.models.flagModel as fm
import os

r = redis.Redis(db=2)

schema = Schema(title=TEXT(stored=True),
                id=ID(stored=True, unique=True),
                description=TEXT,
                labels=KEYWORD(stored=True),
                url=TEXT(stored=True),
                author=TEXT(stored=True),
                time=TEXT,
                userID=TEXT)

if not os.path.exists("index"):
        os.mkdir("index")

ix = create_in("index", schema)
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


from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser

ix = open_dir("index")
flags = []

with ix.searcher() as searcher:
        query = MultifieldParser(["title", "description", "labels", "url", "author"], ix.schema).parse(u"Josh*")
        results = searcher.search(query)

        for result in results:
                flags.append(result["id"])

print flags
