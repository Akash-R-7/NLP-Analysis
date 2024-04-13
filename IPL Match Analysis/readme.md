## Analysis of recent IPL 2024 matches
* Get Scorecard
* Top reddit comments from matchpost
* Topic Analysis on comments
* Emotion detection from Reddit Comments

## App Demo

https://github.com/Akash-R-7/Data-Viz/assets/36988779/b69f20ed-5228-443f-af95-44f66964178b

## Requirements
* One needs to have a Reddit account. Next create Client ID and Client Secret key and store them in a json format to retrieve reddit posts and comments.
* For emotion analysis, following model from huggingface is used: https://huggingface.co/j-hartmann/emotion-english-distilroberta-base. This model has been further weight-quantized to int-8 for faster inferencing.
* Topic Analysis uses simple BOW, but can be implemented with contextual model, like BERTopic (commented code), using the following sentence-transformers embeddings: https://huggingface.co/sentence-transformers/all-mpnet-base-v2.
* Application uses python version 3.10.13 with all the required dependencies listed in requirements.txt.
* To run the app, once the keys and models have been set up, use the following command ```streamlit run main.py```
