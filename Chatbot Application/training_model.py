import json
import torch
from nltk_resources import tokenize, stem, bag_of_words
import numpy as np
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open('intents.json') as f:
    intents = json.load(f)

all_words, tags, xy = [], [], []                     # xy = x: patterns and y: labels --> [(x, y)]

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        tokenized_sent = tokenize(pattern)
        xy.append((tokenized_sent, tag))
        all_words.extend(tokenized_sent)

ignore_words = ['?', '!', '.', ',', ';']
stemmed_words = [stem(word) for word in all_words if word not in ignore_words]

all_words = sorted(set(stemmed_words))
tags = sorted(tags)

X_train, Y_train = [], []

for t_sent, tag in xy:
    bag = bag_of_words(t_sent, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    Y_train.append(label)

X_train = np.array(X_train)
Y_train = np.array(Y_train)

# Hyper parameters
batch_size = 14
input_size = len(X_train[0])
hidden_size = 14
output_size = len(tags)
learning_rate = 0.001
num_of_epochs = 1000


class ChatBotDataset(Dataset):
    def __init__(self, X, Y):
        self.n_samples = len(X)
        self.x_data = torch.from_numpy(X).float()
        self.y_data = torch.from_numpy(Y).long()

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


chatbot = ChatBotDataset(X_train, Y_train)
chatbotLoader = DataLoader(dataset=chatbot, batch_size=batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_of_epochs):
    for (words, labels) in chatbotLoader:
        words = words.to(device)
        labels = labels.to(device)

        # forward
        outputs = model(words)
        loss = criterion(outputs, labels)

        # backward and optimizer
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

data = {
    "model_state": model.state_dict(),
    "input_size":input_size,
    "hidden_size":hidden_size,
    "output_size":output_size,
    "all_words":all_words,
    "tags":tags,
}

FILENAME = 'data.pth'
torch.save(data, FILENAME)
