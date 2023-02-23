import os
import openai
import polars as pl

openai.organization = "org-Vfki9wAixkDQGPP3mkFNOYwC"
with open("secret.txt", "r") as f:
    openai.api_key = f.read().strip()
