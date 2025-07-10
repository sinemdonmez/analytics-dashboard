from flask import request

def build_filters(fields):
    filters = []
    values = []

    for key, clause in fields.items():
        value = request.args.get(key)
        if value:
            if key == "device" and value.lower() == "all":
                continue
            filters.append(clause)
            values.append(value)

    return filters, values
