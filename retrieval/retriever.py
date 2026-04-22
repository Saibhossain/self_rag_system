
def retrieve_with_filter(retriever, query, metadata_filter=None):
    docs = retriever.invoke(query)

    if metadata_filter:
        docs = [
            d for d in docs
            if all(d.metadata.get(k) == v for k, v in metadata_filter.items())
        ]

    return docs
