#!/usr/bin/env python3
""" 12-log_stats """
from pymongo import MongoClient

def log_stats():
    """
    Provide stats about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    """Total number of logs"""
    total_logs = logs_collection.count_documents({})

    """Number of logs for each method"""
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: logs_collection.count_documents({"method": method}) for method in methods}

    """Number of logs for method GET and path /status"""
    status_check_count = logs_collection.count_documents({"method": "GET", "path": "/status"})

    print("{} logs".format(total_logs))
    print("Methods:")
    for method, count in method_counts.items():
        print("    method {}: {}".format(method, count))
    print("{} status check".format(status_check_count))