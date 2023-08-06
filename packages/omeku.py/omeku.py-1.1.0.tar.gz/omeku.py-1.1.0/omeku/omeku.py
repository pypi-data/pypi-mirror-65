import urllib

from . import http, dict, errors

noresponse = "Couldn't contact the API right now..."


def img(target: str):
    possible = [
        'pat', 'kiss', 'neko', 'hug', 'lick'
    ]

    if target is None:
        raise errors.EmptyArgument("You have to at least define an argument in string format\nArguments: {}".format(possible))

    if target.lower() not in possible:
        raise errors.InvalidArgument("You haven't added any valid arguments\nArguments: {}".format(possible))

    try:
        if target.lower() == "neko":
            r = http.get("/neko")
        else:
            r = http.get("/" + target.lower())
    except Exception as e:
        raise errors.NothingFound(noresponse)

    return r["url"]
