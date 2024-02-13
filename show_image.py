import base64
import sys


def write(data: bytes) -> None:
    sys.stdout.buffer.write(data)
    sys.stdout.flush()


def write_png_image(path: str) -> None:
    with open(path, "rb") as fp:
        data = base64.standard_b64encode(fp.read())

        write(b"\033_Ga=T,f=100,m=1;\033\\")

        while data:
            payload, data = data[:4096], data[4096:]

            write(b"\033_Gm=1;" + payload + b"\033\\")

        write(b"\033_Gm=0;\033\\")


if __name__ == "__main__":
    write_png_image(sys.argv[1])
