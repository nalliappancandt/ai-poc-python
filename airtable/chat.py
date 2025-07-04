import langchain_ollama
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from pydantic import BaseModel

from airtable import services


llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
            Role: You are experienced staffing AI assistant to monitor airtable data and response queries.
            Task: Analyze the user query and call specific tool function and response summarized response based on function response.
            Follow these instructions:-
            If the user query asks for finding profiles based on rating, the call get_profiles_by_rating tool function.
            If the user query asks for finding profiles based on certifications, the call get_profiles_by_certifications tool function.
            If the user query asks for finding profiles based on skills, the call get_profiles_by_skills tool function.
            If the user query asks for finding profiles based on roles, the call get_profiles_by_roles tool function.
    """),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])



## YOUR FUNCTION CALLS HERE:-
tools=[
  services.get_profiles_airtable, 
  services.get_skills_by_name, 
  services.get_roles_by_name, 
  services.get_profiles_by_certifications,
  services.get_profiles_by_rating
]

# Construct the tool calling agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

class Item(BaseModel):
    query: str

async def chat_invoke(item: Item):
    return  agent_executor.invoke({"input": item.query})

#print(agent_executor.invoke({"input": "List out the skills and experience having by Shwetha Talapalli?"}))

#result = agent_executor.invoke(
 #   {
        #"input": "Who has Next.js and Python experience with 4 years and 3 years respectively?"
        #"input":"How much experience does Manikant Upadhyay has on Next.js?"
        #"input":"What was the Manikant Upadhyay Role?"
       # "input": "List the people who have AWS certifications?"
       # "input": "How many people who have AWS certifications and list out the names?"
        #"input": "How many people who have Salesforce certifications and list out the names?"
        #"input": "How many people who have Machine Learning certifications and list out the names?",
        #"input": "List out the skills and experience having by Shwetha Talapalli?"
  #  }
#)



#print(result)