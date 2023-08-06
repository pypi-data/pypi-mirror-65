from . import *


def main():
    import sys
    if len(sys.argv[1:]) != 2:
        exit(1)
    key = sys.argv[1]
    content = sys.argv[2]
    if "PUBLIC KEY" in key:
        p(EasyRSA(public_key=key.encode("utf-8")).encrypt(content))
    elif "PRIVATE KEY" in key:
        p(EasyRSA(private_key=key.encode("utf-8")).decrypt(content))
    else:
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
