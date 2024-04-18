from transformers import pipeline
pipe = pipeline("text-classification", model="roberta-base-openai-detector")
print(pipe("Hello world! Is this content AI-generated?"))  # [{'label': 'Real', 'score': 0.8036582469940186}]
