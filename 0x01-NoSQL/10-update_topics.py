#!/usr/bin/env python3
""" 10-update_topics """


def update_topics(mongo_collection, name, topics):
    """
    Change all topics of a school document based on the name.

    Args:
        mongo_collection: pymongo collection object.
        name: School name to update.
        topics: List of topics approached in the school.
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
