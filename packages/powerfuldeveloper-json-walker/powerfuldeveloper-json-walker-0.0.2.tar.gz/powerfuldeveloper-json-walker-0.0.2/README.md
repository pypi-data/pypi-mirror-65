# Powerfuldeveloper Json Walker

Walk on jsons like it's nothing 😎  
# Usage
Just give `JsonWalker` class the json which you want
to pars and this class is able to give you feet which
need to walk on json !  
```python
from powerfuldeveloper.json_walker import JsonWalker

some_json = {
    "key_1": 'test',
    "key_2": 1,
}
json_walker = JsonWalker(some_json)
print(json_walker.key_1) 
# test
print(type(json_walker.key_1)) 
# JsonWalker
print(json_walker.key_1.inner_key_1) 
# None
print(type(json_walker.key_1.inner_key_1)) 
# JsonWalker
if json_walker.key_1.inner_key_1:
    print('inner key 1 exists')

```
