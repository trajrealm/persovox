import os
import sys

print("Current Working Directory:", os.getcwd())
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
print("sys.path:", sys.path)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("Updated sys.path:", sys.path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
