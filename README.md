
# Imperial-py README

ImperialBin is a hastebin alternative built with UI and user experience in mind.

### Connect With Us!

* [ImperialBin](https://Imperialb.in)
* [Discord](https://discord.gg/cTm85eW49D)

## Endpoints

|Function           |Endpoint            |Request Type|
|:----:             |:----:              |:----:      |
|`create_document()`|`/api/document`     |POST        |
|`get_document()`   |`/api/document`     |GET         |
|`edit_document()`  |`/api/document`     |PATCH       |
|`verify()`         |`/api/CheckApiToken`|GET         |

# Example Usage

An API Token is not required, but certain calls don't work without one and this is generally made with authorization in mind. 

Add `IMPERIAL-TOKEN` to path to set it automatically.

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

### Shorthand Functions
```python
import imperial_py
imperial_py.create_document("Hello World!")  # same as Imperial().post_code()
imperial_py.get_document("bmhn60klmpw")  # same as Imperial().get_code()
# etc...
```


## Python Exclusives
* camelCase json response is converted to snake_case
* The `expires_in` dict key gets converted from an isoformat string to a datetime object

## Docs 
To get full docs, refer to imperial documentation. To view what goes on with imperial-py, view the full code. Every function has docstrings, and a description.


## Contibuting
Either send contributions in the discord or open a pull request.  If you suggest a change, make sure it's backwards compatible. I believe right now, imperial-py is python 3.5 and up.