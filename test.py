import threading
s = ""
def func1():
	global s
	for i in range(1000):
		s += '1'

def func2():
	global s
	for i in range(1000):
		s += '2'

t1 = threading.Thread(target=func1)
t2 = threading.Thread(target=func2)


t1.start()
t2.start()

print(s)