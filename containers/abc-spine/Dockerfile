FROM python:3.10

# Add user to group
RUN groupadd -r appuser && useradd -m --no-log-init -r -g appuser appuser

RUN mkdir -p /app /input /output && chown appuser:appuser /app /input /output

RUN apt-get update && apt-get upgrade -y
RUN apt-get install gcc
#Switch to user
USER appuser

#Set working dir
WORKDIR /app

RUN python -m pip install --user -U pip

# Clone ABC-core
RUN git clone https://github.com/DMcSweeney/abc-core.git abcCore

# Copy main script and models
COPY main.py .
COPY models .

## Install requirements
COPY requirements.txt .

LABEL org.nrg.commands="[{\"name\": \"abc-spine\", \"description\": \"Locates vertebral levels on a CT scan\", \"label\": \"abc-spine\", \"version\": \"1.0\", \"type\": \"docker\", \"image\": \"abc/abc-spine:1.0\", \"command-line\": \"python -m main -i /input -o /output\", \"mounts\": [{\"name\": \"in\", \"writable\": \"false\", \"path\": \"/input\"}, {\"name\": \"out\", \"writable\": \"true\", \"path\": \"/output\"}], \"inputs\": [{\"name\": \"SCAN_ID\", \"description\": \"Scan ID\", \"required\": true}], \"outputs\": [{\"name\": \"output\", \"description\": \"Mask with vertebral levels identified\", \"mount\": \"out\", \"required\": true}], \"xnat\": [{\"name\": \"abc-spine\", \"description\": \"Run spine labelling from ABC toolkit\", \"label\": \"abc-spine\", \"contexts\": [\"xnat:imageScanData\"], \"external-inputs\": [{\"name\": \"scan\", \"description\": \"Input scan\", \"type\": \"Scan\", \"required\": true, \"matcher\": \"'DICOM' in @.resources[*].label\"}], \"derived-inputs\": [{\"name\": \"scan-id\", \"description\": \"Scan id\", \"type\": \"string\", \"derived-from-wrapper-input\": \"scan\", \"derived-from-xnat-object-property\": \"id\", \"provides-value-for-command-input\": \"SCAN_ID\"}, {\"name\": \"scan-dicoms\", \"description\": \"The dicom resource on the scan\", \"type\": \"Resource\", \"derived-from-wrapper-input\": \"scan\", \"provides-files-for-command-mount\": \"in\", \"matcher\": \"@.label == 'DICOM'\"}], \"output-handlers\": [{\"name\": \"spine-output\", \"accepts-command-output\": \"output\", \"as-a-child-of\": \"scan\", \"type\": \"Resource\", \"label\": \"SPINE\"}]}]}]"
