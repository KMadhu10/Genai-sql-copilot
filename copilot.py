import os
from dotenv import load_dotenv

from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent

# 1. Load security environment variables
load_dotenv()

# 2. Establish connection to your local PostgreSQL container
db_uri = "postgresql+psycopg2://postgres:admin123@localhost:5432/fde_retail_db"
print("🔌 Linking core driver straight to PostgreSQL database...")
db = SQLDatabase.from_uri(db_uri)

# 3. Instantiate the Native Groq AI Ingestion Engine using the current production model ID
print("🧠 Activating Dedicated ChatGroq Engine...")
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b", # 💡 FIX: Updated to active production model based on official docs!
    temperature=0.0                  # Factual query alignment
)

# 4. Assemble the Intelligent SQL Agent using tool parameters
print("🛡️ Building secure SQL processing pipeline...")
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,               # Shows the step-by-step thinking loop live
    agent_type="tool-calling"   # Modern stable tool calling standard
)

if __name__ == "__main__":
    print("\n🌟 GenAI SQL Copilot Engine Online!")
    test_prompt = "What is the total gross revenue generated from all successful orders?"
    try:
        response = agent_executor.invoke({"input": test_prompt})
        print(response["output"])
    except Exception as e:
        print(f"❌ Execution Failure: {e}")
