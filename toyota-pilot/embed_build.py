# embed_build.py
import os, json, requests

API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise SystemExit("Set OPENROUTER_API_KEY first: export OPENROUTER_API_KEY='sk-or-...'")

EMBED_URL = "https://openrouter.ai/api/v1/embeddings"
MODEL = "openai/text-embedding-3-small"   # pick an embedding-capable model from your OpenRouter account

docs = json.load(open("data/trim_docs.json"))
out = {}

for row in docs:
    text = row["doc"]
    print("Embedding", row["id"])
    payload = {
        "model": MODEL,
        "input": text
    }
    r = requests.post(
        EMBED_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    if r.status_code != 200:
        print("Embedding failed:", r.status_code, r.text)
        raise SystemExit("Embedding request failed")
    data = r.json()
    # OpenRouter uses OpenAI-like response format
    embedding = data["data"][0]["embedding"]
    out[row["id"]] = embedding

with open("data/trim_vectors.json", "w") as f:
    json.dump(out, f)

print(f"✅ Wrote vectors for {len(out)} trims to data/trim_vectors.json")
