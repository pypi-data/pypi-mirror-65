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
    
    # Connect to S3
    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   

    # Extra file name, file format and export object type
    _, fileFormat = os.path.splitext(key)
    objClass = obj.__class__.__module__.split(".")[0]
    raiseString = "Object class {} not supported for {} export. - ".format(objClass,fileFormat)

    # Comma separated files 
    if fileFormat == ".csv":
        if objClass == "pandas":
            buffer = io.StringIO()
            obj.to_csv(buffer,index=False)    
            s3resource.Object(bucket, key).put(Body=buffer.getvalue())
        else:
            raise Exception(raiseString)
        
    # Excel files 
    elif fileFormat == ".xlsx":
        if objClass == "pandas":
            with io.BytesIO() as output:
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    obj.to_excel(writer)
                data = output.getvalue()
                s3resource.Object(bucket, key).put(Body=data)
        else:
            raise Exception(raiseString)

    # Pickle files 
    elif fileFormat == ".pkl":
    
        if objClass == "sklearn":
            with tempfile.TemporaryFile() as fp:
                joblib.dump(obj, fp)
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read())
        elif objClass == "keras":
                joblib.dump(obj, fp)
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read())
            #serializedMyData = pickle.dumps(obj)
            #s3resource.Object(bucket, key).put(Body=serializedMyData)
        elif objClass == "pandas":
            serializedMyData = pickle.dumps(obj)
            s3resource.Object(bucket, key).put(Body=serializedMyData)
        else:
            raise Exception(raiseString)

def importFileFromS3(bucket, key, objClass="pandas", **kwargs):
    """ This module imports a pandas.DataFrame from specified bucket/key. 

    Arguments:
        - bucket [str]      -   S3 export bucket,no trailing "/".
                                "stage-data-scientist".
        - key [str]         -   S3 export key, no leading "/". String should 
                                end with the desired file format. 
                                "public/.../example.csv". Currently supported 
                                fileformats is .csv,.xlsx & .pkl
        - objClass [str]    -   String explaining what object type file should
                                be loaded as (default = "pandas")
    Keyword Arguments:
        - **kwargs [any]    -   Keyword arguments import function. Import 
                                function varies for each file format: 
                                file format:
                                    .csv  = pd.read_csv()
                                    .xlsx = pd.read_excel()
                                    .pkl  = pd.read_pickle()
    Returns:
        - obj [python obj]  -   Imported 
    """
    import boto3
    import io
    import os
    import pandas as pd
    from sklearn.externals import joblib
    from keras.models import load_model

    # Connect to S3
    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   

    # Extra file name, file format and export object type
    _, fileFormat = os.path.splitext(key)
    raiseString = "Object class {} not supported for {} export. - ".format(objClass,fileFormat)

    # Get raw data from S3
    S3obj = s3client.get_object(Bucket=bucket,Key=key)
    S3data = S3obj["Body"].read()

    # Comma separated files 
    if fileFormat == ".csv":
        if objClass == "pandas":
            obj = pd.read_csv(io.BytesIO(S3data),**kwargs)
        else:
            raise Exception(raiseString)

    # Excel files 
    elif fileFormat == ".xlsx":
        if objClass == "pandas":
            obj = pd.read_excel(io.BytesIO(S3data), **kwargs)
        else:
            raise Exception(raiseString)

    # Pickle files 
    elif fileFormat == ".pkl":
        if objClass == "pandas":
            obj = pd.read_pickle(io.BytesIO(S3data), **kwargs)
        elif objClass == "keras":
            tmp = tempfile.NamedTemporaryFile()
            with open(tmp.name, 'wb') as f:
                S3obj.download_fileobj(f)
                obj = load_model(temp.name)  
        elif objClass == "sklearn":
            tmp = tempfile.NamedTemporaryFile()
            with open(tmp.name, 'wb') as f:
                S3obj.download_fileobj(f)
                obj = joblib.load(temp.name)           
        else:
            raise Exception(raiseString)

    return obj

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






# FROM https://machinelearningmastery.com/save-load-keras-deep-learning-models/
# # Export keras 
# from keras.models import model_from_json

# model_json = model.to_json()
# with open("model.json", "w") as json_file:
#     json_file.write(model_json)
# # serialize weights to HDF5
# model.save_weights("model.h5")
# print("Saved model to disk")
 
# # Import keras 
# # load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("model.h5")
# print("Loaded model from disk")
# loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

