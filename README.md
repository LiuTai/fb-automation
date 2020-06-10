# Facebook Automation
Below is what you can do with this program:
 -- Login to Facebook
 -- Add people to group chat

 ## Install
 1. Make sure you have Chrome browser installed.
 2. Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) and put it into bin folder: `./bin/chromedriver`. Make sure webdriver is the same version as Chrome browser
 3. Install Selenium: `pip install -r requirements.txt`

 ### Usage
```
positional arguments:
  mode
    options: [create_group]

optional arguments:
   -u USERNAME,
   -p PASSWORD,
   -0 OUTPUT FILE DIRECTORY

Log directory:
./src/tmp

User config file:
./src/users.json
```

### Example
```
 python3 main.py create_group -u "account" -p "password" -o "./src/tmp/user.json"
```