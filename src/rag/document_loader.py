from pathlib import Path

from pypdf import PdfReader


def load_documents(documents_path):
    '''Load all PDF policy documents and extract their text.'''

    documents = []

    # Find every PDF inside the policy documents directory.
    pdf_files = sorted(Path(documents_path).glob('*.pdf'))

    for pdf_path in pdf_files:

        reader = PdfReader(pdf_path)

        # Extract text from every page of the PDF.
        text = '\n'.join(
            page.extract_text() or ''
            for page in reader.pages
        ).strip()

        # Only keep documents where text was successfully extracted.
        if text:
            documents.append({
                'text': text,
                'source': pdf_path.name
            })

    return documents