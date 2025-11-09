# recommend.py
import os, json, re, numpy as np, requests

def to_json(s: str):
    s = s.strip()
    # remove ```json ... ``` fences if present
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.IGNORECASE | re.MULTILINE)
    s = s.strip()
    # if extra text still surrounds the JSON, grab the first {...} or [...]
    if not (s.startswith("{") or s.startswith("[")):
        m = re.search(r"(\{.*\}|\[.*\])", s, flags=re.DOTALL)
        if m:
            s = m.group(1)
    return json.loads(s)


from sklearn.metrics.pairwise import cosine_similarity

# ---------- config ----------
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")
if not OPENROUTER_KEY:
    raise SystemExit("Set OPENROUTER_API_KEY first")

CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
EMBED_MODEL = "openai/text-embedding-3-small"   # must match your vectors
PARSER_MODEL = "openai/gpt-4o-mini"             # pick a chat model available to you on OpenRouter
FINAL_MODEL  = "openai/gpt-4o-mini"             # you can use a stronger model if available

# ---------- data ----------
VEHICLES = json.load(open("data/vehicles.json"))
ONTOLOGY = json.load(open("data/feature_ontology.json"))
TRIM_VECS = json.load(open("data/trim_vectors.json"))

BY_ID = {v["id"]: v for v in VEHICLES}
MAT_IDS = list(TRIM_VECS.keys())
MAT = np.array([TRIM_VECS[i] for i in MAT_IDS], dtype=np.float32)

def call_llm(system, user, model=PARSER_MODEL, temperature=0.1):
    payload = {
        "model": model,
        "messages": [
            {"role":"system","content": system},
            {"role":"user","content": user}
        ],
        "temperature": temperature
    }
    r = requests.post(
        CHAT_URL,
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type":"application/json"},
        json=payload
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def apply_ontology(phrases):
    out = []
    for p in phrases:
        key = ONTOLOGY.get(p.lower().strip())
        out.append(key if key else p.lower().strip())
    return sorted(list(set([x for x in out if x])))

EXTRACT_SYSTEM = (
    "You extract car-shopping preferences as strict JSON. "
    "Map obvious synonyms to canonical feature keys (e.g., 'seat warmers' -> 'heated_front_seats'). "
    "If unsure, omit. Output ONLY valid JSON."
)

EXTRACT_USER_TMPL = """
User answers (free text):
Purpose: {purpose}
Location: {location}
Appearance: {appearance}
Features: {features}
Budget: {budget}

Return JSON with exactly these keys:
{{
  "purpose": [],
  "location_tags": [],
  "style_vibe": [],
  "must_have": [],
  "nice_to_have": [],
  "powertrain_pref": "hybrid|gas|phev|ev|no-strong-preference",
  "budget_total_usd": {{ "target": 0, "flex_pct": 10 }},
  "notes": ""
}}
"""

def profile_to_text(p):
    parts = []
    if p.get("purpose"): parts.append("Purpose: " + ", ".join(p["purpose"]))
    if p.get("location_tags"): parts.append("Location: " + ", ".join(p["location_tags"]))
    if p.get("style_vibe"): parts.append("Style: " + ", ".join(p["style_vibe"]))
    if p.get("must_have"): parts.append("Must-haves: " + ", ".join(p["must_have"]))
    if p.get("nice_to_have"): parts.append("Nice-to-have: " + ", ".join(p["nice_to_have"]))
    if p.get("powertrain_pref"): parts.append("Powertrain: " + p["powertrain_pref"])
    return ". ".join(parts)

def can_satisfy(trim, musts):
    base = set(trim.get("features", []))
    adds = set()
    for p in trim.get("packages", []):
        for a in p.get("adds", []):
            adds.add(a)
    for m in musts:
        if m not in base and m not in adds:
            return False
    return True

def suggest_packages(trim, musts):
    rec = []
    base = set(trim.get("features", []))
    for m in musts:
        if m in base: 
            continue
        for p in trim.get("packages", []):
            if m in p.get("adds", []):
                rec.append(p["name"])
    return sorted(list(set(rec)))

# ---------- Pilot input ----------
user_free = {
    "purpose":   "family and weekend road trips",
    "location":  "Dallas suburbs, mostly highway, sometimes heavy rain",
    "appearance":"sleek and modern",
    "features":  "heated seats, blind spot",
    "budget":    "around 40k"
}

# A) Extract structured prefs
extract_user = EXTRACT_USER_TMPL.format(**user_free)
raw = call_llm(PARSER_MODEL, extract_user, model=PARSER_MODEL, temperature=0.1)
try:
    prof = to_json(raw)
except Exception:
    print("Extraction failed. Raw:\n", raw)
    raise

# B) Normalize feature names
prof["must_have"] = apply_ontology(prof.get("must_have", []))
prof["nice_to_have"] = apply_ontology(prof.get("nice_to_have", []))

# C) Rank by embeddings (we already built vectors with embed_build.py)
u_text = profile_to_text(prof)
# Reuse the same embedding model you used earlier -> vectors already on disk

# Compute similarity against MAT
from numpy.linalg import norm
def cosine(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# Get user embedding via OpenRouter embeddings (one-off call)
EMBED_URL = "https://openrouter.ai/api/v1/embeddings"
r = requests.post(
    EMBED_URL,
    headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type":"application/json"},
    json={"model": EMBED_MODEL, "input": u_text}
)
r.raise_for_status()
u_vec = np.array(r.json()["data"][0]["embedding"], dtype=np.float32)

sims = MAT @ u_vec / (np.linalg.norm(MAT, axis=1) * np.linalg.norm(u_vec))
top_idx = np.argsort(-sims)[:10]

candidates = []
for i in top_idx:
    tid = MAT_IDS[i]
    trim = BY_ID[tid]
    if not can_satisfy(trim, prof["must_have"]):
        continue
    candidates.append({
        "id": trim["id"],
        "model": trim["model"],
        "year": trim["year"],
        "trim": trim["trim"],
        "score_vector": float(sims[i]),
        "suggested_packages": suggest_packages(trim, prof["must_have"]),
        "detail_url": trim.get("detail_url",""),
        "style_vibe": trim.get("style_vibe", []),
        "features": trim.get("features", []),
        "colors": trim.get("colors", [])
    })

# D) Finalize with grounded LLM
FINALIZE_SYSTEM = (
    "You are a grounded Toyota recommender. You receive a user profile and candidate trims "
    "with their true features/packages. Recommend ONLY from candidates. "
    "If a must-have is missing but available via a listed package, include that package in recommended_customizations. "
    "Do not invent features or packages. Return valid JSON."
)

FINALIZE_USER = f"""
User profile:
{json.dumps(prof, ensure_ascii=False)}

Candidates:
{json.dumps(candidates[:10], ensure_ascii=False)}

Return JSON:
{{
  "top_5": [
    {{
      "id": "trim-id",
      "model": "RAV4",
      "year": 2025,
      "trim": "Hybrid XLE",
      "fit_score": 0,
      "reasons": ["...","..."],
      "recommended_customizations": ["Weather Package","Midnight Black","Panoramic Roof"]
    }}
  ],
  "others": [{{"id":"...", "fit_score":80}}]
}}
"""

final_raw = call_llm(FINALIZE_SYSTEM, FINALIZE_USER, model=FINAL_MODEL, temperature=0.2)
try:
    result = json.loads(final_raw)
except Exception:
    print("Finalize failed. Raw:\n", final_raw)
    raise

print("\n=== USER PROFILE (normalized) ===")
print(json.dumps(prof, indent=2))
print("\n=== RECOMMENDATIONS ===")
print(json.dumps(result, indent=2))
