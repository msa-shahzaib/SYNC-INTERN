import torch.nn as nn


class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_of_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_of_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out_layer1 = self.l1(x)
        out_layer1 = self.relu(out_layer1)
        out_layer2 = self.l2(out_layer1)
        out_layer2 = self.relu(out_layer2)
        out_layer3 = self.l3(out_layer2)
        return out_layer3


