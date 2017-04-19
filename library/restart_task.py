#!/usr/bin/python

try:
  import boto3
  HAS_BOTO3 = True
except ImportError:
  HAS_BOTO3 = False

import pprint
import os

# Credentials & Region
access_key = os.environ['AWS_ACCESS_KEY_ID']
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
region = os.environ['AWS_DEFAULT_REGION']

# ECS Details

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import boto3_conn, ec2_argument_spec, get_aws_connection_info, camel_dict_to_snake_dict

def test_main():

  msg = ""
	
  argument_spec = ec2_argument_spec()

  module = AnsibleModule(
    argument_spec=argument_spec,
    supports_check_mode=True,
    mutually_exclusive=[],
    required_together=[]
  )

  # Let's use Amazon ECS
  client = boto3.client(
    'ecs',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name="ap-southeast-2"
  )
  
  response = client.list_tasks(
    cluster="cluster-poc",
    desiredStatus='RUNNING'
  )
  
  task_arn = response['taskArns'][0]
  
  response = client.stop_task(
    cluster="cluster-poc",
    task=task_arn,
    reason='Stop by BMX'
  )

  msg = "Task Stop"
	  
  result = dict(changed=False, output=msg)
  module.exit_json(**result)

if __name__ == "__main__":
  test_main()
