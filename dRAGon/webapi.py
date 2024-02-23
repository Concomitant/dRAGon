from fastapi import FastAPI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI


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

government_chain = LLMChain(llm=llm, prompt=government_prompt)

app = FastAPI()

@app.get("/items/{seed}")
def read_item(seed:str):
    return {"seed":government_chain(seed)["text"]}

