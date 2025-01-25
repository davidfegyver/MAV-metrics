### Set up crontab to run script every minute

```bash
* * * * * /usr/bin/python3 /root/fetchMAV.py >> /root/fetchMAV.log 2>&1
```

### Install requirements

```bash
pip3 install influxdb_client
```

### Set up Grafana Dashboard using the supplied JSON
