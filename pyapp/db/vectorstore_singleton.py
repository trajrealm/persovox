
_vectorstore_registry = {}

def create_vectorstore(user_id):
    return _vectorstore_registry.get(user_id)

def add_vectorstore(user_id, vstore):
    _vectorstore_registry[user_id] = vstore

def get_all_vectorstore_users():
    return list(_vectorstore_registry.keys())

def get_all_vectorstores():
    """Optional: Get the entire registry (read-only)."""
    return _vectorstore_registry.copy()

