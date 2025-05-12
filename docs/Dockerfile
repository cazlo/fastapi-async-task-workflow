FROM python:3.11-bookworm AS py-build

ENV DEBIAN_FRONTEND noninteractive

# os patch
RUN apt update && apt upgrade -y && rm -rf /var/lib/apt/lists/*


# setup mkdocs
RUN pip install mkdocs==1.6.1

WORKDIR /opt/app

# Install PlantUML Markdown and all Dependencies for local build of images
RUN pip install plantuml-markdown==3.11.1
RUN apt update && \
    apt install -y openjdk-17-jre-headless graphviz && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
ENV PLANTUML_JAVAOPTS="-Djava.awt.headless=true"
ADD https://github.com/plantuml/plantuml/releases/download/v1.2025.2/plantuml-1.2025.2.jar /opt/plantuml/plantuml.jar
RUN echo "#!/bin/bash" > /usr/local/bin/plantuml && \
    echo 'java $PLANTUML_JAVAOPTS -jar /opt/plantuml/plantuml.jar ${@}' >> /usr/local/bin/plantuml && \
    chmod +x /usr/local/bin/plantuml

# Install mermaid2 plugin
RUN pip install mkdocs-mermaid2-plugin==1.2.1

# Install MkDocs as dependency for proper pallete-specific diagram color rendering + nicer ubjectively CSS overall
RUN pip install mkdocs-material==9.6.11

# this is also useful for easier PDF generation if desired
#RUN pip install mkdocs-print-site-plugin

RUN pip install mkdocs-kroki-plugin==0.9.0

COPY mkdocs.yml .
COPY adr_theme adr_theme