import uvicorn

from moonlan.server import app


def main():
    uvicorn.run(app, port=3000)


if __name__ == '__main__':
    main()
