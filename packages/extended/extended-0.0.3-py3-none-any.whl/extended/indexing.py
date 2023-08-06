def first(expr, defer=None):
    """
    returns the first item from the collection

    Parameters
    ----------
    expr : iterable
        the list
    defer : any type, optional
        what is returned when nothing is provided in the iterable. The default is None.

    Returns
    -------
    out : item
        first item in the array

    Examples
    --------
    >>> xt.first(['a','b'])
    'a'
    
    >>> xt.first([])
    None

    """
    iter(expr)
    try:        
        return expr[0]
    except IndexError:
        return defer


def last(expr, defer=None):
    """
    returns the last item from the collection

    Parameters
    ----------
    expr : iterable
        the list
    defer : any type, optional
        what is returned when nothing is provided in the iterable. The default is None.

    Returns
    -------
    out : item
        last item in the array

    Examples
    --------
    >>> xt.last(['a','b'])
    'b'
    
    >>> xt.last([])
    None

    """
    iter(expr)
    try:        
        return expr[-1]
    except IndexError:
        return defer
        
    
def rotate_left(input_list,n=1):
    """
    rotates the elements of the list to the left

    Parameters
    ----------
    input_list : iterable
        list of elements to be rotated
    n : int or list, optional
        number of spaces to be rotated. If a list, subsequent numbers rotate along
        subsequent axes. The default is 1 unit on the principle axis of the list.

    Returns
    -------
    out : list
        returns the elements rotated left in the format of a list.

    Examples
    --------
    
    >>> xt.rotate_left(list('abcde'),1)
    ['b', 'c', 'd', 'e', 'a']

    >>> #use negative numbers to rotate the other way
    >>> xt.rotate_left(list('abcde'),n=-1)
    ['e', 'a', 'b', 'c', 'd']
    
    >>> # you can also rotate along the secondary axis only
    >>> xt.rotate_left([['a','b'],['c','d'],['e','f']],[0,1])
    [['b', 'a'], ['d', 'c'], ['f', 'e']]

    >>> # you can just rotate on a single axis as long as it's 
    >>> xt.rotate_left([['a','b'],['c','d'],['e','f']],1)
    [['c', 'd'], ['e', 'f'], ['a', 'b']]

    >>> # is equivalent to
    >>> xt.rotate_left([['a','b'],['c','d'],['e','f']],[1,0])
    [['c', 'd'], ['e', 'f'], ['a', 'b']]


    """
    input_list = list(input_list)
    try: iter(n)
    except: n = [n]
    if n[0]<0:
        n[0] = len(input_list)+n[0]
    if len(n)>1:
        input_list = [rotate_left(i,n[1:]) for i in input_list]
    return input_list[n[0]:]+input_list[:n[0]]



def rotate_right(input_list,n=1):
    """
    rotates the elements of the list to the right

    Parameters
    ----------
    input_list : iterable
        list of elements to be rotated
    n : int or list, optional
        number of spaces to be rotated. If a list, subsequent numbers rotate along
        subsequent axes. The default is 1 unit on the principle axis of the list.

    Returns
    -------
    out : list
        returns the elements rotated right in the format of a list.

    Examples
    --------
    
    >>> xt.rotate_right(list('abcde'),1)
    ['e', 'a', 'b', 'c', 'd']
    
    >>> xt.rotate_right(list('abcde'),-1)
    ['b', 'c', 'd', 'e', 'a']

    >>> # you can also rotate along the secondary axis only
    >>> xt.rotate_right([['a','b'],['c','d'],['e','f']],[0,1])
    [['b', 'a'], ['d', 'c'], ['f', 'e']]

    >>> # you can just rotate on a single axis as long as it's 
    >>> xt.rotate_right([['a','b'],['c','d'],['e','f']],-1)
    [['c', 'd'], ['e', 'f'], ['a', 'b']]

    >>> # is equivalent to
    >>> xt.rotate_right([['a','b'],['c','d'],['e','f']],[-1,0])
    [['c', 'd'], ['e', 'f'], ['a', 'b']]


    """

    try: iter(n)
    except: n = [n]
    return rotate_left(input_list, [-i for i in n])


#%%




# def transpose(arr):
#     return [[i[j] for i in arr] for j in range(max([len(i) for i in arr]))]


# def flatten

# def partition(arr,n):
#     if isinstance(n,up_to):
#         return [arr[n*i:n*i+n] for i in range(int(len(arr) / n) + (len(arr) % n > 0))]
#     else:
#         return [arr[n*i:n*i+n] for i in range(len(arr)//n)]

# def partition(arr,n,d=None):
#     if d is None: d=n    
#     if isinstance(n,up_to): finish = len(arr)
#     else: finish = len(arr)//n*n    
#     return [arr[i:i+n] for i in range(0,finish,d)]


#%%

# class up_to(int):
#     pass


# def partition(expr,n,d=None,k=None,x=None):
#     # print(expr,n,d)
#     if d is None: d=n
#     try: iter(n)
#     except: 
#         n,d = [[n],[d]]
#     if isinstance(n[0],up_to): 
#         finish = len(expr)
#     else: 
#         finish = len(expr)//n[0]*n[0] 

#     if len(n)==1:
#         return [expr[i:i+n[0]] for i in range(0,finish,d[0])]
#     else:
#         expr = [expr[i:i+n[0]] for i in range(0,finish,d[0])]
#         return [partition(expr[i:i+n[0]],n[1:],d[1:],k=k,x=x) for i in expr]
    
    
        
# partition(
# partition(list('abcdefghi'),3)
# ,2,1)

