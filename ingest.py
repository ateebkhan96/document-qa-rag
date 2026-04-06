import pymupdf
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def pdf_to_chunk(pdf_path):

    doc = pymupdf.open(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )


    def clean_text(text):

        text = re.sub("[\xa0\u200b|\n]", " ", text)

        lines = text.split()

        lines = [line for line in lines if re.search(r'[a-zA-Z0-9]', line)]  # filter
        return " ".join(lines)

    final_dict = []

    ch_id = 0
    for page in doc:

        text = page.get_text()
        text = clean_text(text)
        page_chunks = splitter.split_text(text)

        for i, chunk in enumerate(page_chunks):
            values = {"text": chunk, "source": pdf_path, "page": page.number + 1, "chunk_id": ch_id}

            final_dict.append(values)
            ch_id += 1

    doc.close()

    return final_dict