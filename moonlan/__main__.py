import uvicorn

from moonlan.server import app


def main():
    uvicorn.run(app, host='0.0.0.0', port=3000)


if __name__ == '__main__':
    main()
