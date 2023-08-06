'''Utilities for manipulating dictionaries
'''

def get_only_key(d):
    '''Returns the only key in the dictionary
       @throws ValueError if there is more than a single key
    '''
    keys_as_list = list(d.keys())
    if len(keys_as_list) > 1:
        raise ValueError('Asking for only key in a multi-key dictionary')
    return keys_as_list[0]

def get_only_pair(d):
    '''Returns the only <key, value> in the dictionary
       @throws ValueError if there is more than a single key
    '''
    key = get_only_key(d)
    return key, d[key]
