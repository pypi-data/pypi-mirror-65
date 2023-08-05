"""Miscellaneous functions used to fulfill common requirements


## Example

Example CSV file, `accounts.csv`:

    Id,Email
    1,john@example.com
    2,jane@example.com

Example usage:

    from pprint import pprint

    list_output = csv_to_list('accounts.csv')
    pprint(list_output)
    [{'Email': 'john@example.com', 'Id': '1'},
    {'Email': 'jane@example.com', 'Id': '2'}]

    dict_ouput = csv_to_dict('Id', 'accounts.csv')
    pprint(dict_ouput)
    {'1': {'Email': 'john@example.com'}, '2': {'Email': 'jane@example.com'}}

## Installation

    pip3 install onnmisc

## Contact

* Code: [onnmisc](https://github.com/OzNetNerd/onnmisc)
* Blog: [oznetnerd.com](https://oznetnerd.com)
* Email: [will@oznetnerd.com](mailto:will@oznetnerd.com)

"""

from .csv_funcs import *
