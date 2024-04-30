#!/usr/bin/env python3
"""
Script that provides stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient
from collections import Counter

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    total_logs = collection.count_documents({})
    print("{} logs".format(total_logs))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("    method {}: {}".format(method, count))
        
    query = {"method": "GET", "path": "/status"}
    status_check = collection.count_documents(query)
    print("{} status check".format(status_check))

    # Top 10 IPs
    ips = collection.distinct("ip")
    ip_counts = Counter(ips)
    top_ips = ip_counts.most_common(10)
    print("IPs:")
    for ip, count in top_ips:
        print("    {}: {}".format(ip, count))