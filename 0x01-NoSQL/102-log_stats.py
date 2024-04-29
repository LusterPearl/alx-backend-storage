#!/usr/bin/env python3
"""
Log stats - new version
"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    """Number of logs"""
    num_logs = logs_collection.count_documents({})

    """Methods"""
    methods = {}
    for log in logs_collection.find({}, {"method": 1}):
        method = log.get("method", "UNKNOWN")
        methods[method] = methods.get(method, 0) + 1

    """IPs"""
    ips = {}
    for log in logs_collection.find({}, {"ip": 1}):
        ip = log.get("ip", "UNKNOWN")
        ips[ip] = ips.get(ip, 0) + 1

    """Sort IPs by count"""
    sorted_ips = {k: v for k, v in sorted(ips.items(), key=lambda item: item[1], reverse=True)}

    """Output"""
    print(f"{num_logs} logs")
    print("Methods:")
    for method, count in methods.items():
        print(f"\tmethod {method}: {count}")
    print("IPs:")
    for idx, (ip, count) in enumerate(sorted_ips.items()):
        if idx >= 10:
            break
    print(f"\t{ip}: {count}")