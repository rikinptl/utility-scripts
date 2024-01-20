
try:
    import csv
    import json
    from jsonschema import validate, ValidationError
    import boto3 
    import pandas as pd
    from typing import Dict, Any, Union
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



def push_to_s3(client: Union[boto3.resources.base.ServiceResource], data: Dict[str, Any], path: str =None, userid: str =None, validate_data: bool =False, config: str =None)-> None:

    if path == None :
         path = f'Candidate Profile/{userid}.xlsx'
    
    def push_data(data,path)-> None:
        df = pd.DataFrame([data])
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index = False, sheet_name = f'{userid}') 
        excel_buffer.seek(0)
        client.upload_fileobj(excel_buffer, 'autoweby-userinfo-prod-us-east-2', path)

    def data_val(data, config) -> bool:
        try:
            with open(config, 'r') as schema_file:
                schema_content = schema_file.read()

                schema = json.loads(schema_content)
        
            validate(data, schema)
            return True
        except ValidationError as ex:
            print(f"Validation error: {ex.message}")
            return False
        except json.decoder.JSONDecodeError as json_error:
            print(f"JSON decoding error: {json_error}")
            return False


    if not validate_data:
        try:
            push_data(data,path)
        except:
            print('Error Pushing to S3!')
    else:
        try:
            if data_val(data,config):
                push_data(data,path)
        except Exception as ex: 
            print(ex)

            


def main()-> None:
    client = S3Loader.connect_to_s3(r'C:\Users\Pjp\Downloads\rootkey.csv')
    data = {
  "user_id": "2b38a163-4b12-45e0-8ca9-eb53bc7d8e74",
  "First Name": "John",
  "Middle Name": "Doe",
  "Last Name": "Smith",
  "Personal Email Address": "john.doe@example.com",
  "Marketing Email Address": "john.doe@example.com",
  "Phone Number Personal": "1234567890",
  "Phone Number Marketing": "9876543210",
  "Address 1": "123 Main St",
  "Address 2": "Apt 456",
  "City": "Anytown",
  "State": "CA",
  "Zipcode": 12345,
  "Current Passport Number": "AB123456",
  "Old Passport Number": "XY987654"
}

    push_to_s3(client, data,userid = 'rikin', validate_data= True, config= r'val_schema.json')

if __name__ == '__main__':
    main()
