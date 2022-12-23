import pandas as pd
import os
import time

from NaturalLanguageProcessing import udotNLP

from annoy import AnnoyIndex

from flask import Flask
from flask_restful import Resource, Api

import tensorflow_hub as hub
import tensorflow as tf



# AUX METHODS BELOW

jobs_df = None
embeddings_df = None
embed = None


def get_repo() -> None:
  """
  clones the repository automatically
  """

  try:
    os.system('git clone https://github.com/UniversalDot/tensorflow')
  except:
    print('it was not possible to get the dataset')
    return
  finally:
    print('dataset downloaded')


def get_dataset() -> tf.Tensor:
  """
  loads the dataset in a format readable from the create_save function
  """
  df = tf.data.Dataset.load('/content/tensorflow/dataset/key_embeddings')
  df = tf.reshape(df.get_single_element(), (-1, 512))
  df = tf.data.Dataset.from_tensor_slices(df)
  return df


def update():
    start_time = time.time()

    global jobs_df, embeddings_df, embed
    # TODO
    jobs_df = pd.read_csv("../dataset/jobsdesc_extended.csv")
    # TODO
    # embeddings_df = pd.read_csv("../dataset/embeddings-msmarco-distilbert-base-v4.csv")
    embeddings_df = pd.read_csv("../dataset/jobsdesc_embeddings_use.csv")

    print("Downloading Embedder")
    if embed is None:
        module_url = 'https://tfhub.dev/google/universal-sentence-encoder-large/5'
        embed = hub.KerasLayer(module_url, trainable=True, name='USE_embedding')



    print("Files are Updated                     :",
          time.time() - start_time)



# API ROUTES BELOW
app = Flask(__name__)
api = Api(app)

# Prediction class where the input is collected
class predict(Resource):
    def get(self, AVAILABILITY, REPUTATION, INTEREST):
        """

        :param AVAILABILITY: Availability of the Profile
        :param REPUTATION:
        :param INTEREST:
        :return:
        """

        # Update the Database
        update()

        # Filter on Reputation; Eliminate the tasks that requires more reputation than the user has.
        start_time = time.time()
        filtered_reputation = jobs_df[jobs_df["Required Reputation"] < REPUTATION]
        print("Filtered on Reputation                :",
              time.time() - start_time, "Remaining Jobs:", len(filtered_reputation))

        # Filter on Availability; Eliminate the tasks that requires more hours a week than the user has.
        start_time = time.time()
        filtered_availability = filtered_reputation[filtered_reputation["Hours Needed"] < AVAILABILITY]
        print("Filtered on Availability              :",
              time.time() - start_time, "Remaining Jobs:", len(filtered_availability))

        # Get the remaining tasks ID
        start_time = time.time()
        available_id = filtered_availability.reset_index()["index"].tolist()
        print("The remaining task ID's are collected :",
              time.time() - start_time)

        # Return the embeddings of the remaining jobs
        start_time = time.time()
        embeddings_to_be_searched = []
        for id in available_id:
            embeddings_to_be_searched.append(embeddings_df.iloc[id].values.flatten().tolist()[1:])
        print("Embeddings are collected              :", time.time() - start_time)

        # Build Annoy
        start_time = time.time()
        vector_size = len(embeddings_to_be_searched[0])
        annoy = AnnoyIndex(vector_size, 'euclidean')
        for i in range(len(embeddings_to_be_searched)):
            v = embeddings_to_be_searched[i]
            annoy.add_item(i, v)

        annoy.build(100)
        print("Annoy is built                        :", time.time() - start_time)

        # Preprocess INTEREST
        start_time = time.time()
        interest_keywords = udotNLP.text2Keywords(INTEREST)

        interest_embeddings = embed(interest_keywords)
        print("Preprocessing of INTEREST is done     :"
              , time.time() - start_time)


        closest_points = annoy.get_nns_by_vector(interest_embeddings[0], 5)

        print(" ---- ")
        for i in closest_points:
            print(jobs_df["jobdescription"].iloc[i])
            print(" ---- ")



        return {"Availability": AVAILABILITY,
                "Reputation": REPUTATION,
                "Interest": INTEREST,
                "Possible Jobs": closest_points}


api.add_resource(predict, "/predict/<int:AVAILABILITY>/<int:REPUTATION>/<string:INTEREST>")




# NOTE: IF YOU RUN 'flask run', THE CODE BELOW WON'T BE EXECUTED
if __name__ == '__main__':
    app.run(debug=True)





