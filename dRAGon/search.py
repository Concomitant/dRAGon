import whoosh
import os.path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from whoosh.index import create_in
from whoosh.fields import * # TODO: Get rid of this for the love of god and all attendant bodhisattvas
from whoosh.qparser import QueryParser
from whoosh.index import open_dir


## Define search method

def search_rulebook(query=""):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query)
        results = searcher.search(query)
        return results[0]




## Initialize chunkers

text_splitter = RecursiveCharacterTextSplitter(
        # Chunk params
        chunk_size=300,
        chunk_overlap=50,
        length_function=len, #We are counting characters, not tokens
        is_separator_regex=False,
)





## Index Content


#schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content = TEXT)
schema = Schema(id_=ID(stored=True), content = TEXT(stored=True))

# create index if it does not exist
if not os.path.exists("indexdir"):
    # Load data
    with open("../../cairn-markdown.md") as file:
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


#with ix.searcher() as searcher:
#    query = QueryParser("content", ix.schema).parse("magic")
#    results = searcher.search(query)
#    print(results[0])


