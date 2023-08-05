This is the official python repo for TrueData.
-------


**What have we covered so far ?**
* Websocket APIs
  *  Live data
  *  Historical data

**How do you use it ?**

**For beginners**

* Installing from PyPi
```
pip install truedata
```

* Connecting 
```
from truedata.websocket.TD import TD
td_app = TD('<enter_your_login_id>', '<enter_your_password>')
```

* Starting live data
```
td_app.start_live_data('<enter_symbol>', req_id=2000)  # Example: td_app.start_live_data('CRUDEOIL-I')
count = 0
while count < 60:
    print(f'{td_app.live_data[2000].ltp} @ {td_app.live_data[2000].timestamp}')
    sleep(1)
    count = count + 1
```

<br>
<br>
<br>
<br>
<br>
<br>

**For advanced users**
* Installing from PyPi
```
pip install truedata==xx.xx.xx <pick your version number>
```
* Installing from source

Download the sources

Make "truedata" the working directory using cd
```
python3 setup.py install
```

* Connecting 
```
from truedata.websocket.TD import TD
td_app = TD('<enter_your_login_id>', '<enter_your_password>, live_port=8080, historical_port=8090)  # historical_port should be None, if you do not have access to historical data...
```

* Starting live data
```
td_app.start_live_data('<enter_symbol>', req_id=2000)  # Example: td_app.start_live_data('CRUDEOIL-I')
count = 0
while count < 60:
    print(td_app.live_data[2000].__dict__)
    sleep(1)
    count = count + 1
```
    
**What is the plan going forward ?**
* Ease of contract handling
* Improved error handling
