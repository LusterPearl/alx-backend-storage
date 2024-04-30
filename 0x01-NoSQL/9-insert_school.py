#!/usr/bin/env python3
""" 9-insert_school.py """
from pymongo.collection import Collection


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in the collection based on kwargs.
    Args:
        mongo_collections: pymongo collection object
        **kwargs: Keyword arguments for the new document

    Returns:
        The new _id of the inserted document
    """
    return mongo_collection.insert_one(kwargs).inserted_id
