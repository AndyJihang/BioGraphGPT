🧬 BioGraphGPT: Biomedical Q&A over Knowledge Graph

BioGraphGPT is a lightweight Streamlit app that enables natural language question answering over a biomedical knowledge graph. Users can ask questions about drugs, genes, and diseases—such as “What genes does Gefitinib affect?”—and receive concise answers based on curated biomedical relationships, interpreted and formatted using GPT-4.

🚀 Features

 - 🧠 Natural language understanding with GPT-4
 - 🔍 Query biomedical knowledge graphs with ease
 - 🧬 Supports drug-to-gene, gene-to-disease, drug-to-disease, and disease-to-drug queries
 - 🖥️ User-friendly Streamlit interface

📁 File Structure

OpenAIData-App/

│
├── app.py                   # Main Streamlit application
├── kg_triples.parquet       # Biomedical knowledge graph data
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── secrets.toml         # API key (OpenAI)
├── README.md                # This file
🔧 Setup & Run Locally
Clone the repo
git clone https://github.com/AndyJihang/OpenAIData-App.git
cd OpenAIData-App
Install dependencies
pip install -r requirements.txt
Add OpenAI API key
Create a file .streamlit/secrets.toml with:
OPENAI_API_KEY = "your_openai_api_key_here"
Run the app
streamlit run app.py
💡 Example Questions
What genes does Gefitinib affect?
Which drugs treat lung cancer?
What diseases are associated with BRCA1?
📜 License
MIT License
