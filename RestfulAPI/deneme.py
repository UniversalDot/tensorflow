import pandas as pd
import tensorflow_hub as hub
from tqdm import tqdm

jobs_df = pd.read_csv("../dataset/jobsdesc_extended.csv")
jobs_df = jobs_df["jobdescription"]
jobs_list = jobs_df.tolist()

module_url = 'https://tfhub.dev/google/universal-sentence-encoder-large/5'
embed = hub.KerasLayer(module_url, trainable=True, name='USE_embedding')

embedding_list = []
for i in tqdm(range(len(jobs_list))):
    embedding = embed([jobs_list[i]]).numpy().tolist()[0]

    embedding_list.append(embedding)


print(embedding_list)
df = pd.DataFrame(embedding_list)
df.to_csv("jobsdesc_embeddings_use.csv")

