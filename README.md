# Tiny utility to drive obs studio via CLI

Uses python and the simpleobsws library. Tested on obs-studio compiled from
master + https://github.com/obsproject/obs-studio/pull/6468/

Create the config file `~.obspycli.conf` as follows:
```
[DEFAULT]
# Commented out lines are the default already
# host=localhost
# port=4455
password=foobar123
```

Run:
```
obs-cli start_recording
obs-cli stop_recording
```

