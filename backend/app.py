from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)


# Open model initiation

def open_model(model_path):
    """
    helper function for loading model
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model_cluster = open_model("kmodes_4.pkl") 

def inference_cluster(data, model):
    """
    input : list with length : 6 --> [1, 2, 3, 4, 5, male/female]
    ouput : predicted class (idx, label)
    """
    label = ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3']
    columns = ['Reading', 'Music', 'Cinema', 'Exhibition', 'Computer', 
               'Sport', 'Walking', 'Travelling', 'Gardening', 'Cooking', 'Fishing',
               'Sex', 'Age', 'MaritalStatus', 'Profession']
    data = pd.DataFrame([data],columns=columns)
    res = model_cluster.predict(data)
    return res[0], label[res[0]]


# Homepage

@app.route("/")
def welcome():
    return "<h3>Selamat Datang di Healing Project</h3>"

# Predict page

@app.route("/predict", methods=["GET", "POST"])
def predict_cluster():
    columns = ['Reading', 'Music', 'Cinema', 'Exhibition', 'Computer', 
               'Sport', 'Walking', 'Travelling', 'Gardening', 'Cooking', 'Fishing',
               'Sex', 'Age', 'MaritalStatus', 'Profession']
    content = request.json
    newdata = [content['Reading'], 
               content['Music'],
               content['Cinema'],
               content['Exhibition'],
               content['Computer'],
               content['Sport'],
               content['Walking'],
               content['Travelling'],
               content['Gardening'],
               content['Cooking'],
               content['Fishing'],
               content['Sex'],
               content['Age'],
               content['MaritalStatus'],
               content['Profession']
               ]
    res_idx, res_label = inference_cluster(newdata, model_cluster)
    result = str(res_idx)

    response = jsonify(success=True,
                       result=result)
    return response, 200

# app.run(debug=True)