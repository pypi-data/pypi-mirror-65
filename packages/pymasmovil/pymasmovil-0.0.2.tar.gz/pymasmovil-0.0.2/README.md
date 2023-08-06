# Más Móvil Python API client

This Python API client provides access to Más Móvil's B2B REST API.

## Installation

### Requirements

* Python 3.8+

## Usage

### Login

To authenticate, you need to specify credentials which need to be set as environment variables with the following names:

```bash
'MM_BASEURL': 'https://<host>/cableOperadores/services/apexrest/api'
'MM_USER': 'user'
'MM_PASSWORD': 'pwd'
```
`MM_BASEURL` must point to the MásMóvili's API environment, either testing or production. Pymasmovil will only append API routes to it like `/v0/accounts` to perform requests. In the case of testing, check with them as this surely changes per customer.

`MM_USER` and `MM_PASSWORD` must be replaced with your actual user credentials. 

### Session creation

The login is done when we create a session using the `Session.create` method:

```python
from pymasmovil.models.session import Session

session = Session.create()

print('Session created with id : {}'.format(session.session_id))
 
```

This returns the API key needed to authenticate all subsequent requests. That is why the `Session` instance has to be passed in to other all other objects methods.

### Account

```python
from pymasmovil.models.account import Account

account_id = '0017E000017pEo3QAE'
account = Account.get(session, account_id)

```
To create a new account we need to use `Account.create` passing the account data as keyword arguments. The `Account` attributes are listed bellow. Note they are all strings.

```
town, surname, stair, roadType, roadNumber, roadName, region, province, postalCode, phone, name, id, flat, email, door, donorCountry, documentType, documentNumber, corporateName, buildingPortal
```
No attribute is mandatory for the client leaving parameter validation to the API.

```python
from pymasmovil.models.account import Account

account = Account.create(session, town='Barcelona', surname='Garcia', phone='616010101')
```

### OrderItem

Order items can be accessed the same way as accounts:

```python
from pymasmovil.models.order_items.py import OrderItem

order_item_id = '8028E34500215wgQAA'
order_item = OrderItem.get(session, order_item_id)
```

Currently, order items can be created following the account creation example, but the structure of their attributes is a bit more complex. 

Since `GET /order-item/:id` response and the `POST /accounts/:id/order-items` request don't match except for a few attributes, order item creation is then designed to opimistically build an `OrderItem` instance based on the attributes inferred from the POST body. MásMóvil's API doesn't return the whole resource as one would expect with a REST API. That is why `OrderItem`'s `create` input data structure won't directly match an `OrderItem` attributes.

The minimum structure is presented as the variable `sample-order-item-post-request`: 


```python
from pymasmovil.models.order_items.py import OrderItem

order_item_data = {
    'lineInfo': [
        {
            'name': 'Antonio',
            'surname': 'Garcia',
            'phoneNumber': '616010101',
            'documentType': 'NIF',
            'portabilityDate': '2020-02-06',
            'iccid_donante': '8934046318031035245',
            'iccid': '8934046318031035250',
        }
    ]
}

order_item = OrderItem.create(session, order_item_data)

```

## Development

### Python version

We use [Pyenv](https://github.com/pyenv/pyenv) to fix the Python version and the virtualenv to develop the package.

You need to:

* Install and configure [`pyenv`](https://github.com/pyenv/pyenv)
* Install and configure [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv)
* Install the required Python version:

```
$ pyenv install 3.8.2
```

* Create the virtualenv:

```
$ pyenv virtualenv 3.8.2 pymasmovil
```

### Python packages requirements

 Install the Python packages in the virtual environment:

 ```
 $ pyenv exec pip install -r requirements.txt
 ```

## License

TBD
