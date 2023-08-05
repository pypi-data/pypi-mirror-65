# sqlsettingslib

Python lib: Store settings in a database

## What is this library for?

In some projects you might want to store some variables for longer than you run the program. When restarting the program you might still want some settings to be the same. Those settings could be stored in a database. This lib does all the complicated part for you.

## Usage

```python
from sqlsettingslib import Setting

# Define the path for your database
path = "path/to/sqlsettingslib.sqlite3"

# Create a sqlsettingslib object:
s = Setting(path)

# Add some sqlsettingslib
s.add_setting(
    text_id="user_name",
    readable_name="User name",
    description="A name for the user",
    value="MyCoolUserName"
)

print(s["user_name"])
# -> "MyCoolUserName"

s["user_name"] = "AnotherCoolName"
print(s["user_name"])
# -> "AnotherCoolName"

s.update_setting(
    text_id="user_name",
    description="A unique name for the user."
)

print(s.get_setting(detail="description")[0])
# -> "A unique name for the user."
```