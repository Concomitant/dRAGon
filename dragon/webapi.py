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
        f"Answer the following question as it applies to the {rpg_title} RPG by {rpg_author}: {{question}}\n"
        f"use these sources {{source}}. Remember to answer the question to the best of your ability using the sources."
        f"If there is no apparent answer, reply instead that you are unable to answer the question."
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
