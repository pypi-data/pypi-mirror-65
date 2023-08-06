# Project description
For working with api methods of the test environment

# Installation
$ pip install bee_data_api
 
# Examples
Running only on python 3.7+
    
    import bee_data_api

    your_variable = bee_data_api.bee_data.DataTest()
    response = your_variable.get_module(50).json())
# Results
We receive the answer from 'request' library

```
{'id': 50, 'name': '1string', 'description': '2string', 'project': {'id': 14, 'projectName': 'new name', 'description': 'некоторое описание проекта'}}
```

