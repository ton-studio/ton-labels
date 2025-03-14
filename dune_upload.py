import sys
import ast
import pandas as pd
from dune_client.client import DuneClient

dune = DuneClient.from_env()

file_path = sys.argv[1]
df = pd.read_csv(file_path, index_col=0)

# convert df.tags from a string to a list
# example value of df.tags[0]: "['defi', 'nft]"

df.tags = df.tags.apply(ast.literal_eval)
df.submissionTimestamp = pd.to_datetime(df.submissionTimestamp)

table = dune.upload_csv(
    data=df.to_csv(),
    description="Labeled dataset for TON blockchain",
    table_name="labels",
    is_private=False,
)

print(table)
