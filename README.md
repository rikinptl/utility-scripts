# Utility Scripts

Welcome to the "utility-scripts" repository! This repository contains various Python utility scripts for different operations.

## Table of Contents
- [S3 Loader](#s3-loader)

## S3 Loader
The `s3loader/` subfolder is dedicated to the S3 Loader utility script. This script processes JSON data, validates it against a specified schema (located in the same directory), and then uploads the validated data into an S3 bucket.

### Usage
1. Place your JSON data file in the same directory.
2. Ensure that the schema file is available in the same directory.
3. Run the S3 Loader script.

Example:
```bash
python s3loader/s3_loader.py
