def convert_to_int(currency_str, unit=1):
    """ (str) -> int
    
    convert string type currency value to integer value.
    it removes comma and multiplies its omitted unit.
    
    >>> convert_to_int('123,456', 100)
    12345600
    """
    currency_int = int(currency_str.replace(',','')) * unit
    return currency_int
