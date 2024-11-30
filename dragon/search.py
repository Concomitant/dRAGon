from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

from config import config


## Define search method


def search_rulebook(query_text=""):
    print("Begin search")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_text)
        results = [i.fields() for i in searcher.search(query)]
    # TODO: Remove
    print('RESULTS:', results)
    if results == []:
        results = ['NO RESULTS FOUND']
    return results


## Initialize chunkers

text_splitter = RecursiveCharacterTextSplitter(
    # Chunk params
    chunk_size=300,
    chunk_overlap=50,
    length_function=len,  # We are counting characters, not tokens
    is_separator_regex=False,
)

## Index Content

schema = Schema(id_=ID(stored=True), content=TEXT(stored=True))

# create index if it does not exist
if not Path(config["index_directory"]).exists():
    # Load data
    with Path(config["rulebook_path"]).open() as file:
        rulebook = file.read()
    # Chunk

    chunks = text_splitter.split_text(rulebook)

    Path(config["index_directory"]).mkdir()
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    # Add chunks to index
    for chunk in chunks:
        writer.add_document(id_=str(hash(chunk)), content=chunk)
    writer.commit()
else:
    # Open already created index
    ix = open_dir("indexdir")
