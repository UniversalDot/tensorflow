# Tensorflow
This repository contains the TensorFlow models and its associated data.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# Model creation
The model used for the recommendation system is the [ScaNN](https://github.com/google-research/google-research/tree/master/scann) implemented through [Tensorflow](https://www.tensorflow.org/recommenders/api_docs/python/tfrs/layers/factorized_top_k/ScaNN) to allow serving with Tensorflow Serving service.
The model creation process each time requires different steps:
- Preprocessing
    - Simple text preprocessing
    - Keyword extraction
- Embedding
- Training of the ScaNN
- Testing
- Saving and serving
## Preprocessing
### Simple text preprocessing
### Keyword extraction
TODO
## Embedding
TODO
## Training
The training of the ScaNN can be found in model_creation folder
## Testing
TODO
## Saving and serving
The saving of the ScaNN can be found in model_creation folder
# Deployment

The model is deployed to Tensorflow Serving. Its design is outlined in the image below.


![Deployment](https://github.com/UniversalDot/tensorflow/blob/develop/design/deployment.png)

# Testing the model

TODO
## Testing on Colab

Access on the [Colab notebook](https://colab.research.google.com/drive/1Dg1cvifrzqrtuhPyf_kTOCejl3wbt9c_?usp=sharing) to test the trained model interactivelly.
## Maintainers

[@VittorioRossi](https://github.com/VittorioRossi) [@Tunahan Sarı](https://github.com/TutubanaS)






