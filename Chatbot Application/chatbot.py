import torch
import json
from training_model import NeuralNet
from nltk_resources import tokenize, bag_of_words
import random

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json') as f:
    intents = json.load(f)

FILENAME = 'data.pth'
data = torch.load(FILENAME)

input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']
model_state = data['model_state']
all_words = data['all_words']
tags = data['tags']

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def get_response(msg):
    tokenized_prompt = tokenize(msg)
    bag = bag_of_words(tokenized_prompt, all_words)
    X = bag.reshape(1, bag.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    y, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:
                return random.choice(intent["responses"])

    return "Unable to understand..."

