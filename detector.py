from transformers import pipeline
import  argparse

def generativeTextDetector(candidate_text):

    pipe = pipeline("text-classification", model="roberta-base-openai-detector")
    print(pipe("Hello world! Is this content AI-generated?"))  # [{'label': 'Real', 'score': 0.8036582469940186}]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Classify generative vs real text')
    parser.argparse('candidate_text', type=str, help='Enter the text to be candidate text to be classified')
    args = parser.parser_args()

    candidate_text = args.candidate_text

    generativeTextDetector(candidate_text)