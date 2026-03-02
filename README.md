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

### Telegram Gifts marketplaces

To add offchain telegram gifts marketplace you should add subcategory `offchain_marketplace` label — if trades are hapenning offchain(or does not use standard NFT contracts) and tag `telegram-gifts` for each address used by marketplace(deposits, withdraws).

## Help Us Label Active TON Addresses and Earn TON

We need your help labeling unknown addresses on the TON Blockchain. You can find the list of addresses that need labeling, along with the rules for earning TON rewards, on this Dune dashboard:
👉 https://dune.com/ton_foundation/labelling

## View Labels on Tonviewer

To see our labels directly in Tonviewer (the TON blockchain explorer), install [this Chrome extention](https://github.com/ohld/ton-labels-extension).
It’s a powerful tool for on-chain analysis.

---

Join TON Data Hub – a community of TON analysts where we share best practices for analyzing TON data and host regular contests.
➡️ https://t.me/tondatahub

## Dataset overview

_Calculated on: 2026-02-17 (commit ef2043c)._

### Categories

| Category                                        | Labels | Addresses | Share |
|-------------------------------------------------|--------|-----------|-------|
| [gaming](./assets/gaming)                       | 438    | 970       | 39.0% |
| [CEX](./assets/cex)                             | 68     | 474       | 19.1% |
| [merchant](./assets/merchant)                   | 115    | 218       | 8.8%  |
| [other](./assets/other)                         | 22     | 207       | 8.3%  |
| [DEX](./assets/dex)                             | 16     | 146       | 5.9%  |
| [scammer](./assets/scammer)                     | 4      | 109       | 4.4%  |
| [scripted-activity](./assets/scripted-activity) | 44     | 99        | 4.0%  |
| [infrastructure](./assets/infrastructure)       | 14     | 60        | 2.4%  |
| [wallet](./assets/wallet)                       | 16     | 54        | 2.2%  |
| [liquid-staking](./assets/liquid_staking)       | 7      | 39        | 1.6%  |
| [defi](./assets/cdp)                            | 2      | 28        | 1.1%  |
| [lending](./assets/lending)                     | 5      | 26        | 1.0%  |
| [bridge](./assets/bridge)                       | 10     | 23        | 0.9%  |
| [fund](./assets/fund)                           | 10     | 14        | 0.6%  |
| [tradingbot](./assets/tradingbot)               | 8      | 14        | 0.6%  |
| [ads](./assets/ads)                             | 1      | 4         | 0.2%  |

### Tags

| Tag                               | Usage |
|-----------------------------------|-------|
| defi                              | 172   |
| has-custodial-wallets             | 121   |
| nft                               | 114   |
| scammer                           | 88    |
| suspicious                        | 88    |
| pool                              | 71    |
| telegram-gifts                    | 61    |
| telegram-stars                    | 16    |
| telegram-premium                  | 13    |
| fee-collector                     | 11    |
| no-kyc                            | 8     |
| kyc                               | 5     |
| referral-address                  | 5     |
| telegram-ads                      | 5     |
| telegram-stars-rewards-withdrawal | 4     |
| deposit                           | 2     |
| crypto-card                       | 1     |
| withdrawal                        | 1     |
