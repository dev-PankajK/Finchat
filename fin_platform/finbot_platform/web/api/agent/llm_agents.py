from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from finbot_platform.web.api.agent import agent_tools
from langchain.chat_models import ChatOpenAI
from finbot_platform.settings import settings

def lang_multitool_agent(user_id):
    llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0,api_key=settings.openai_api_key)
    tools = [agent_tools.sql_agent,agent_tools.info_agent,agent_tools.data_saver]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""you are the master agent of bank,Named FinBot Agent, responsible to answer any kinds of banking related queries of users
                right now you are solving queries of a user whose user_id is {user_id}. You must run the data_saver function after getting answer of user question
                you have 3 tools to use - 
                1. query_generator - this is the function to generate sql queries just provide user's message and user_id in the function and it will generate sql query for you, this function is to get user specific details like balance, transaction etc from sql database
                2. sql_agent - this function is to run sql queries just provide sql query you got from query_generator and user_id in the arguments
                3. info_agent - it's a function to get answers about general questions you should respond this answer to user instead of crearting your own response
                4. data_saver - function to save the user question and your response with  metadata this function take below arguments
                    query - user's question
                    query_type - one of two types of queris account_info or information
                    agent_type - whichever tool you use to get answer sql_agent or info_agent
                    query_info - the sql query you got using sql_agent but provide it without user_id like 'SELECT balance FROM users  WHERE user_id =' , it's very important to remove user_id from query
                    You must Invoke this function once you find the response for the user input""",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm_with_tools = llm.bind(
        functions=[format_tool_to_openai_function(t) for t in tools]
    )

    agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor