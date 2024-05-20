import time

from educore import light,pin

p=pin(11)
p.write_analog(value=100)
time.sleep(1)
a = light(0)
while 1:
    print(a.read())
    time.sleep(1)