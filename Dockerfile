FROM python:3.9.9

# Set workdir
WORKDIR /opt/loggy

# Install dependencies
COPY ./src/requirements.txt ./
RUN pip3 install -r ./requirements.txt

# Install application
COPY ./setup.py ./
COPY ./src ./src/
RUN python3 setup.py install

# Run loggy
ENTRYPOINT ["loggy"]
CMD []
