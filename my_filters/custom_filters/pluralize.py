def pluralize(num, str_single, str_plural, show_number_first = True):
    """Write the correct pluralization depending on the number"""
    pluralization = str_single if num == 1 else str_plural
    return f"{num} {pluralization}" if show_number_first else pluralization