import os
def gather_files():
    tasks = []
    for filename in os.listdir("./tasks"):
        if filename.endswith(".txt") or filename.endswith(".md"):
            tasks.append(filename)
    return tasks