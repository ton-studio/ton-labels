import re
import json
from typing import List
from datetime import datetime

from pydantic import BaseModel, field_validator
from pytoniq_core import Address


# Load categories and tags from external files
with open("categories.json", "rt") as f:
    categories_data = json.load(f)
allowed_categories = {item["name"] for item in categories_data}

with open("tags.json", "rt") as f:
    tags_data = json.load(f)
allowed_tags = {item["name"] for item in tags_data}

# Define allowed subcategories for each category
allowed_subcategories = {
    "merchant": {"onchain_marketplace", "offchain_marketplace"},
    "scammer": {"drainer"},
    "scripted-activity": {"sybil"},
    "gaming": {"gambling"},
    "DEX": {"perpetuals", "launchpad"},
    "defi": {"lending", "yield_aggregator", "liquid_staking", "perpetuals"},
}


class LabelledAddress(BaseModel):
    address: str
    source: str
    comment: str
    tags: List[str]
    submittedBy: str
    submissionTimestamp: datetime

    @field_validator("address")
    def validate_address(cls, address: str) -> str:
        try:
            address_uf = Address(address).to_str(True, is_bounceable=True)
        except Exception as e:
            raise ValueError(f"Invalid address: {address}: {e}")

        if address_uf != address:
            raise ValueError(
                "Address must be in bounceable format (starts with 'EQ' or 'Ef')"
            )
        return address

    @field_validator("tags")
    def validate_tags(cls, tags: List[str]) -> List[str]:
        not_in_allowed_list = set(tags) - set(allowed_tags)
        if len(not_in_allowed_list) > 0:
            raise ValueError(
                f"Tags '{not_in_allowed_list}' are not in the allowed tags list"
            )
        return tags


class Metadata(BaseModel):
    label: str
    name: str = None
    organization: str
    category: str
    subcategory: str
    website: str
    description: str

    @field_validator("website")
    def validate_website(cls, website):
        if website == "":  # Allow empty website
            return ""

        if not website.startswith("https://"):
            raise ValueError("Website must start with https://")
        if "." not in website:
            raise ValueError("Website must contain '.'")
        if "?" in website:
            raise ValueError("Website must not contain '?'")
        if website.endswith("/"):
            raise ValueError("Website must not end with '/'")
        return website

    @field_validator("label", "organization")
    def validate_key(cls, value):
        if value.startswith("sybil_"):
            # If it starts with sybil_, allow any characters after
            return value
        elif not re.match(r"^[a-z0-9._]+(?:_EQ[A-Za-z0-9_]+)?$", value):
            raise ValueError(f"{value} must be lowercase and can only contain '.', '_'")
        return value

    @field_validator("category")
    def validate_category(cls, category):
        if category not in allowed_categories:
            raise ValueError(
                f"Category '{category}' is not in the allowed categories list"
            )
        return category
    
    @field_validator("subcategory")
    def validate_subcategory(cls, subcategory, info):
        category = info.data.get('category')
        
        # Allow empty subcategory
        if subcategory == "":
            return subcategory
            
        # If category has allowed subcategories, validate against them
        if category in allowed_subcategories:
            if subcategory not in allowed_subcategories[category]:
                raise ValueError(
                    f"Subcategory '{subcategory}' is not allowed for category '{category}'. "
                    f"Allowed subcategories are: {allowed_subcategories[category]}"
                )
        elif subcategory != "":
            # If category doesn't have defined subcategories, only empty string is allowed
            raise ValueError(
                f"Category '{category}' does not allow any subcategories. Only empty string is allowed."
            )
            
        return subcategory
    
    def model_post_init(self, __context):
        if not self.name:
            # Convert label to name format if name is not provided
            self.name = self.label.replace("_", " ").capitalize()


class LabelledData(BaseModel):
    metadata: Metadata
    addresses: List[LabelledAddress]
