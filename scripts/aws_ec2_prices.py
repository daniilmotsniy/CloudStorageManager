from os import environ

import boto3
import json
from pkg_resources import resource_filename

# Search product filter. This will reduce the amount of data returned by the
# get_products function of the Pricing API
FLT = '[{{"Field": "tenancy", "Value": "shared", "Type": "TERM_MATCH"}},'\
      '{{"Field": "operatingSystem", "Value": "{o}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "preInstalledSw", "Value": "NA", "Type": "TERM_MATCH"}},'\
      '{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "capacitystatus", "Value": "Used", "Type": "TERM_MATCH"}}]'

# "servicecode": "AmazonS3",
# "location": "US East (N. Virginia)",
# "locationType": "AWS Region",
# "group": "INT-AA-RestoreObject",
# "groupDescription": "Expedited INT Retrieval",
# "usagetype": "USE1-Expedited-Retrieval-Bytes",
# "operation": "IntAARestoreObject",
# "regionCode": "us-east-1",
# "servicename": "Amazon Simple Storage Service"


# Get current AWS price for an on-demand instance
def get_price(region, instance, os):
    f = FLT.format(r=region, t=instance, o=os)
    data = client.get_products(ServiceCode='AmazonEC2', Filters=json.loads(f))
    od = json.loads(data['PriceList'][0])['terms']['OnDemand']
    id1 = list(od)[0]
    id2 = list(od[id1]['priceDimensions'])[0]
    return od[id1]['priceDimensions'][id2]['pricePerUnit']['USD']


def get_region_name(region_code):
    default_region = 'US East (N. Virginia)'
    endpoint_file = resource_filename('botocore', 'data/endpoints.json')
    try:
        with open(endpoint_file, 'r') as f:
            data = json.load(f)
        # Botocore is using Europe while Pricing API using EU...sigh...
        return data['partitions'][0]['regions'][region_code]['description'].replace('Europe', 'EU')
    except IOError:
        return default_region


# Use AWS Pricing API through Boto3
# API only has us-east-1 and ap-south-1 as valid endpoints.
# It doesn't have any impact on your selected region for your instance.
session = boto3.Session(region_name='us-east-1',
                        aws_access_key_id=environ['AWS_ACCESS_KEY'],
                        aws_secret_access_key=environ['AWS_SECRET_KEY'])
client = session.client('pricing')


if __name__ == '__main__':
    # Get current price for a given instance, region and os
    price = get_price(get_region_name('eu-west-1'), 't3.micro', 'Linux')
    print(price)
