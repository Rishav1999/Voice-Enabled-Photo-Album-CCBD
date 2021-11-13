import json
import urllib.parse
import boto3
import logging
import requests

print('Loading function')

s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

label_list=[]

def insert(key, label_list):
    es_dict = {"image_name":key, "category": label_list}
    #Inserting Into Elastic Search
    response1 = requests.post(
        url="https://search-photos-j4x6mrklmexwgxabap7luxu23y.us-east-1.es.amazonaws.com/photos/_doc",
        data=json.dumps(es_dict),
        headers={'Content-Type': 'application/json'},
        auth=('Rishav17', 'Rishav1708#'))
        
        
def lambda_handler(event, context):
    logger.debug("hello")
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
        
    logger.debug('reading image: {} from s3 bucket {}'.format(key, bucket))
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MaxLabels=12,
        MinConfidence=80,
    )
    
    logger.debug('Detected labels for ' + key)
    for label in response['Labels']:
        logger.debug(label['Name'] + ' : ' + str(label['Confidence']))
        label_list.append(label['Name'])
        print("Hello",label['Name'])
    print(label_list)
    metadata = s3.head_object(Bucket='photoalbumb', Key=key)
    print(metadata)
    time = metadata['ResponseMetadata']['HTTPHeaders']['date']
    new_label= metadata['ResponseMetadata']['HTTPHeaders']['x-amz-meta-customlabels']
    string_label = new_label.split(',')
    for x in string_label:
        label_list.append(x)
    # time = metadata.get('date')
    print("Time",time)
    print(label_list)
    insert(key, label_list)
