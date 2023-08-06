def tally(expr, test=lambda x:x):
    """
    tallies all items in expr using test as the criteria.  The default test is none; just
    tally the items in the list.

    Parameters
    ----------
    expr : list
        list of items to be tallied
    test : function
        test to be applied to each item to determine if the items are tallied together
    
    Returns
    -------
    out : list
        list of lists with the items tallied up.  If you use a nested list,
        the items get returned as a tuple.  If you use a dictionary, you'll
        only get the keys.  
    
    Examples
    --------
    >>> xt.tally(['a','a','b','a','c','b','a'])
    [['a', 4], ['b', 2], ['c', 1]]
    
    >>> # you can use objects as tallied items
    >>> import sympy as sp
    >>> sp.var('a b c')
    >>> xt.tally([a,a,b,a,c,b,a])
    [[a, 4], [b, 2], [c, 1]]
    
    >>> # if you nest in a list, it gets returned as a tuple
    >>> xt.tally([[1,2],[3,4],[3,4]])
    [[(1, 2), 1], [(3, 4), 2]]

    >>> # numpy arrays behave just like lists
    >>> xt.tally([np.array([1,2]),np.array([3,4]),np.array([1,2])])
    [[(1, 2), 2], [(3, 4), 1]]
        
    
    >>> # tests of items return just the 
    >>> xt.tally([[1,2],[2,3],[1,2],[1,1]],test=xt.first)
    [[(1, 2), 3], [(2, 3), 1]]
    
    >>> # it's not recommended to use on dicts or sets or other unordered collections
    >>> # as elements since the order upon exit cannot be guaranteed. Turn these 
    >>> # into lists first
    >>> xt.tally([{'a','b','c'}])
    [[('b', 'c', 'a'), 1]]
    """

    D = {} #stores the tallies
    E = {} #stores the test definitions
    for i in expr:
        try:
            iter(i)
        except:
            pass
        else:
            if not isinstance(i,str):
                i = tuple(i)
        try:
            D[test(i)]+=1
        except KeyError:
            E[test(i)] = i
            D[test(i)] = 1           
    return [[E[k],v] for k,v in D.items()]


def counts(expr):
    """
    returns a count of each item in the list as a dict

    Parameters
    ----------
    expr : iterable
        the list with elements that need tallied.

    Returns
    -------
    out : dict
        the keys are the items and the values are the counts

    >>> xt.counts(['a','a','b','a','c','b','a'])
    {'a': 4, 'b': 2, 'c': 1}
    
    >>> # you can use objects as tallied items
    >>> import sympy as sp
    >>> sp.var('a b c')
    >>> xt.counts([a,a,b,a,c,b,a])
    {a: 4, b: 2, c: 1}
    
    >>> # if you nest in a list, it gets returned as a tuple
    >>> xt.counts([[1,2],[3,4],[3,4]])
    {(1, 2): 1, (3, 4): 2}

    >>> # numpy arrays behave just like lists
    >>> xt.counts([np.array([1,2]),np.array([3,4]),np.array([1,2])])
    {(1, 2): 2, (3, 4): 1}
        
    >>> # it's not recommended to use on dicts or sets or other unordered collections
    >>> # as elements since the order upon exit cannot be guaranteed. Turn these 
    >>> # into lists first
    >>> xt.counts([{'a','b','c'}])
    {('c', 'b', 'a'): 1}

    """
    return {k:v for k,v in tally(expr)}


def counts_by(expr, test=lambda x:x):
    """
    returns a count of each item in the list as a dict

    Parameters
    ----------
    expr : iterable
        the list with elements that need tallied.

    Returns
    -------
    out: dict
        the keys are the items and the values are the counts

    >>> xt.counts_by(['a','a','b','a','c','b','a'])
    {'a': 4, 'b': 2, 'c': 1}
    
    >>> # you can use objects as tallied items
    >>> import sympy as sp
    >>> sp.var('a b c')
    >>> xt.counts_by([a,a,b,a,c,b,a])
    {a: 4, b: 2, c: 1}
    
    >>> # if you nest in a list, it gets returned as a tuple
    >>> xt.counts_by([[1,2],[3,4],[3,4]])
    {(1, 2): 1, (3, 4): 2}

    >>> # numpy arrays behave just like lists
    >>> xt.counts_by([np.array([1,2]),np.array([3,4]),np.array([1,2])])
    {(1, 2): 2, (3, 4): 1}
        
    
    >>> # tests of items return just the first item that satisfies the condition
    >>> xt.counts_by([[1,2],[2,3],[1,2],[1,1]],test=xt.first)
    {(1, 2): 3, (2, 3): 1}
    
    >>> # it's not recommended to use on dicts or sets or other unordered collections
    >>> # as elements since the order upon exit cannot be guaranteed. Turn these 
    >>> # into lists first
    >>> xt.counts_by([{'a','b','c'}])
    {('c', 'b', 'a'): 1}

    """
    return {k:v for k,v in tally(expr, test=test)}
    

