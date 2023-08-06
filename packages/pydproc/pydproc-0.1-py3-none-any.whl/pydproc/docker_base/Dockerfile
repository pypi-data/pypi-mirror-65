# base image
FROM python:3

# Setup workdir
RUN mkdir /workdir
WORKDIR /workdir

# Add essential files inside image
COPY run_proc.py .
COPY proc.yml .

# Install dependencies
RUN pip3 install pyyaml -q
RUN pip3 install requests -q

# Runs when docker container starts
ENTRYPOINT [ "python", "./run_proc.py" ]
