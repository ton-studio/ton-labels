# ton-labels
Public dataset of labelled TON blockchain addresses

After each commit to the main branch artefacts are compiled and pushed:
* To [the build branch](https://github.com/shuva10v/ton-labels/blob/build/assets.json) - may be useful for manual checking addresses
* To TON Public Data Lake: s3://ton-blockchain-public-datalake/v1/ton-labels/json/
* To Dune: **dune.ton_foundation.dataset_labels** table

## How to add labels

1. Create a .json file in the path: `assets / {category} / {label}.json`.
2. Run `build_assets.py` to validate a schema of your JSON against the data models described in `models.py`.
3. If you want to add a new category or a tag, make sure to add them to `categories.json` and `tags.json`.