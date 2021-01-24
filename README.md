# Imperial-py README

ImperialBin is a hastebin alternative built with UI and user experience in mind.

### Connect With Us!

* [ImperialBin](https://Imperialb.in)
* [Discord](https://discord.gg/cTm85eW49D)

## Endpoints

* `/api/PostCode` > `post_code()`
* `/api/getCode` > `get_code()`
* `/api/checkApiToken/:apiToken` > verify()`
* `/api/getShareXConfig/:apiToken` > `get_sharex_config()`


## Python Exclusives
* camelCase json response is converted to snake_case (except sharex config)
* `expires_in`: dict key gets converted from an isoformat string to a datetime object

## Docs 
To get full docs, refer to imperial documentation. To view what goes on with imperial-py, view the full code. Every function has docstrings, and a description for increased readability.


## Contibuting
Either send contributions in the discord or open a pull request.  If you suggest a change, make sure it's backwards compatible. I believe right now, we are python 3.5 and up, but this will need more testing.