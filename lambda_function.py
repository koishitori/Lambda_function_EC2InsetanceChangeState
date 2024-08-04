import boto3
import json

def lambda_handler(event, context):
    region = event['region']
    tag_name = event['tagName']
    action = event['action']
    test = event['test']

    ec2 = boto3.client('ec2', region_name=region)

    # Get EC2 instances with the specified tag
    response = ec2.describe_instances(
        Filters=[
            {'Name': f'tag:{tag_name}', 'Values': [action, 'true']}
        ]
    )

    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A')
            instances.append((instance_id, name))

    if not instances:
        return {
            'statusCode': 200,
            'body': json.dumps(f'No instances found with tag {tag_name}={action} or {tag_name}=true')
        }

    for instance_id, name in instances:
        print(f"Instance ID: {instance_id} ({name})")

    instance_ids = [instance[0] for instance in instances]

    if not test:
        if action == 'start':
            ec2.start_instances(InstanceIds=instance_ids)
            message = f"Started instances: {', '.join([f'{id} ({name})' for id, name in instances])}"
        elif action == 'stop':
            ec2.stop_instances(InstanceIds=instance_ids)
            message = f"Stopped instances: {', '.join([f'{id} ({name})' for id, name in instances])}"
        else:
            message = f"Invalid action: {action}. Use 'start' or 'stop'."
    else:
        message = f"Test mode: Would have {action}ed instances: {', '.join([f'{id} ({name})' for id, name in instances])}"

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }