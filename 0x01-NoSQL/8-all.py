#!/usr/bin/env python3
""" 8-all """
from pymongo.collection import Collection


def list_all(mongo_collection):
    """
    List all documents in a collection

    Args:
    mongo_collection: pymongo collection object.


    Returns:
    List of documents in the collection.
    """
    return list(mongo_collection.find())
