import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


CHROMA_BASE = "vector_db"

COLLECTION_NAME = "video_chat"

EMBED_MODEL = "BAAI/bge-small-en-v1.5"


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL
    )


def create_vector_db(
    transcript_path,
    video_id
):

    with open(
        transcript_path,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1200,

        chunk_overlap=250,

        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " "
        ]
    )

    chunks = splitter.split_text(text)

    docs = [

        Document(
            page_content=chunk
        )

        for chunk in chunks
    ]

    db_path = os.path.join(
        CHROMA_BASE,
        video_id
    )

    Chroma.from_documents(

        documents=docs,

        embedding=get_embeddings(),

        persist_directory=db_path,

        collection_name=COLLECTION_NAME
    )

    print(
        f"Vector DB Created: {video_id}"
    )