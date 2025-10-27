kuzu-load-data:
    uv run marimo edit kuzu-load-data.py

kuzu-explorer:
    podman run --rm -p 8000:8000 \
    -v ./data/movielens/kuzu-movielens.kuzu:/database \
    kuzudb/explorer:latest

    podman run -p 8000:8000 \
           -v ./data/movielens:/database \
           -e KUZU_FILE=database.kz \
           --rm kuzudb/explorer:latest