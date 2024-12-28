from anki.collection import Delimiter, ImportCsvRequest
from aqt import mw


def import_flashcards_from_file(file_path: str) -> None:
    try:
        print(f"Importing flashcards from file: {file_path}")

        metadata = mw.col.get_csv_metadata(path=file_path, delimiter=Delimiter.COMMA)
        print(f"Metadata retrieved: {metadata}")

        request = ImportCsvRequest(
            path=file_path,
            metadata=metadata,
        )
        print(f"Request created: {request}")

        response = mw.col.import_csv(request)
        print(f"Import response: {response}")

        print(f"Found notes: {response.log.found_notes}")
        print(f"Updated notes: {list(response.log.updated)}")
        print(f"New notes: {list(response.log.new)}")

    except Exception as e:
        print(f"Error during flashcard import: {e!s}")
