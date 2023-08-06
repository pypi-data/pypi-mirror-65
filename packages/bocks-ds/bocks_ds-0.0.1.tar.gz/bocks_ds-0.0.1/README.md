# datasource-python
Python SDK for all DataSource iterations


## Installation

Install this package via pip:

`pip install bocks_ds`


## Usage

### The Client

First, import this package and instantiate a client object, providing the name of the datasource to access.

```
import bocks_ds

ds_client = bocks_ds.Client("starfinder")
```

We will use this client for all of the following examples. It is recommended to instantiate the client in a central location that you may import into other application files as necessary.

Note that if you enter a string here that is not a valid target, a `DSTargetError` exception will be raised.


### Fetching Data

There are currently only two options to consider when fetching data: the type and the parameters.

The "type" can be thought of as a data table, though we will discuss some complexities later on.

In the example below, we will request the name and price for all rows in the "armor" type from the "starfinder" client that we instantiated above. In this example we'll also show you how you can add an optional status check after making the request.

```
response = ds_client.armor.get(['name', 'price'])
if response.status_code == 200:
    data = response.json()
```

Note that the `ds_client` will accept any value as an attribute, which it will then use to craft an API request. If you request something that doesn't exist, the request will raise a `DSQueryError` exception.

### Refining Your Request

The API allows for active filtering of strings and integers within your request. To do this, you'll need to set arguments immediately prior to making the request. 

For data values that return strings, you may refine with the terms `<value_name>_like` and `<value_name>_is`. For "like" queries, sequencing is not considered and the search is not case sensitive. For "is" queries, only exact, case-sensitive matches will be returned.

For data values that return integers, you may refine with the terms `<value_name>_min`, `<value_name>_max` and `<value_name>_equals`. These equate to "greater than or eqal to", "less than or equal to", and "equal to", respectively.

Finally, it is often valuable to select an item specifically by its `ID`, which functions in a more direct manner than the queries for integers (see example below).

All arguments must be presented as a single dictionary, as seen in the examples below.

```
client.armor.set_arguments({"name_like":"basic"})
response = ds_client.armor.get(['name', 'price'])
```

```
client.armor.set_arguments({"price_min":200, "price_max":2000})
response = ds_client.armor.get(['name', 'price'])
```

```
client.armor.set_arguments({"id":1})
response = ds_client.armor.get(['name', 'price'])
```

Note that these requests do not stack, but you can place all terms into a single dictionary to futher refine results. If `set_arguments` is called multiple times, the final call will overwrite previous calls.

```
query = {"name_like":"basic", "price_min":200, "price_max":2000}
client.armor.set_arguments(query)
response = ds_client.armor.get(['name', 'price'])
```

As a final note: all arguments are cleared when `get` is called.

### Fetching Nested Data

As mentioned previously, not all types match their data tables precisely. Some types include additional data from relationships with other tables. Documentation for these relationships is automatically generated in the API Documentation (such as at *docs.sfdatasource.com*).

In order to access nested data, it is required that you present a dictionary describing the data to fetch.

Where we previously provided a list of string field-names to query, we will now include a dictionary in that list, as seen in the examples below.

```
query = [
    "name",
    {
        "effect_ranges": ["name", "description"],
    }
]
all_spells = ds_client.spells.get(query)
```

This logic is recursive, so in the event that a relationship target has it's own relationships you may do the following:

```
query = [
    "name",
    {
        "class_proficiencies": ['name'],
        "class_features": ["name", {
            "class_special_skills": ['name']
        }],
    }
]
spells = client.classes.get(query)
```