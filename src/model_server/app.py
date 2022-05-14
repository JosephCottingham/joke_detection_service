import json, boto3, os
import  tensorflow
# from zipfile import ZipFile
import tensorflow_text as text
import tensorflow_hub as hub
import joblib

# model_folder = "model"
# sub_folders = [name for name in os.listdir(model_folder) if os.path.isdir(os.path.join(model_folder, name))]
# model_folder = model_folder + '/' + sub_folders[0]

# model = load_model(('model.h5'),custom_objects={'KerasLayer':hub.KerasLayer})
model = joblib.load('model.joblib')

def lambda_handler(event, context):
    # Get the passed GET query pram (Should contain joke string)
    joke = event['queryStringParameters'].get('joke')
    # Set prediction to -1 if there is no joke argument included in the request
    prediction = -1
    if joke != None:
        # Run the joke though the model
        prediction = model.predict([joke])
    # return a json with the result of the model
    response =  json.dumps({"prediction":float(prediction[0][0])})
    return {
        'statusCode': 200,
        'headers':{
            'Content-type':'application/json'
        },
        'body': response
    }