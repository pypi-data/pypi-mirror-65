# Handy Dict
> A library with some handy utils to deal with dictionaries that contain arrays


This file will become your README and also the index of your documentation.

## Install

`pip install handy-dict`

## How to use

### Let's start with a dictionary

```python
pikachu = {
  "name": "pikachu",
  "moves": [
    {
      "move": {
        "name": "mega-punch",
        "url": "https://pokeapi.co/api/v2/move/5/"
      }
    },
    {
      "move": {
        "name": "pay-day",
        "url": "https://pokeapi.co/api/v2/move/6/"
      }
    },
    {
      "move": {
        "name": "thunder-punch",
        "url": "https://pokeapi.co/api/v2/move/9/"
      }
    }
  ],
  "stats": [
    {
      "base_stat": 90,
      "effort": 2,
      "stat": {
        "name": "speed",
        "url": "https://pokeapi.co/api/v2/stat/6/"
      }
    },
    {
      "base_stat": 50,
      "effort": 0,
      "stat": {
        "name": "special-defense",
        "url": "https://pokeapi.co/api/v2/stat/5/"
      }
    }
  ]
}
```

### `apply_keyed`

```python
from handy_dict import apply_keyed
```

With *handy-dict* you can apply a function to the keys inside a dictionary, say you want to take `name` out of `stat`,  go from something like this:

```json
{
  "base_stat": 50,
  "effort": 0,
  "stat": {
    "name": "special-defense",
    "url": "https://pokeapi.co/api/v2/stat/5/"
  }
}
```

to this:

```json
{
  "base_stat": 50,
  "name": "special-defense"
}
```

The function `transform_stat` is just a little helper that will transform the `stats` array in our `pikachu` dictionary and return a new array, that will replace the `stats` in a copy of the original dict:

```python
def transform_stat(stat_array):
    return {
        stat["stat"]["name"]: stat["base_stat"] 
        for stat in stat_array 
    } 
```

```python
modified_pikachu = apply_keyed(pikachu,["stats"], transform_stat)
modified_pikachu["stats"]
```




    {'speed': 90, 'special-defense': 50}



### `return_keyed`

```python
from handy_dict import return_keyed
```

*handy-dict* also makes it easy to return multiple values from a dictionary, iterating through keys and arrays:

```python
return_keyed(pikachu, ["moves","move","name"])
```




    ['mega-punch', 'pay-day', 'thunder-punch']


