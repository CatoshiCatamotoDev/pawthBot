def util_commify(value):
    # Round value (remove value after decimal point)
    # Add comma's to make more readable
    return ("{:,}".format(round(value)))