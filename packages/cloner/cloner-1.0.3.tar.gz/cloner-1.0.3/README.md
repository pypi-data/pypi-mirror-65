# A tiny utility to quickly clone github repos

## Usage
Set your local repo directory via the CLONER_PATH environment variable
``` bash
echo "export CLONER_PATH=\"~/repos\"" >> ~/.bash_profile
```

Then you can clone any github repo into that directory with the username and repo name, like this:
``` bash
cloner kardasis cloner
```
will clone this repo into `~/repos/kardasis/cloner`


You can also use the web URL from the repo
``` bash
cloner https://github.com/kardasis/cloner
```
or any URL from within the repo
``` bash
cloner https://github.com/kardasis/cloner/blob/master/cloner/cli.py
```



