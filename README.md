# Description
This is a stopwatch GUI app with start, stop, and reset functions.

![Screenshot](/screenshots/screenshot.png?raw=true)

Hitting start while already started has no effect.

When you hit stop, the time is not reset.

You can hit start to resume from the last stop. For example, if you stop at
1.5 seconds, and then wait 5 seconds, and then hit start, the time continues
from 1.5 seconds; not 6.5 seconds.

reset stops and resets the time to 0.

stopping while already stopped has no effect.

# Running the script directly on Windows
On Windows, you can run this without a console window via
```
> pythonw .\stopwatch.py 
```

# Building stopwatch.exe via Poetry
First, you have to install Poetry. You'll have to google if you don't know.

Then you can use Poetry to install the dependencies (just pyinstaller).
```
> poetry install
```

Finally, you can run the following command to build stopwatch.exe.
```
> poetry run pyinstaller --onefile --windowed stopwatch.py
```

