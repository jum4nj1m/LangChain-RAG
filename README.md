# Medium Analyzer RAG

A Python Retrieval-Augmented Generation (RAG) example. It uses OpenAI for chat completions and embeddings, and Pinecone to store and retrieve document vectors. Retrieved passages are supplied to the chat model as context for answering questions.

## Requirements

- Python 3.11 or newer
- An OpenAI API key with access to the selected chat and embedding models
- A Pinecone account, API key, and index
- [`uv`](https://docs.astral.sh/uv/) (recommended) or another Python package manager

## Setup

Install dependencies from the project configuration:

```powershell
uv sync
```

Create a `.env` file in the project root with your credentials and Pinecone index name:

```dotenv
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
INDEX_NAME=your_pinecone_index_name
```

Keep `.env` private; do not commit API keys or add them directly to source code. The scripts use `python-dotenv` to load environment variables.

## Ingest documents

Before ingestion, edit the `file_path` in `ingestion.py` to the location of the document you want to index. It currently contains a machine-specific path, so it will not work on another computer without changing it.

Run ingestion from the project root:

```powershell
uv run python ingestion.py
```

The script loads and splits the source document, creates embeddings with `OpenAIEmbeddings`, and writes the chunks to the Pinecone index named by `INDEX_NAME`.

## Ask questions

Run the application:

```powershell
uv run python main.py
```

`main.py` currently includes a sample question. Change the `query` value to ask about your ingested document. The app embeds the query, retrieves the three most relevant Pinecone chunks, and uses the OpenAI chat model to answer from that context.

## Models and Pinecone index

Both ingestion and query-time retrieval use OpenAI embeddings. They must use the same embedding model, and the Pinecone index's vector dimension must match that model's output. If you change the embedding model or its dimensions, recreate or clear the Pinecone index and ingest the documents again.

The chat model is set in `main.py` in the `ChatOpenAI` initialization. Ensure the configured model name is available to your OpenAI account.

## Troubleshooting

- **Missing credentials:** Ensure `.env` is in the project root and contains a valid `OPENAI_API_KEY`. Run the scripts from the project root so `load_dotenv()` can find it.
- **Pinecone authentication or index errors:** Check `PINECONE_API_KEY`, `INDEX_NAME`, and that the index exists and has the expected embedding dimension.
- **Embedding dimension or retrieval errors:** Use the same embedding model for ingestion and queries. Recreate the index and re-ingest after changing embedding models or dimensions.
- **A key was exposed:** Revoke it and create a replacement. Never share or commit API keys.

