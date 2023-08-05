keys = []
values = []
ROWS = {}
def pack(dictionary, nameName):
    for name1 in dictionary.keys():
        if type(dictionary[name1]) != dict:
            keys.append('{}_'.format(nameName) + name1)
            values.append(dictionary[name1])
        else:
            pack(dictionary[name1], nameName)
    res = {keys[i]: values[i] for i in range(len(keys))} 
    return res

def square(x):
	return x ** 2