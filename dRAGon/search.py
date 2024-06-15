import whoosh
import os.path
import yaml
from langchain.text_splitter import RecursiveCharacterTextSplitter
from whoosh.index import create_in
from whoosh.fields import * # TODO: Get rid of this for the love of god and all attendant bodhisattvas
from whoosh.qparser import QueryParser
from whoosh.index import open_dir

## Get Config

with open("config/config.yml") as cf:
    config = yaml.safe_load(cf)


## Define search method

def search_rulebook(query_text=""):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_text)
        results = [i.fields() for i in searcher.search(query)]
    return results



## Initialize chunkers

text_splitter = RecursiveCharacterTextSplitter(
        # Chunk params
        chunk_size=300,
        chunk_overlap=50,
        length_function=len, #We are counting characters, not tokens
        is_separator_regex=False,
)

## Index Content

schema = Schema(id_=ID(stored=True), content = TEXT(stored=True))

# create index if it does not exist
if not os.path.exists("indexdir"):
    # Load data
    with open("../../"+config['rulebook']) as file:
        rulebook = file.read()
    # Chunk

    chunks = text_splitter.split_text(rulebook)

    os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    # Add chunks to index
    for chunk in chunks:
        writer.add_document(id_=str(hash(chunk)), content=chunk)
    writer.commit()
else:
    # Open already created index
    ix = open_dir("indexdir")
