FROM python:3.9.9

# Copy files
WORKDIR /opt/loggy
COPY ./setup.py ./
COPY ./src ./src/

# Install dependencies
RUN pip3 install -r ./src/requirements.txt

# Install application
RUN python3 setup.py install

# Run loggy
ENTRYPOINT ["loggy"]
CMD []
