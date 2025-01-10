# ton-labels
Public dataset of labelled TON blockchain addresses

After each commit to the main branch artefacts are compiled and pushed:
* To [the build branch](https://github.com/shuva10v/ton-labels/blob/build/assets.json) - may be useful for manual checking addresses
* To TON Public Data Lake: s3://ton-blockchain-public-datalake/v1/ton-labels/json/
* To Dune: **dune.ton_foundation.dataset_labels** table