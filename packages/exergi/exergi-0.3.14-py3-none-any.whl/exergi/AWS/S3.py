""" This module defines all exergi functions within the AWS.S3 module"""

def exportPandasToS3(obj,bucket,key):
    """ This module exports a pandas.DataFrame to specified bucket/key. 

    Keyword Arguments:
        - obj [python obj.]  -- Python object to be exported
        - bucket [str]       -- S3 export bucket,no trailing "/".
                                "stage-data-scientist".
        - key [str]          -- S3 export key, no leading "/". String should 
                                end with the desired file format. 
                                "public/.../example.csv". Currently supported 
                                fileformats is .csv,.xlsx & .pkl
    Returns:
        None
    """

    import boto3
    import io
    import pickle
    import os
    import pandas as pd
    import tempfile
    from sklearn.externals import joblib
    from sklearn.preprocessing import MinMaxScaler
    
    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   

    fileName, fileFormat = os.path.splitext(key)

    if fileFormat == ".csv":
        buffer = io.StringIO()
        obj.to_csv(buffer,index=False)    
        s3resource.Object(bucket, key).put(Body=buffer.getvalue())

    elif fileFormat == ".xlsx":
        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                obj.to_excel(writer)
            data = output.getvalue()
            s3resource.Object(bucket, key).put(Body=data)

    elif fileFormat == ".pkl":
        if obj.__class__.__module__.split(".")[0] == "sklearn":
            with tempfile.TemporaryFile() as fp:
                joblib.dump(obj, fp)
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read())
        elif obj.__class__.__module__.split(".")[0] == "keras":
            serializedMyData = pickle.dumps(obj)
            s3resource.Object(bucket, key).put(Body=serializedMyData)
        elif obj.__class__.__module__.split(".")[0] == "pandas":
            serializedMyData = pickle.dumps(obj)
            s3resource.Object(bucket, key).put(Body=serializedMyData)
        else:
            raise("Object class not supported for export")

    else:
        raise("File format ({}) not supported".format(fileFormat))

def importFileFromS3(bucket, key,**kwargs):
    """ This module imports a pandas.DataFrame from specified bucket/key. 

    Arguments:
        - bucket [str]      -   S3 export bucket,no trailing "/".
                                "stage-data-scientist".
        - key [str]         -   S3 export key, no leading "/". String should 
                                end with the desired file format. 
                                "public/.../example.csv". Currently supported 
                                fileformats is .csv,.xlsx & .pkl
    Keyword Arguments:
        - **kwargs [any]    -   Keyword arguments import function. Import 
                                function varies for each file format: 
                                file format:
                                    .csv  = pd.read_csv()
                                    .xlsx = pd.read_excel()
                                    .pkl  = pd.read_pickle()
    Returns:
        - df [pd.DataFrame] -   Imported DataFrame
    """
    import boto3
    import io
    import os
    import pandas as pd

    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   
    obj = s3client.get_object(Bucket=bucket,Key=key)
    data = obj["Body"].read()
    
    _, fileFormat = os.path.splitext(key)

    if fileFormat == ".csv":
        df = pd.read_csv(io.BytesIO(data),**kwargs)
    elif fileFormat == ".xlsx":
        df = pd.read_excel(io.BytesIO(data), **kwargs)
    elif fileFormat == ".pkl":
        df = pd.read_pickle(io.BytesIO(data), **kwargs)
    else:
        raise("File format ({}) not supported".format(fileFormat))
    return df

def getFilePath(bucket,prefix):
    """ List all files (sorted) in the specified bucket
    
    Arguments:
        - bucket [str]      -   S3 bucket where path i located,no trailing "/".
                                "stage-data-scientist".
        - prefix [str]      -   S3 prefix where files should be listed, "/". 
    Returns:
        - pathsToCsv [lst]  -   List of files in bucket-prefix. 
    """
    import pandas as pd
    import io
    import boto3

    s3resource = boto3.resource("s3")
    s3bucket = s3resource.Bucket(bucket)
    pathsToCsv = []
    
    for objectSummary in list(s3bucket.objects.filter(Prefix=prefix))[0:]:
        pathsToCsv.append(objectSummary.key)
    pathsToCsv = [file.replace(prefix,"") for file in pathsToCsv if file != prefix]
    pathsToCsv = sorted([file for file in pathsToCsv if not "/" in file])
    return pathsToCsv