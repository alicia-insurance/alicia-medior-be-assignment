BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def base62_encode(num: int) -> str:
    if num == 0:
        return BASE62[0]

    encoding = ""
    base = len(BASE62)

    while num > 0:
        num, rem = divmod(num, base)
        encoding = BASE62[rem] + encoding

    return encoding
