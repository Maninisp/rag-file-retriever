from retrieve_file.project_detector import detect_project_root

test_cases = [
    ("test_data/project_alpha/app.py", "test_data"),
    ("test_data/project_beta/app.py", "test_data"),
    ("test_data/notes/ideas.txt", "test_data"),
    ("test_data/project_alpha/app.py", "test_data/project_alpha"),
    ("test_data/project_beta/app.py", "test_data/project_alpha"),
]

for file_path, search_root in test_cases:
    print(detect_project_root(file_path, search_root))