from retrieve_file.semantic_search import semantic_search

queries = [
    "Find the veterinary clinic management application",
    "Which file implements pet appointments?",
    "Where are employee support tickets handled?",
    "How do I calculate income tax?"
]

# for query in queries:
#     print(f"\nQuery: {query}")

#     results = semantic_search(query, top_k=3, threshold=0.20)

#     if not results:
#         print("No relevant files found")
#     else:
#         for result in results:
#             print(result["name"], round(result["score"], 4))

for query in queries:
    results = semantic_search(query, top_k=3)

    print(f"\nQuery: {query}")
    print(results if results else "No relevant files found")