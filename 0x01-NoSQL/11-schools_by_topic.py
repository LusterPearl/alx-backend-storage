#!/usr/bin/env python3
""" 11-schools_by_topic """
from pymongo.collection import Collection


def schools_by_topic(mongo_collection: Collection, topic: str) -> list:
    """
    Return the list of schools having a specific topic.

    Args:
        mongo_collection: pymongo collection object.
        topic: Topic searched.

    Returns:
        List of schools having the specified topic.
    """
    schools = mongo_collection.find({"topics: topic"})
    return list(schools)