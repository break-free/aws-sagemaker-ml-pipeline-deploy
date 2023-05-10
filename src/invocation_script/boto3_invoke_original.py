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
# Expect Setosa:
payload = pd.DataFrame([[4.5,3.45,1.5,1.2]]) # 4.5cm sepal length, 3.45cm sepal width, 1.5cm petal length, 1.2cm width

# Expect Versicolor:
# payload = pd.DataFrame([[6.0,3.45,4.0,1.2]]) # 6.0cm sepal length, 3.45cm sepal width, 4.0cm petal length, 1.2cm width

# Expect Virginica:
# payload = pd.DataFrame([[7.2,3.45,6.9,1.2]]) # 7.2cm sepal length, 3.45cm sepal width, 6.9cm petal length, 1.2cm width

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