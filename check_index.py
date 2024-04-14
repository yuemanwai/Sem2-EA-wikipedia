from whoosh.index import open_dir
import os

index_dir = os.path.join(os.getcwd(), 'index_dir') 

index = open_dir(index_dir)

with index.searcher() as searcher:
    reader = searcher.reader()

    print(f"Total documents in index: {reader.doc_count()}")

    for doc_num in range(reader.doc_count()):
        stored_fields = reader.stored_fields(doc_num)
        print(f"Document ID: {doc_num}, Stored Fields: {stored_fields}")