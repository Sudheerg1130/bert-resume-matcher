from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import torch

text = "I am a java Developer"

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def get_embedding(text):
    encoded = tokenizer(
        text,
        return_tensors="pt"
    )
    
    with torch.no_grad():
       output = model(**encoded)

    cls_vector = output.last_hidden_state[:, 0, :]

    return cls_vector

sentence1 = "I am a Java developer"
sentence2 = "I am a Python developer"

embedding1 = get_embedding(sentence1)
embedding2 = get_embedding(sentence2)

print("Embedding 1 shape:", embedding1.shape)
print("Embedding 2 shape:", embedding2.shape)

similarity = cosine_similarity(
    embedding1.numpy(),
    embedding2.numpy()
)
print("Cosine Similarity:", similarity)