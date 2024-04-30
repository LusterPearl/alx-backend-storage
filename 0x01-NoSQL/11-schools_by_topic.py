#!/usr/bin/env python3
""" 11-schools_by_topic """


def schools_by_topic(mongo_collection, topic):
    """
    Return the list of schools having a specific topic.

    Args:
        mongo_collection: pymongo collection object.
        topic: Topic searched.

    Returns:
        List of schools having the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))
