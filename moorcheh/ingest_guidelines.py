from moorcheh.client import moorcheh_client
import glob

GUIDELINE_PATH = "firstaid_guidelines"

def ingest_first_aid_guidelines():
    """
    Ingests a set of general first aid and mental health first aid guidelines
    into a predetermined Moorcheh namespace for general medical assistance.
    """
    docs = []
    metadatas = []
    
    for filepath in glob.glob(f"{GUIDELINE_PATH}/*.txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().strip()
            docs.append(text)
            metadatas.append({"source": filepath.split("/")[-1]})

    moorcheh_client.documents.add(
        namespace="first_aid_guidelines",
        documents=docs,
        metadata=metadatas
    )

if __name__ == "__main__":
    ingest_first_aid_guidelines()
