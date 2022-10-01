def set_attributes(obj,data):
    for key, value in data.items():
            setattr(obj, key, value)
    obj.save()
    return obj