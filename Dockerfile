FROM python:3.10
RUN pip install git+https://github.com/MoonfaceDev/moonlan.git
ENTRYPOINT moonlan