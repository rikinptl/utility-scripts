# Utility Scripts

🛠️ Welcome to the "utility-scripts" repository! This repository contains various Python utility scripts for different operations.

## Table of Contents
- [S3 Loader](#s3-loader-utility)

# S3 Loader Utility

🚀 Welcome to the `s3loader/` subfolder of the "utility-scripts" repository. This folder contains a Python utility script, `s3loader.py`, designed for uploading JSON data to an S3 bucket after validation against a specified schema.

## Files

- 📄 **s3loader.py**: Main Python script for the S3 Loader utility.
- 📄 **val_schema.json**: JSON schema file used for successful data validation.
- 📄 **non_val_schema.json**: JSON schema file designed to test failed data validation.

## Dependencies

Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```
# Usage

## S3Loader Class

- ⚙️**connect_to_s3(s3_credentials_path: str) -> boto3.resources.base.ServiceResource**: Establishes a connection to S3 using the provided AWS credentials.

## push_to_s3 Function

- ⬆️ **push_to_s3(client: boto3.resources.base.ServiceResource, data: Dict[str, Any], path: str = None, userid: str = None, validate_data: bool = False, config: str = None) -> None**: Uploads data to S3 after validation against a specified schema.

### Parameters:

- `client`: S3 client obtained from `S3Loader.connect_to_s3`.
- `data`: Dictionary containing the data to be uploaded.
- `path`: S3 bucket path where the data will be uploaded (default is based on user ID).
- `userid`: User ID used to construct the default path (if not provided, a default user ID is used).
- `validate_data`: Flag to enable or disable data validation (default is False).
- `config`: Path to the JSON schema file for data validation.

## main Function

- 🚀**main() -> None**: Example usage of the S3 Loader script. Establishes an S3 connection, defines sample data, and uploads it to S3 with or without data validation.

### Example

```python
if __name__ == '__main__':
    main()
```
Customize the sample data and paths according to your requirements.

# JSON Schema Files

- 📄**val_schema.json**: A sample JSON schema file for successful validation.
- 📄**non_val_schema.json**: A sample JSON schema file designed to test failed validation (change in property name).


Feel free to explore and enhance the S3 Loader utility script for your specific use case. Happy coding!  🚀

