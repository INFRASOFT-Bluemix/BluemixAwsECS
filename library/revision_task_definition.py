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
cluster_name = os.environ['CLUSTER_NAME']
td_name = os.environ['TASK_DEFINITION']
image_name = os.environ['IMAGE_NAME']

# ECS Details

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import boto3_conn, ec2_argument_spec, get_aws_connection_info, camel_dict_to_snake_dict

def main():

  msg = ""

  argument_spec = ec2_argument_spec()

  module = AnsibleModule(
    argument_spec=argument_spec,
    supports_check_mode=True,
    mutually_exclusive=[],
    required_together=[]
  )

  client = boto3.client(
    'ecs',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
  )

  response = client.register_task_definition(
    family=td_name,
    containerDefinitions=[
    {
      "name":td_name,
      "image":image_name,
      "memory":512,
      "portMappings":[
      {
        "hostPort":80,
        "containerPort":8081,
        "protocol":"tcp"
      }],
      "essential":True,
      "entryPoint":
      [
        "java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "/app.jar", "--server.port=8081"
      ],
      "cpu":0 
    }]
  )

  msg = "Revision Task Definition"
  
  result = dict(changed=False, output=msg)
  module.exit_json(**result)

if __name__ == "__main__":
  main()



