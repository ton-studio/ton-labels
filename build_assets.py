import os
import git
import json
import pandas as pd
from pathlib import Path
from loguru import logger
from pytoniq_core import Address


from models import LabelledData

"""
Utility script to collect all json files in "assets" directory and build a single CSV and JSON file.
Each json file can contain a single object or an array of objects related to the same entity.

Also the scripts validates enumeration fields against dictionaries:
* categories.json
"""


if __name__ == "__main__":
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    logger.info(f"Building assets for commit {sha}")

    serialized_labels = {}
    label_to_file = {}  # Track which file each label comes from

    for path in Path("assets").rglob("*"):
        if not path.is_file() or path.name.startswith("."):  # Skip directories and hidden files
            continue

        if not path.suffix == ".json":
            raise Exception(f"File should be .json: {path}")
            
        with open(path, "rt") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                raise Exception(f"Can't parse JSON on path: {path}")

        labelled_data = LabelledData(**data)
        metadata = labelled_data.metadata

        # Check for duplicate label across files
        label = metadata.label
        if label in label_to_file and label not in ["scammer"]:  # allow multiple scammer labels
            raise Exception(
                f"Label '{label}' is present in both {label_to_file[label]} and {path}. Each label must be unique across all JSON files."
            )
        label_to_file[label] = path

        for address_data in labelled_data.addresses:
            address = Address(address_data.address)
            address_raw = address.to_str(False).upper()
            address_uf = address.to_str(True, is_bounceable=True)
            address_uf_nb = address.to_str(True, is_bounceable=False)

            if address_raw in serialized_labels:
                raise Exception(
                    f"Address {address_data.address} appears also in {serialized_labels[address_raw]}"
                )

            serialized_labels[address_raw] = {
                "label": metadata.label,
                "name": metadata.name,
                "category": metadata.category,
                "subcategory": metadata.subcategory,
                "organization": metadata.organization,
                "description": metadata.description,
                "website": metadata.website,
                "address": address_raw,
                "address_uf": address_uf,
                "address_uf_nb": address_uf_nb,
                "source": address_data.source,
                "comment": address_data.comment,
                "tags": address_data.tags,
                "submittedBy": address_data.submittedBy,
                "submissionTimestamp": address_data.submissionTimestamp.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "github_hash": sha,
            }

    logger.info(
        f"Building output files with {len(serialized_labels)} labelled addresses."
    )
    output_df = pd.DataFrame(serialized_labels.values())
    os.makedirs("output/csv", exist_ok=True)

    output_df.to_csv("output/csv/assets.csv", index=False)
    os.makedirs("output/json", exist_ok=True)

    with open("output/json/assets.json", "wt") as f:
        for row in output_df.to_dict(orient="records"):
            f.write(json.dumps(row))
            f.write("\n")
