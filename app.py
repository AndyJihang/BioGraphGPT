import os
import json
import pandas as pd
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

kg_triples = pd.read_csv("/Users/jihangbc.edu/Downloads/kg_triples.csv")


def parse_question_with_llm(question: str) -> dict:
    prompt = f"""
You are a biomedical assistant. Extract the user's intent as JSON:
- query_type: one of ["drug_to_gene","drug_to_disease","gene_to_disease","disease_to_drug"]
- drug, gene, disease: strings or null

Example 1:
Q: What genes does Gefitinib affect?
→ {{"query_type":"drug_to_gene","drug":"Gefitinib","gene":null,"disease":null}}

Example 2:
Q: Which drugs affect genes associated with lung cancer?
→ {{"query_type":"disease_to_drug","drug":null,"gene":null,"disease":"lung cancer"}}

Now:
Q: {question}
→
"""
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )
    text = resp.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # fallback for null→None
        fixed = text.replace("null","null")  # keep null, json.loads will handle it
        return json.loads(fixed)


def query_kg(intent: dict, kg_df: pd.DataFrame) -> pd.DataFrame:
    qt = intent.get("query_type")
    drug = intent.get("drug") or ""
    gene = intent.get("gene") or ""
    disease = intent.get("disease") or ""

    if qt == "drug_to_gene":
        return kg_df[
            (kg_df.source.str.lower() == drug.lower()) &
            (kg_df.relation.str.contains("affects|increases|decreases", case=False))
        ]

    if qt == "drug_to_disease":
        return kg_df[
            (kg_df.source.str.lower() == drug.lower()) &
            (kg_df.relation.str.startswith("treats"))
        ]

    if qt == "gene_to_disease":
        return kg_df[
            (kg_df.source.str.lower() == gene.lower()) &
            (kg_df.relation == "associated_with")
        ]

    if qt == "disease_to_drug":
        # 1) find all genes associated with the disease
        assoc = kg_df[
            (kg_df.relation == "associated_with") &
            (kg_df.target.str.lower() == disease.lower())
        ]["source"].unique().tolist()

        # 2) find all drugs affecting those genes
        return kg_df[
            (kg_df.relation.str.contains("affects|increases|decreases", case=False)) &
            (kg_df.target.str.lower().isin([g.lower() for g in assoc]))
        ]

    return pd.DataFrame()


def generate_answer(question: str, df: pd.DataFrame) -> str:
    if df.empty:
        return "No relevant information found in the knowledge graph."

    sample = df.head(10).to_dict(orient="records")
    facts = "\n".join(f"{r['source']} --[{r['relation']}]--> {r['target']}" for r in sample)

    prompt = f"""
You are a helpful biomedical assistant. The user asked:
"{question}"

Here are some KG facts:
{facts}

Write a concise English answer based on these facts.
"""
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5
    )
    return resp.choices[0].message.content.strip()


def answer_user_question(question: str) -> str:
    intent = parse_question_with_llm(question)
    print("🔍 Parsed intent:", intent)
    results = query_kg(intent, kg_triples)
    return generate_answer(question, results)


if __name__ == "__main__":
    q = input("💬 Ask a biomedical question: ")
    print("\n🧠 Answer:\n", answer_user_question(q))
