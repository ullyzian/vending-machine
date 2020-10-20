# Vending Machine

# Setup

Create virtual environment and install dependencies
```shell script
$ python -m venv venv
(win) $ source venv/Scripts/activate
(unix) $ source venv/bin/activate
$ pip install -r requirements.txt
```

Run application
```shell script
$ python main.py
```


## Bundle app

Create apps for Mac (app and shell exec), Windows and Linux

```shell script
$ pyinstaller main.spec
```
After that you can find executable files for your system in `dist/` folder