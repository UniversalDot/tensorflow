import pandas as pd
import time

from NaturalLanguageProcessing import udotNLP

from annoy import AnnoyIndex

from flask import Flask
from flask_restful import Resource, Api



# AUX METHODS BELOW

jobs_df = None
embeddings_df = None

def update():
    global jobs_df, embeddings_df
    # TODO
    jobs_df = pd.read_csv("../dataset/jobsdesc_extended.csv")
    # TODO
    embeddings_df = pd.read_csv("../dataset/embeddings-msmarco-distilbert-base-v4.csv")

    print("updated")




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

        # Filter on Reputation; Eliminate the tasks that requires more reputation than the user has.
        start_time = time.time()
        filtered_reputation = jobs_df[jobs_df["Requiered Reputation"] < REPUTATION]
        print("Filtered on Reputation                :",
              time.time() - start_time, "Remaining Jobs:", len(filtered_reputation))

        # Filter on Availability; Eliminate the tasks that requieres more hours a week than the user has.
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
        interest_embeddings = udotNLP.text2Embeddings(interest_keywords)
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




if __name__ == '__main__':
    update()
    app.run(debug=True)





