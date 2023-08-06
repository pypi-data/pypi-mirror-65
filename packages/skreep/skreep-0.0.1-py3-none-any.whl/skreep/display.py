def display(obj, set='default'):

    if 'default' == set:
        return obj.text
    
    if 'list' == set:
        return [i.text for i in obj]