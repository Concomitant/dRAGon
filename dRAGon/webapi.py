from fastapi import FastAPI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
import search
import logging


# Make an LLM object with a temperature
llm = OpenAI(temperature=.7)
# Come up with some random content to bias the LLM.
# This doesn't mean we will have consistent results,
# but if we want to change all the input slightly
# we can by swapping in a different seed.

#seed = "The Hierophant"

government_prompt = PromptTemplate(
  input_variables=["seed"],
  template= "Your seed is {seed}.\nChoose one example of a form of government. Be concise: ",
)

rag_prompt = PromptTemplate(
        input_variables=["question", "source"],
        template = "Answer the following question as it applies to the Cairn RPG by Yochai Gal: {question}\n\
        use these sources {source}. Remember to answer the question to the best of your ability using the sources. If there is no apparent answer,\
        reply instead that you are unable to answer the question.",
        )

rag_chain = LLMChain(llm=llm, prompt=rag_prompt)


app = FastAPI()
@app.get("/items/{question}")
def read_item(question:str):
    source =(search.search_rulebook(question))
    import pdb; pdb.set_trace()
    context = {"question": question, "source": source}
    return {"answer":rag_chain(context)["text"]}

