import nanowebserver


def req(data:dict):
    return 'The server is working great!'


nanowebserver.NanoWeb(req)