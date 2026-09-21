import os
from dotenv import load_dotenv
import streamlit as st # Added to handle cloud secrets securely

from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent

# 1. Load local env variables if present
load_dotenv()

# 2. Production-Grade Credential Routing (Cloud vs Local)
if "DATABASE_URL" in st.secrets:
    # Running live on Streamlit Cloud
    db_uri = st.secrets["DATABASE_URL"]
else:
    # Running locally on your laptop
    db_uri = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin123@localhost:5432/fde_retail_db")

if "GROQ_API_KEY" in st.secrets:
    groq_key = st.secrets["GROQ_API_KEY"]
else:
    groq_key = os.getenv("GROQ_API_KEY")

# 💡 FDE Guardrail: SQLAlchemy requires 'postgresql+psycopg2://' to route properly
if db_uri and db_uri.startswith("postgresql://"):
    db_uri = db_uri.replace("postgresql://", "postgresql+psycopg2://", 1)

print("🔌 Routing core database configuration pool...")
db = SQLDatabase.from_uri(db_uri)

# 3. Instantiate the AI Ingestion Engine
print("🧠 Activating Dedicated ChatGroq Engine...")
llm = ChatGroq(
    groq_api_key=groq_key,
    model_name="openai/gpt-oss-120b", # Your verified production model ID
    temperature=0.0                  
)

# 4. Assemble the Intelligent SQL Agent
print("🛡️ Building secure SQL processing pipeline...")
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,               
    agent_type="tool-calling"   
)
