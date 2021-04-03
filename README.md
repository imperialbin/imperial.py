

# imperial-py

## Imperial is a code/text sharing site with the user experience in mind, it has feautures such as editing, encryption and integration with github gists and discord.

### Connect With Us!

* [Imperial Bin](https://Imperialb.in)
* [Discord](https://discord.gg/cTm85eW49D)

## Endpoints

|Function           |Endpoint            |Request Type|
|:----:             |:----:              |:----:      |
|`create_document()`|`/api/document`     |POST        |
|`get_document()`   |`/api/document`     |GET         |
|`edit_document()`  |`/api/document`     |PATCH       |
|`delete_document()`|`/api/document`     |DELETE      |
|`verify()`         |`/api/CheckApiToken`|GET         |

# Example Usage

An API Token is not required, but you can't edit without one, and this is generally made with authorization in mind.

Add `IMPERIAL-TOKEN` to path to set it automatically; this will get overwritten by setting one manually.

```python
from imperial_py import Imperial

imp = Imperial()

imp.create_document("Hello World!")
# {'success': True, 'document_id': 'bmhn60klmpw', 'raw_link': 'https://www.imperialb.in/r/bmhn60klmpw', 'formatted_link': 'https://www.imperialb.in/p/bmhn60klmpw', 'expires_in': datetime.datetime(2021, 1, 29, 18, 55, 37, 725000), 'instant_delete': False}

imp.get_document("bmhn60klmpw")
# {'success': True, 'document': 'Hello World!'}

imp.edit_document("Hello From Python!", "bmhn60klmpw")
# {'success': True, 'message': 'Successfully edited the document!', 'document_id': 'phqmaxastug', 'raw_link': 'https://www.imperialb.in/r/phqmaxastug', 'formatted_link': 'https://www.imperialb.in/p/phqmaxastug', 'expires_in': datetime.datetime(2021, 2, 13, 19, 30, 54, 839000), 'instant_delete': False}

imp.get_document("bmhn60klmpw")
# {'success': True, 'document': 'Hello From Python!'}

```

## Shorthand Functions
```python
import imperial_py
imperial_py.create_document("Hello World!")  # same as Imperial().create_document()
imperial_py.get_document("bmhn60klmpw")  # same as Imperial().get_document()
# etc...
```


# Python Exclusives
* camelCase json response is converted to snake_case
* The `expiration` dict key gets converted from an isoformat string to a datetime object

# Contributing

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Commit changes to your own branch
4. Push your work to your fork
5. Submit a Pull request so that I can review your changes

NOTE: If you suggest a change, make sure it's backwards compatible. As of now, imperial-py is python 3.0 and up.

# Docs 
To get full docs, refer to imperial documentation. To view what goes on with imperial-py, view the full code. Every function has docstrings and a description.
