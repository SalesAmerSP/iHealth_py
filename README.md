# iHealth Python

Add Client ID and client secret to user_info

# return_ihealth_files.py

**PreReq**

You will need to change line 93 to a local directory to create the temp file

In this set of scripts, Python will:

- auth_in - log into iHealth and obtain a token
- list_files - list all files associated with qkview
Example:
```
{'id': 'c3RhdF9tb2R1bGUueG1s', 'permissions': '0644', 'size': 5504428, 'lastModified': 'Apr 16 2024 14:27', 'value': '/stat_module.xml'}
```
- search - find specific filename and in this case it is */stat_module.xml* file 
- get_files - grab file and contents based on filename search and file id *c3RhdF9tb2R1bGUueG1s*
 