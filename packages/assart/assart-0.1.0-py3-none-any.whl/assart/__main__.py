#!/usr/bin/env python3
import argparse
import boto3
import os


def gen_report(rec_list, unit):
    for rec in rec_list:
        print("Bucket Name:", rec['bucket_name'])
        print("\tCreation Date:", rec['creation_date'])
        print("\tNumber of Files:", rec['num_files'])
        total = "\tTotal Size:"
        if unit == 'KB':
            print(total, (rec['total_size'] / 1024), unit)
        elif unit == 'MB':
            print(total, (rec['total_size'] / 1024 / 1024), unit)
        elif unit == 'GB':
            print(total, (rec['total_size'] / 1024 / 1024 / 1024), unit)
        else:
            print(total, rec['total_size'], "bytes")
        print("\tLast Modified Date:", rec['last_modified_date'])
        print("")


def main():
    parser = argparse.ArgumentParser(description='A simple S3 analytics reporting tool')
    parser.add_argument('-u', '--unit', required=False, type=str,
                        choices=['KB', 'MB', 'GB'], help='Unit of Size')
    args = parser.parse_args()
    s3 = boto3.resource('s3')
    buckets = list(s3.buckets.all())
    records = []
    for bucket in buckets:
        record = {}
        record['bucket_name'] = bucket.name
        record['creation_date'] = str(bucket.creation_date)
        num_files = 0
        total_size = 0
        # inefficient for buckets with many items consider refactor
        last_mod_list = []
        bucket_objs = s3.Bucket(bucket.name)
        for objs in bucket_objs.objects.all():
            # check size to differtiate between folders and files
            if objs.size > 0:
                num_files += 1
                last_mod_list.append(objs.last_modified)
            total_size += objs.size
        record['num_files'] = num_files
        record['total_size'] = total_size
        record['last_modified_date'] = str(max(last_mod_list))
        records.append(record)
    gen_report(records, args.unit)


if __name__ == "__main__":
    main()
