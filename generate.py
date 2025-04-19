# ai_core/generate.py

import torch
from model import GPTMini
import torch.nn.functional as F

def load_model():
    checkpoint = torch.load("ai_core/model.pth", map_location=torch.device('cpu'))

    char2idx = checkpoint["char2idx"]
    idx2char = checkpoint["idx2char"]
    vocab_size = len(char2idx)

    model = GPTMini(vocab_size)
    model.load_state_dict(checkpoint["model"])
    model.eval()

    return model, char2idx, idx2char

def generate_text(prompt, max_length=200):
    model, char2idx, idx2char = load_model()

    input_ids = [char2idx.get(ch, 0) for ch in prompt]
    input_tensor = torch.tensor([input_ids], dtype=torch.long)

    for _ in range(max_length):
        with torch.no_grad():
            output = model(input_tensor)
            next_token_logits = output[0, -1, :]
            probs = F.softmax(next_token_logits, dim=0).numpy()
            next_token = torch.tensor([int(torch.multinomial(torch.tensor(probs), 1))])
            input_tensor = torch.cat([input_tensor, next_token.unsqueeze(0)], dim=1)

    result = ''.join([idx2char[idx.item()] for idx in input_tensor[0]])
    return result

if __name__ == "__main__":
    prompt = input("Rayhan Boss: ")
    response = generate_text(prompt)
    print("\nAI: " + response)
