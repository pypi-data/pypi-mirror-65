from decimal import Decimal
from numbers import Number

import boto3


def create_topics_table(name="fdbk_topics", *args, **kwargs):
    dynamodb = boto3.client('dynamodb', *args, **kwargs)

    return dynamodb.create_table(
        TableName=name,
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        BillingMode='PAY_PER_REQUEST',
    )


def create_data_table(name="fdbk_data", *args, **kwargs):
    dynamodb = boto3.client('dynamodb', *args, **kwargs)

    return dynamodb.create_table(
        TableName=name,
        AttributeDefinitions=[
            {
                'AttributeName': 'topic_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'topic_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'timestamp',
                'KeyType': 'RANGE'
            },
        ],
        BillingMode='PAY_PER_REQUEST',
    )


def delete_table(name, *args, **kwargs):
    dynamodb = boto3.client('dynamodb', *args, **kwargs)

    return dynamodb.delete_table(
        TableName=name,
    )


def delete_topics_table(name="fdbk_topics", *args, **kwargs):
    return delete_table(name, *args, **kwargs)


def delete_data_table(name="fdbk_data", *args, **kwargs):
    return delete_table(name, *args, **kwargs)


def obj_decimals_to_numbers(obj):
    for key, value in obj.items():
        if isinstance(value, Decimal):
            if value % 1 > 0:
                obj[key] = float(value)
            else:
                obj[key] = int(value)

    return obj


def obj_numbers_to_decimals(obj):
    for key, value in obj.items():
        if isinstance(value, Number):
            obj[key] = Decimal(str(value))

    return obj
