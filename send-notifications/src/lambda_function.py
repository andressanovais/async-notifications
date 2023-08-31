import json
import boto3
import redis


def lambda_handler(event):
    r = redis.Redis(
        host='master.lala.sae1.cache.amazonaws.com',
        port=7236,
        password='umaSenhaGeradaAleatoriamente',
        ssl=True,
        decode_responses=True,
    )
    
    connection_id = r.get(f"user:{event['user_id']}:connection")

    client = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url='https://lala.execute-api.sa-east-1.amazonaws.com/develop',
    )
    
    print(f'conexao: {connection_id}')
    resp = client.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(event),
    )
    
    return {
        'statusCode': 200,
    }
