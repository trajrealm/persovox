import os

def get_available_users(base_dir="data"):
    return [
        name for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name))
    ]