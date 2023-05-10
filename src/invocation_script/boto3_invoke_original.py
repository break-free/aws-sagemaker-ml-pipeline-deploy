import boto3
from io import StringIO
import pandas as pd

client = boto3.client('sagemaker-runtime')

endpoint_name = 'breakfree-ml-pipeline-20230510202603' # Your endpoint name.
content_type = "text/csv"   # The MIME type of the input data in the request body.

"""
There's a world-famous dataset (https://archive.ics.uci.edu/ml/datasets/iris) that lots of machine learning models use to train themselves.
The data is provided in a CSV format as 
    sepal length in cm | sepal width in cm | petal length in cm | petal width in cm | class (label)
"""
payload = pd.DataFrame([[1.5,0.2,4.4,2.6]]) # 1.5cm sepal length, 0.2cm sepal width, 4.4cm petal length, 2.6cm width
csv_file = StringIO()
payload.to_csv(csv_file, sep=",", header=False, index=False)
payload_as_csv = csv_file.getvalue()

response = client.invoke_endpoint(
    EndpointName=endpoint_name, 
    ContentType=content_type,
    Body=payload_as_csv
    )

label = response['Body'].read().decode('utf-8')
print(label)