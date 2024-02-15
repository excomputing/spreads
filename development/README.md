<br>

Notes

<br>

## Remote & Local Environments

### Remote



### Local



<br>

## Development Notes

The directive

```shell
pylint --generate-rcfile > .pylintrc
```

generates the dotfile `.pylintrc` of the static code analyser [pylint](https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html).  Subsequently, analyse via

```shell
python -m pylint --rcfile .pylintrc ...
```

<br>

## Simple Storage Service

About [list_objects_v2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html)

```python
# ResponseMetadata
pattern = {
    'RequestId': '...', 
    'HostId': '...', 
    'HTTPStatusCode': 200, 
    'HTTPHeaders': {
        'x-amz-id-2': '...', 
        'x-amz-request-id': '...', 
        'date': 'Thu, 15 Feb 2024 21:30:43 GMT', 
        'x-amz-bucket-region': 'eu-west-1', 
        'content-type': 'application/xml', 
        'transfer-encoding': 'chunked', 
        'server': 'AmazonS3'}, 
    'RetryAttempts': 0}
```


<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
