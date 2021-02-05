
# Imperial-py README

ImperialBin is a hastebin alternative built with UI and user experience in mind.

### Connect With Us!

* [ImperialBin](https://Imperialb.in)
* [Discord](https://discord.gg/cTm85eW49D)

## Endpoints

* `/api/PostCode` > `post_code()`
* `/api/getCode` > `get_code()`
* `/api/checkApiToken/:apiToken` > `verify()`


# Example Usage
```python
from imperial_py import Imperial

imp = Imperial()  # with or without api token

imp.post_code("Hello World!")
# {'success': True, 'document_id': 'bmhn60klmpw', 'raw_link': 'https://www.imperialb.in/r/bmhn60klmpw', 'formatted_link': 'https://www.imperialb.in/p/bmhn60klmpw', 'expires_in': datetime.datetime(2021, 1, 29, 18, 55, 37, 725000), 'instant_delete': False}

imp.get_code("bmhn60klmpw")
# {'success': True, 'document': 'Hello World!'}
```


## Python Exclusives
* camelCase json response is converted to snake_case
* The `expires_in` dict key gets converted from an isoformat date string to a datetime object

## Docs 
To get full docs, refer to imperial documentation. To view what goes on with imperial-py, view the full code. Every function has docstrings, and a description for increased readability.


## Contibuting
Either send contributions in the discord or open a pull request.  If you suggest a change, make sure it's backwards compatible. I believe right now, we are python 3.5 and up, but this will need more testing.