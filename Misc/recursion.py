def mymax(a, b):
    if (a >= b):
        return a
    else:
        return b

def themax(l):
    if len(l) == 1:
        return l[0]
    
    elif len(l) == 2:
        return mymax(l[0], l[1])
    
    else:
        return mymax(mymax(l[0], l[1]), themax(l[2:]))
    
def isSorted(l):
    if len(l) == 1:
        return True
    
    elif l[0] == themax(l):
        return isSorted(l[1:])
    
    else:
        return False        
    
def slowSort(l):
    if isSorted(l):
        return l
    
    elif l[0] == themax(l):
        return [l[0]] + list(slowSort(l[1:]))
    
    else:
        return list(slowSort(l[1:] + [l[0]]))

def merge(a, b):
    if len(a) == 0:
        return b
    elif len(b) == 0:
        return a
    elif a[0] < b[0]:
        return [a[0]] + merge(a[1:], b)
    else:
        return [b[0]] + merge(a, b[1:])
    
def mergesort(x):
    if len(x) < 2:
        return x
    else:
        h = len(x) // 2
        return merge(mergesort(x[:h]), mergesort(x[h:]))
    

        
