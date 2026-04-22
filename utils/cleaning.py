def deduplicate_docs(docs):
    seen = set()
    unique = []

    for doc in docs:
        content = doc.page_content.strip()

        if not content:
            continue

        if content not in seen:
            seen.add(content)
            unique.append(doc)

    print(f"✅ Deduplicated: {len(unique)} docs")
    return unique
