from fastapi import FastAPI
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel

import search
from config import config


class Query(BaseModel):
    text: str

rpg_title = config["rpg_title"]
rpg_author = config["rpg_author"]

# Make an LLM object with a temperature
llm = OpenAI(temperature=0.7)

rag_prompt = PromptTemplate(
    input_variables=["question", "source"],
    template=(
        f"""Examine the following snippets from {rpg_title} RPG. Following the snippets will be a question about the content\n
        If the answer to the question is found in the text answer accordingly. Otherwise reply that the answer is not found 
        in the provided text, and suggest a modified version of the question that might yield better results when provided 
        to a search engine.
        \n
        {{source}}\n
        {{question}}\n
        \n
        Remember to  provide answers that are found in the provided snippet from {rpg_title}. If the content concerns a different 
        subject than the question, answer in the negative and suggest an alternative query to answer the user's question.
        
        Examine the above snippets from {rpg_title} RPG. Following the snippets will be a question about the content\n
        If the answer to the question is found in the text answer accordingly. Otherwise reply that the answer is not found 
        in the provided text, and suggest a modified version of the question that might yield better results when provided 
        to a search engine.

        Reply below:\n\n"""
    ),
)

# Create a RunnableSequence, equivalent to rag_prompt.pipe(llm), or RunnableSequence(first=rag_prompt, last=llm)
rag_chain = rag_prompt | llm


app = FastAPI()


@app.post("/api/query")
async def read_item(query: Query):
    source = search.search_rulebook(query.text)
    context = {"question": query.text, "source": source}
    return {"answer": rag_chain.invoke(context)}
