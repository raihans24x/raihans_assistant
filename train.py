# ai_core/train.py

import torch
import torch.nn as nn
import torch.optim as optim
from model import GPTMini
from torch.utils.data import Dataset, DataLoader

# Simple tokenizer
class CharDataset(Dataset):
    def __init__(self, text, block_size=64):
        chars = sorted(list(set(text)))
        self.char2idx = {ch: i for i, ch in enumerate(chars)}
        self.idx2char = {i: ch for ch, i in self.char2idx.items()}
        self.vocab_size = len(chars)
        self.block_size = block_size
        self.data = text

    def __len__(self):
        return len(self.data) - self.block_size

    def __getitem__(self, idx):
        chunk = self.data[idx:idx + self.block_size + 1]
        x = torch.tensor([self.char2idx[c] for c in chunk[:-1]], dtype=torch.long)
        y = torch.tensor([self.char2idx[c] for c in chunk[1:]], dtype=torch.long)
        return x, y

def train_model():
    with open("ai_core/data.txt", "r", encoding="utf-8") as f:
        text = f.read()

    dataset = CharDataset(text)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = GPTMini(vocab_size=dataset.vocab_size).to(device)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(10):  # Train for 10 epochs
        total_loss = 0
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            output = model(x)
            loss = criterion(output.view(-1, output.size(-1)), y.view(-1))
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

    torch.save({
        "model": model.state_dict(),
        "char2idx": dataset.char2idx,
        "idx2char": dataset.idx2char
    }, "ai_core/model.pth")

if __name__ == "__main__":
    train_model()
