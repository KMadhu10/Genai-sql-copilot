import os
from dotenv import load_dotenv
import streamlit as st

from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent

# 💡 NEW FIX: Import the standard SQLAlchemy core driver to configure pooling options
from sqlalchemy import create_engine

# 1. Load local environment configuration keys safely
load_dotenv()

# 2. Production Credential Routing (Cloud vs Local Workspace)
if "DATABASE_URL" in st.secrets:
    db_uri = st.secrets["DATABASE_URL"]
else:
    db_uri = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin123@localhost:5432/fde_retail_db")

if "GROQ_API_KEY" in st.secrets:
    groq_key = st.secrets["GROQ_API_KEY"]
else:
    groq_key = os.getenv("GROQ_API_KEY")

# Ensure structural formatting string prefixes are exact for SQLAlchemy Core
if db_uri and db_uri.startswith("postgresql://"):
    db_uri = db_uri.replace("postgresql://", "postgresql+psycopg2://", 1)

print("🔌 Building self-healing connection pooling architecture...")

# 💡 THE ARCHITECTURAL GUARDRAIL: We build an explicit engine configured with pool safeguards
engine = create_engine(
    db_uri,
    pool_pre_ping=True,      # Pings the DB first; if dead, it automatically reconstructs the connection!
    pool_recycle=1800        # Automatically purges and recycles connections older than 30 minutes
)

# Connect LangChain straight to our robust engine mapping layout
db = SQLDatabase(engine)

# 3. Instantiate the Groq Inference AI Processing Unit
print("🧠 Activating Dedicated ChatGroq Processing Pipeline...")
llm = ChatGroq(
    groq_api_key=groq_key,
    model_name="openai/gpt-oss-120b",
    temperature=0.0                  
)

# 4. Assemble the Intelligent SQL Agent Framework
print("🛡️ Deploying secure tool-calling execution blocks...")
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,               
    agent_type="tool-calling"   
)
