from langchain.agents import tool
import mysql.connector
from finbot_platform.settings import settings
from openai import OpenAI
from finbot_platform.db.sql_connection import Connection

client = OpenAI(api_key=settings.openai_api_key)


@tool
def data_saver(query: str, query_type: str, agent_type: str, query_info: str):
    """this is a function to save users chat in the database and returns nothing
    it takes all the arguments in string format"""

    response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    text_embeddings = [(query, response.data[0].embedding)]
    metadata={
        "query_type": query_type,
        "agent_type": agent_type,
        "query_info": query_info
    }
    print(f"INFO: Metadata to save:{metadata}")

@tool
def sql_agent(sql_query: str):
    """function to get data using sql queries as input"""
    try:
        with Connection(settings.db_config) as db:
            results = db.fetch(sql_query)
        return results
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return None

@tool
def info_agent(query: str):
    """function to retrieve relatable information from vector database to answer user's query"""
    return "Yes info_agent too is working.."

# @tool
# def query_generator(query, user_id):
#     """this is the function to generate sql queries to fetch data"""
#     chain = create_sql_query_chain(llm, sql_db)
#     response = chain.invoke({"question": f"{query} and user_id is {user_id}"})
#     return response
