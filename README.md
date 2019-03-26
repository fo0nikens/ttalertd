### TTAlertd | Twilio Top Alert
##### Recieve SMS alerts when <i>top</i> metrics exceed thresholds 

<img src="https://github.com/rootVIII/ttalertd/blob/master/sc.jpg" alt="ex" height="700" width="380">





1.  If not already installed, <code>sudo apt-get install supervisor</code>.
&nbsp;A current version of Twilio must also be installed into your Python3
&nbsp;interpreter: <code>pip3 install twilio</code>. You also need a working,
SMS-capable Twilio number.
<hr>

2. Enter the required fields into the example <b>credentials.yml</b>. Then move
credentials.yml into the <b>utils/</b> directory.

```
twilio:
    - "your Twilio account SID"
    - "your Twilio auth token"
    - "+18885551234" 
    - "+15551234567"
defaults:
    LOAD_AVG_MAX: 1.2
    CPU_LIMIT: 20.0
    ALERT_INTERVAL: 60.0
    RESET_INTERVAL: 60.0

```
- All <b>Twilio</b> list elements should be in quotes
- The 3rd entry is your mobile number
- The 4th entry is your Twilio number
- Ensure to use quotes and +1 for phone numbers
<br><br>
- All <b>defaults</b> values should be floats
- Provide a threshold for Load Average (Top load average over last minute)
- Provide CPU % threshold for each individual Top process found<br>
(the top 8 are analyzed with each iteration)
- Provide an ALERT_LEVEL in seconds
- RESET_INTERVAL: number of iterations of alert intervals


In the example YAML above, a reset interval of 60 iterations is 60 alert<br>
level runs before resetting. (This just means the daemon runs every 60 seconds<br>
and resets after 60 runs).<br>

The code basically runs every sixty seconds. Alerts for processes/CPU % <br>
are sent only once as they are stored in <b>memory.json</b> to prevent repeat alerts.<br>
However changes in users logging in/out and load average thresholds, <i>could</i> be<br>
alerted with each iteration. Therefore if you have many users logging in/out, be<br>
prepared for a lot of alerts.<br>

After the daemon runs 60 times the RESET INTERVAL is met and memory.json is<br>
reset to empty. This means that  Alerts that were previously sent and tracked<br>
may now trigger again.<br>
<hr>
3. If supervisord is already installed, add the project's <b>supervisord.conf</b> contents
&nbsp;to your existing config. file.<br>

- If you just installed supervisord, replace the existing <code>/etc/supervisord.conf</code>
file with the one provided here.

- Edit the line: <code>directory=/etc/supervisor/ttalertd</code> to match the location
  of the project folder.
<hr>

##### Start the daemon with the command <code>sudo service supervisor start</code>
##### Stop the daemon with the command <code>sudo service supervisor stop</code>

<br>

### Alerts
- If the usernames of logged in users changes, an alert will be sent with the username(s), and 
whether they logged on or off (this includes SSH/remote users).

- If the most recent load average exceeds <b>LOAD_AVG_MAX</b> and the previously alerted value,
an alert is sent as an SMS text message.

- The top 8 processes are analyzed. Any that exceed a CPU percentage of <b>CPU_LIMIT</b>
are sent as an SMS text message along with the username, pid, and program name. <i>An alert will
only be sent once</i> for any given process that crosses the threshold. This is decided by
RESET_INTERVAL. Once the RESET_INTERVAL is passed, all alerts are reset.
<br>
Logs are appended to <code>utils/ttalertd.log</code> and <code>/var/log/supervisor/supervisord.log</code>
<br><br
Intended for Linux distros, however only tested/developed only on Ubuntu 18.04
<br><br>
Remember to move credentials.yml into the utils/ directory.
<br>

```
ttalertd
├── credentials.yml
├── __init__.py
├── LICENSE
├── README.md
├── sc.jpg
├── supervisord.conf
├── ttalertd.py
└── utils
    ├── compare.py
    ├── credentials.yml
    ├── __init__.py
    ├── log.py
    ├── memory.json
    ├── read_write.py
    ├── sms.py
    ├── top.py
    ├── ttalertd.log
    └── who.py
```

<hr>
Author: James Loye Colley MAR 2019
