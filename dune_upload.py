import sys
from dune_client.client import DuneClient

dune = DuneClient.from_env()

file_path = sys.argv[1]
with open(file_path) as file:
    data = file.read()

table = dune.upload_csv(
    data=str(data),
    description="Labeled dataset for TON blockchain",
    table_name="labels",
    is_private=False
)

print(table)
