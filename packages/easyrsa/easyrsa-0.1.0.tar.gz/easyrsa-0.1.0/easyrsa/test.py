from . import *


def main():
    import sys
    if len(sys.argv[1:]) != 2:
        exit(1)
    from base64 import b64decode, b64encode
    key = b64decode(sys.argv[1])
    content = sys.argv[2]
    if b"PUBLIC KEY" in key:
        p(b64encode(EasyRSA(public_key=key).encrypt(content)).decode("utf-8"))
    elif b"PRIVATE KEY" in key:
        p(EasyRSA(private_key=key).decrypt(content))
    else:
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
