from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from duckduckgo_search import ddg

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def search_and_answer(query):
    results = ddg(query, max_results=3)
    context = " ".join([r.get("body", "") or r.get("snippet", "") for r in results])
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=128)
    return tokenizer.decode(output[0], skip_special_tokens=True)
