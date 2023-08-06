# Skreep
It's fun data scraping with just a few lines of code. Basically Skreep is a function to make it easier to run selenium.

# Example
```
from skreep.skreep import Skreep
from skreep.download import dl
from skreep.datasheet import sheet
from skreep.save import Save
from skreep.display import display

data = sheet("data")
sk = Skreep()
sv = Save(name='name_file')

for i in data:
    sk.get(i, sc=5)
    title = display(sk.tag('h1', sc=5))
    sv.save(title)

sk.quit()
```

# Dependency
```
selenium
```

# Driver
```https://chromedriver.chromium.org/downloads```

# Donate
BTC ```37rkr9cpVVcxg8vUpF65Cp9Mjgu1WrKD3d``` or 
Paypal [Here](https://paypal.me/dian26?locale.x=id_ID "Donate")
