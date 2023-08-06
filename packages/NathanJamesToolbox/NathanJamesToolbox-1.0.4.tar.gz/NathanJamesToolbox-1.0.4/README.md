# NathanJames Toolbox

Collection of tools used by NathanJames

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

You can use pip to install the package.

```
pip install NathanJamesToolbox
```

## Usage

importing the module

```
from NathanJamesToolbox import NathanJamesToolbox as nj
```

### airtableToolbox

```
myAirtable = nj.airtableToolbox(<airtable base>, <airtable API Key>)
```

Create a dictionary from airtable columns
reverse=False will use airtable base column name as the key and add row ID into the value list
reverse=True will use airtable row ID as the key and add base column name into the value list
*args are additional column you want to add into the value list
```
myAirtable.create_dictionary(url, baseColumnName, reverse=False, *args)
```

Cleans up the string by removing the following charcater in a string ([, ', ])
```
myAirtable.create_dictionary.clean_list_string("['TEST']")
>>> TEST
```

Push a payload into airtable
patch=True sends a patch request
patch=False sens a post request
```
push_data(url, payload, patch=True)
```

## Authors

* **Paulo Fajardo** - *Initial work* - [github](https://github.com/pfajardo-nj/NathanJames-Automation-Script)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details