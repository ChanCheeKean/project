import os
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import argparse

# download and save model locally
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('-m','--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--epochs', type=int, default=50)
    args, _ = parser.parse_known_args()

    print("Downloading Model")
    model_name = 'cardiffnlp/twitter-roberta-base-emotion'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    text = ['The food is surprisingly good!', 'Yuck! The food is shitty!']
    encoded_input = tokenizer(text, return_tensors='pt', padding=True)
    output = model(**encoded_input)
    scores = softmax(output[0].detach().numpy())
    labels = ['anger', 'joy', 'optimism', 'sadness']
    final_label = [{x : y} for score in scores for x, y in zip(labels, score)]
    print(final_label)

    with open(os.path.join(args.model_dir, 'model.pth'), 'wb') as f:
        torch.save(model.state_dict(), f)
    print('Saved Model in', args.model_dir)

if __name__ == "__main__":
    main()
