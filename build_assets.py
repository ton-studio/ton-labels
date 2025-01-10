import os
from pathlib import Path
import json
import traceback
from loguru import logger
import pandas as pd
import git
from pytoniq_core import Address

"""
Utility script to collect all json files in "assets" directory and build a single CSV and JSON file.
Each json file can contain a single object or an array of objects related to the same entity.

Also the scripts validates enumeration fields against dictionaries:
* categories.json
"""

if __name__ == "__main__":
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    output = []
    logger.info(f"Building assets for commit {sha}")

    logger.info("Loading categories whitelist")
    categories = set()
    with open("categories.json", "rt") as f:
        categories_data = json.load(f)
        for item in categories_data:
            categories.add(item["name"])
    logger.info(f"Loaded {len(categories)} categories")

    logger.info("Loading tags whitelist")
    tags = set()
    with open("tags.json", "rt") as f:
        tags_data = json.load(f)
        for item in tags_data:
            tags.add(item["name"])
    logger.info(f"Loaded {len(tags)} tags")

    address_set = set()

    for path in Path("assets").rglob("*.json"):
        with open(path, "rt") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                raise Exception(f"Can't parse JSON on path: {path}")

            if isinstance(data, dict):
                data = [data]
            assert isinstance(data, list), f"Expected list, got {type(data)}"
            for item in data:
                try:
                    assert "address" in item, f"Expected 'address' in {item} ({path})"
                    assert "label" in item, f"Expected 'label' in {item} ({path})"
                    assert (
                        "submittedBy" in item
                    ), f"Expected 'submittedBy' in {item} ({path})"
                    assert (
                        "submissionTimestamp" in item
                    ), f"Expected 'submissionTimestamp' in {item} ({path})"

                    assert "category" in item, f"Expected 'category' in {item} ({path})"
                    assert (
                        item["category"] in categories
                    ), f"Unknown category {item['category']} in {item} ({path})"

                    assert "tags" in item, f"Expected 'tags' in {item} ({path})"
                    for tag in item["tags"]:
                        assert tag in tags, f"Unknown tag {tag} in {item} ({path})"

                    # TODO validate source field?

                    address = Address(item["address"])
                    address_raw = address.to_str(False).upper()
                    address_uf = address.to_str(True, is_bounceable=True)
                    address_uf_nb = address.to_str(True, is_bounceable=False)
                    assert (
                        address_raw not in address_set
                    ), f"Duplicate address {address_raw} in {item} ({path})"
                    address_set.add(address_raw)
                    output.append(
                        {
                            "address": address_raw,
                            "address_uf": address_uf,
                            "address_uf_nb": address_uf_nb,
                            "label": item["label"],
                            "category": item["category"],
                            "subcategory": item.get("subcategory", None),
                            "organization": item.get("organization", None),
                            "image": item.get("image", None),
                            "source": item.get("source", None),
                            "description": item.get("description", None),
                            "comment": item.get("comment", None),
                            "tags": item.get("tags", None),
                            "submittedBy": item.get("submittedBy", None),
                            "submissionTimestamp": item.get(
                                "submissionTimestamp", None
                            ),
                            "github_hash": sha,
                        }
                    )
                except Exception as e:
                    logger.error(
                        f"Error processing {path}: {e}: {traceback.format_exc()}"
                    )
                    raise e

    logger.info(f"Building output files with {len(output)} records")
    output_df = pd.DataFrame(output).sort_values(by="address")
    os.makedirs("output/csv", exist_ok=True)
    output_df.to_csv("output/csv/assets.csv", index=False)
    os.makedirs("output/json", exist_ok=True)
    with open("output/json/assets.json", "wt") as f:
        for row in output_df.to_dict(orient="records"):
            f.write(json.dumps(row))
            f.write("\n")
