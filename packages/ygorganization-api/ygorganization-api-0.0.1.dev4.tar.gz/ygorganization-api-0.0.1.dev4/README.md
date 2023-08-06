# About

This is a Python interface to [the YGOrganization database](https://db.ygorganization.com/), which provides up-to-date information on cards in [the Yu-Gi-Oh! Trading Card Game](https://en.wikipedia.org/wiki/Yu-Gi-Oh!_Trading_Card_Game).

For request paths and further information, please see [the API documentation](https://db.ygorganization.com/about/api).

# Usage

`import ygorganization`

**_async_** `ygorganization.Query(path)` - Queries path, resolves with JSON object
**_async_** `ygorganization.GetCardData(id)` - shorthand for `Query('/data/card/%d'%id)`
**_async_** `ygorganization.GetQAData(id)` - shorthand for `Query('/data/qa/%d'%id)`
