#!/usr/bin/env python3
"""
Module for top students.
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    """
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {"_id": "$_id", "name": {"$first": "$name"}, "averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ]
    return list(mongo_collection.aggregate(pipeline))
