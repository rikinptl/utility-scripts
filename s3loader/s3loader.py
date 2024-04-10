
try:
        import csv
        import json
        from jsonschema import validate, ValidationError
        import boto3 
        import pandas as pd
        import os 
        from PIL import Image
        import io
        import base64
        import requests
        from typing import Dict, Any,Union
        from io import BytesIO
except ModuleNotFoundError:
        print("Please download dependencies from requirement.txt")
except Exception as ex:
        print(ex)

class S3Loader:
        def __init__(self) -> None:
            pass
        @staticmethod
        def connect_to_s3(s3_credentials_path: str)-> boto3.resources.base.ServiceResource:
            try:
                aws_access_key = None
                secret_access_key = None

                with open(s3_credentials_path, mode='r', encoding='utf8') as file:
                    csv_reader = csv.DictReader(file)
                    fields = csv_reader.fieldnames

                    for key in csv_reader:
                        aws_access_key = key[fields[0]]
                        secret_access_key = key[fields[1]]

                return boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=secret_access_key)
            except Exception as ex:
                print(ex)

bucket = 'autoweby-userinfo-prod-us-east-2'

def push_to_s3(client: Union[boto3.resources.base.ServiceResource], data: Dict[str, Any], file_type: str = None, path: str =None, userid: str =None, validate_data: bool =False, config: str =None)-> None:
        userid = data['user_data']['user_uuid']
        if path == None :
            path = f"Candidate_Profile/{userid}/"
                     
        def push_data(data,path,file_type)-> None:
            client.put_object(Bucket = bucket, Key = path + 'Documents/')
            if file_type == None:
                 json_data = json.dumps(data['user_data'])
                 body = json_data.encode('utf-8')
                 client.put_object(Body = body, Bucket =bucket, Key= path + f'{userid}.json' )
            elif file_type.lower() == 'excel': 
                df = pd.DataFrame([data['user_data']])
                transposed_df = df.transpose()
                # Reset index to make the current index (column names) as a column
                transposed_df.reset_index(inplace=True)

                # Set the first row as column names
                transposed_df.columns = transposed_df.iloc[0]

                # Drop the first row as it's now redundant
                transposed_df = transposed_df.drop(0)
                excel_buffer = BytesIO()
                transposed_df.to_excel(excel_buffer, index = False, sheet_name = f'{userid}') 
                excel_buffer.seek(0)
                client.upload_fileobj(excel_buffer, bucket, path + f'{userid}.xlsx')
                
            else : 
                 print('Invalid file format! Default set to json or specify parameter file_type as excel')

           # folders = data['documents_info'].keys()
           # for folder in folders :
             #   for i in range(len(data['documents_info'][folder])):
             #       client.put_object(Bucket =bucket, Key= path + 'Documents/'+ folder + '/' + data['documents_info'][folder][i]['Document Name'])

        def data_val(data, config) -> bool:
            try:
                with open(config, 'r') as schema_file:
                    schema_content = schema_file.read()

                    schema = json.loads(schema_content)
            
                validate(data['user_data'], schema)
                return True
            except ValidationError as ex:
                print(f"Validation error: {ex.message}")
                return False
            except json.decoder.JSONDecodeError as json_error:
                print(f"JSON decoding error: {json_error}")
                return False


        if not validate_data:
            try:
                push_data(data,path,file_type)
            except:
                print('Error Pushing to S3!')
        else:
            try:
                if data_val(data,config):
                    push_data(data,path,file_type)
            except Exception as ex: 
                print(ex)

def fetch_from_s3(client: Union[boto3.resources.base.ServiceResource], userid: str, file_type:str = None)-> Dict[str, Any]:
    sheet_info = None
    doc_info = []

    if file_type == None:
        response = client.get_object(Bucket=bucket, Key=f"Candidate_Profile/{userid}/{userid}.json")
        sheet_info = json.loads(response['Body'].read().decode('utf-8'))
        
    elif file_type.lower() == 'excel':
        response = client.get_object(Bucket=bucket, Key=f"Candidate_Profile/{userid}/{userid}.xlsx")           
        excel_data = response['Body'].read()
        excel_df = pd.read_excel(BytesIO(excel_data))
        sheet_info = {row[0]: row[1] for row in excel_df.values}
        
    else: 
        print('Invalid file type requested.')
    
    document_info = client.list_objects_v2(Bucket=bucket)

    for item in document_info.get('Contents', [])[1:]:
        if f"Candidate_Profile/{userid}/Documents" in item['Key']:
            doc_name = item['Key'].rsplit('/', 1)[-1]
            if doc_name:  # Check if doc_name is not an empty string
                doc_path_on_s3 = item['Key']
                doc_link = f"https://autoweby-userinfo-prod-us-east-2.s3.us-east-2.amazonaws.com/{doc_path_on_s3.rsplit('/', 1)[0]}/{doc_name.replace(' ','+').replace('+','%2B')}"
                doc_info.append({'doc_name': doc_name, 'doc_path_on_s3': doc_path_on_s3,'doc_link': doc_link})



    user_data = {
        "response": [
            {"sheet_info": sheet_info},
            {"doc_info": doc_info}
        ]
    }
    
    return user_data
def doc(client: Union[boto3.resources.base.ServiceResource], mode:str , userid:str, folder: str, doc_name: str,data:str = None,path:str = None)-> None:
    if path == None:
        path = f"Candidate_Profile/{userid}/Documents/{folder}/{doc_name}"
    def push()-> None:
        try:
            pdf_bytes = base64.b64decode(data)
            #pdf_bytes = data.decode('utf-8')
            if doc_name.split('.')[-1] == 'pdf':
                client.put_object(ACL = 'public-read',Bucket =bucket, Key= path, Body = pdf_bytes,ContentType='application/pdf',ContentDisposition = 'inline')
            elif doc_name.split('.')[-1] == 'png':
                client.put_object(ACL = 'public-read',Bucket =bucket, Key= path, Body = pdf_bytes,ContentType='image/png',ContentDisposition = 'inline')
            elif doc_name.split('.')[-1] in ['jpeg','jpg']:
                client.put_object(ACL = 'public-read',Bucket =bucket, Key= path, Body = pdf_bytes,ContentType='image/jpeg',ContentDisposition = 'inline')
            elif doc_name.split('.')[-1] == 'xlsx':
                client.put_object(ACL = 'public-read',Bucket =bucket, Key= path, Body = pdf_bytes,ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',ContentDisposition = 'inline')
            else:
                client.put_object(ACL = 'public-read',Bucket =bucket, Key= path, Body = pdf_bytes,ContentType='text/plain',ContentDisposition = 'inline')
            
        except Exception as ex:
            print(ex)
    def fetch()-> str:
        try:
            url = f"https://{bucket}.s3.us-east-2.amazonaws.com/Candidate_Profile/{userid}/Documents/{folder}/{doc_name.replace(' ', '+').replace('+','%2B')}"
            response = requests.get(url)
            if response.status_code == 200:
            # Create directory if it does not exist
                os.makedirs(os.path.dirname(path), exist_ok=True)
            
                with open(path, "wb") as file:
                    file.write(response.content)
                print("PDF saved successfully")
            else:
                print(response.status_code)
        except Exception as ex:
             print(ex)
    def delete()-> None: 
        try:
            client.delete_object(Bucket= bucket, Key= path)
        except Exception as ex:
            print(ex)
        
    if mode.lower() not in ['push','fetch','delete']:
         print('Can only perform push/fetch/delete operation!')
    elif mode.lower() == 'push':
         push()
    elif mode.lower() == 'fetch':
         fetch()
    elif mode.lower() == 'delete':
         delete()

def main()-> None:
    client = S3Loader.connect_to_s3(r'C:\Users\Pjp\Downloads\rootkey.csv')
    data= {
        "message": "created",
        "user_data": {
            "id": 25,
            "email": "vacha159@webyops.com",
            "password": "12345",
            "first_name": "rikin",
            "last_name": "patel",
            "address": "anand",
            "address2": "demo role",
            "city": "anand",
            "state": "gujarat",
            "zipcode": "388320",
            "country": "India",
            "phone_number": "12345",
            "user_uuid": "rikin",
            "reset_question": "school",
            "reset_answer": "anandalaya",
            "user_role": "candidate"
        }
    }
    #push_to_s3(client, data,file_type='excel', validate_data= True, config= r'val_schema.json')
    #jsond = fetch_from_s3(client,'rikin',file_type='excel')
    #print(jsond)
    with open('jpg_data.txt', 'r') as file:
        bin_data = file.read()
    
    
    bin_data = bin_data.encode('utf-8')
    #bin_data = base64.b64encode(bin_data.encode('utf-8'))
    doc(client,'push','gFqVgCEUhVVX3Ys3uRTZwL','resume','sample_jpg.jpg',bin_data)
if __name__ == '__main__':
        main()