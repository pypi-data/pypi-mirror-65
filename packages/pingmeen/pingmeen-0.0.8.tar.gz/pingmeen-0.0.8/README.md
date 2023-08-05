## Pingmeen lets you know, when your computation is done!

In ML and some other fields there is a common case, when you deal with computation intensive and time consuming tasks, and your solution is often written in Python. Pingmeen package allows you to ping yourself easily using Telegram when computation is done.

### How to use Pingmeen 
1. Send any message to @PingmeenBot in Telegram. It will respond to you with token within 1 minute.
2. Install this package and `requests` package (https://pypi.org/project/requests/)
3. Write some code using class Pingmeen from package and token you received from PingmeenBot.

### Code example
```
import pingmeen

ping = pingmeen.Pingmeen(token = '<your token from bot here>') # if you have passed invalid token, you'll get exception at that line

for i in range(int(1e7)):                                      # instead of that loop put some code you're waiting to be executed
    pass

ping.finish()                                                  # at that line you'll receive a message from PingmeenBot in Telegram
```