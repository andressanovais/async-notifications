import boto3


def get_secret(secret_name: str) -> str:
    client = boto3.client('secretsmanager')
    return client.get_secret_value(SecretId=secret_name)['SecretString']
