from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

print("Import successful, no conflicts!")
