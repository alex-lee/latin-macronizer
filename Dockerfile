FROM python:3.12-slim

RUN apt-get update -qq \
    && apt-get install --yes -qq \
    build-essential \
    curl \
    git \
    libfl-dev \
    procps \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/latin-macronizer

# Build morpheus.
RUN git clone --depth=1 https://github.com/Alatius/morpheus.git
RUN cd morpheus/src \
    && make \
    && make install \
    && cd .. \
    && ./update.sh \
    && ./update.sh

# Install RFTagger.
RUN curl -sSL -o RFTagger.zip https://www.cis.uni-muenchen.de/~schmid/tools/RFTagger/data/RFTagger.zip \
    && echo '598f467a37ed3722aa547d12f13877c242197cefcec7edc004b8c1713b3ab3ed  RFTagger.zip' \
    | sha256sum -c - \
    && unzip RFTagger.zip \
    && rm RFTagger.zip \
    && cd RFTagger/src \
    && make \
    && make install \
    && cd ../.. \
    && rm -rf ./RFTagger

# Install python dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files.
COPY *.txt *.py *.sh pyproject.toml ./
COPY macronizer ./macronizer
RUN pip install -e .

# # Initialize data.
RUN git clone --depth=1 https://github.com/Alatius/treebank_data.git \
    && ./train-rftagger.sh \
    && macronize --initialize \
    && rm -rf ./treebank_data

CMD /bin/bash

ENV TRUNCATETHRESHOLD=-1
