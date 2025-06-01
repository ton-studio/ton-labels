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

## Help Us Label Active TON Addresses and Earn TON

We need your help labeling unknown addresses on the TON Blockchain. You can find the list of addresses that need labeling, along with the rules for earning TON rewards, on this Dune dashboard:
👉 https://dune.com/ton_foundation/labelling

## View Labels on Tonviewer

To see our labels directly in Tonviewer (the TON blockchain explorer), install [this Chrome extention](https://github.com/ohld/ton-labels-extension).
It’s a powerful tool for on-chain analysis.

---

Join TON Data Hub – a community of TON analysts where we share best practices for analyzing TON data and host regular contests.
➡️ https://t.me/tondatahub
