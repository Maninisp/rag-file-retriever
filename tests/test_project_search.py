from pprint import pprint
from retrieve_file.project_search import project_search

results = project_search(
    query="Find the veterinary clinic management application",
    search_root="test_data"
)

pprint(results)