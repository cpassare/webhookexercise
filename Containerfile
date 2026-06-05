# Use the official Red Hat UBI 9 Minimal image
FROM registry.access.redhat.com/ubi9/ubi-minimal:latest

WORKDIR /app

# Install Python 3 and pip, then clean up the cache to keep the image small
RUN microdnf install -y python3 python3-pip && \
    microdnf clean all

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the webhook application code
COPY app.py .

# Run as an arbitrary non-root user (required by OpenShift default SCCs)
USER 1001

EXPOSE 8443

CMD ["python3", "app.py"]
