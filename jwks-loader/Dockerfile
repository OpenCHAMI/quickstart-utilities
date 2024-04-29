FROM cgr.dev/chainguard/wolfi-base

RUN apk add python-3.12 py3.12-pip

# Copy only requirements file to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/* /usr/local/bin/

ENTRYPOINT ["/usr/bin/python", "/usr/local/bin/jwks_to_pem.py"]
