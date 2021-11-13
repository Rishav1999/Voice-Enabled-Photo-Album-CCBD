import requests
import json
import boto3

def getting_es_data(category):
    l= []
    es_dict = {'query': {'match': {'category': category}}}
    
    response = requests.get(
        url="https://search-photos-j4x6mrklmexwgxabap7luxu23y.us-east-1.es.amazonaws.com/photos/_search",
        headers={'content-type': 'application/json'},
        auth=('Rishav17', 'Rishav1708#'), data=json.dumps(es_dict))
        
    data = json.loads(response.content.decode('utf-8'))
    #print(data['hits']['hits'])
    
    #l = []
    for x in data['hits']['hits']:
        l.append(x['_source']['image_name'])
    return l

def lambda_handler(event, context):
    client = boto3.client('lex-runtime')

    response = client.post_text(
        botName='PhotoRetrieve',
        botAlias='bot_photos',
        userId='testuser',
        inputText= event["queryStringParameters"]["q"])

    print(response)
    a = response['slots']['category']
    b = response['slots']['category_one']
    m1 = []
    m2= []
    if a is not None:
        m1 = getting_es_data(a)
    if b is not None:
        m2 = getting_es_data(b)
    m = m1 + m2
    return {
        
        'isBase64Encoded':False,
        'statusCode': 200,
        'headers':{'Access-Control-Allow-Origin':'*'},
        'body':json.dumps(m)
    }
