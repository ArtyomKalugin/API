def get_params(coords, typ):
    delta = typ[0] + '~' + typ[1]
    map_params = {
        "ll": ",".join([coords[0], coords[1]]),
        "bbox": delta,
        "l": "map",
        "pt": "{},pm2dgl".format(','.join(coords))
    }

    return map_params