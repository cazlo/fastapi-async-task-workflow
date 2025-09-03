FROM python:3.13-bookworm AS py-build

ENV DEBIAN_FRONTEND noninteractive

# os patch
RUN apt update && apt upgrade -y && rm -rf /var/lib/apt/lists/*

# renovate: datasource=pypi depName=mkdocs versioning=pep440
ENV MKDOCS_VERSION="1.6.1"
# setup mkdocs
RUN pip install mkdocs==${MKDOCS_VERSION}

WORKDIR /opt/app

# renovate: datasource=pypi depName=plantuml-markdown versioning=pep440
ENV PLANTUML_MARKDOWN_VERSION="3.11.1"
# Install PlantUML Markdown and all Dependencies for local build of images
RUN pip install plantuml-markdown==${PLANTUML_MARKDOWN_VERSION}

# renovate: datasource=repology depName=debian_12/openjdk-17 versioning=loose
ENV OPENJDK_VERSION="17.0.16+8-1~deb12u1"
# renovate: datasource=repology depName=debian_12/graphviz versioning=loose
ENV GRAPHVIZ_VERSION="2.42.2-7+deb12u1"
RUN apt update && \
    apt install -y openjdk-17-jre-headless=${OPENJDK_VERSION} graphviz=${GRAPHVIZ_VERSION} && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
ENV PLANTUML_JAVAOPTS="-Djava.awt.headless=true"
# renovate: datasource=github-releases depName=plantuml/plantuml
ENV PLANTUML_VERSION="1.2025.4"
ADD https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar /opt/plantuml/plantuml.jar
RUN echo "#!/bin/bash" > /usr/local/bin/plantuml && \
    echo 'java $PLANTUML_JAVAOPTS -jar /opt/plantuml/plantuml.jar ${@}' >> /usr/local/bin/plantuml && \
    chmod 755 /usr/local/bin/plantuml /opt/plantuml/plantuml.jar

# renovate: datasource=pypi depName=mkdocs-mermaid2-plugin versioning=pep440
ENV MKDOCS_MERMAID2_VERSION="1.2.2"
# Install mermaid2 plugin
RUN pip install mkdocs-mermaid2-plugin==${MKDOCS_MERMAID2_VERSION}

# renovate: datasource=pypi depName=mkdocs-material versioning=pep440
ENV MKDOCS_MATERIAL_VERSION="9.6.18"
# Install MkDocs as dependency for proper pallete-specific diagram color rendering + nicer ubjectively CSS overall
RUN pip install mkdocs-material==${MKDOCS_MATERIAL_VERSION}

# this is also useful for easier PDF generation if desired
#RUN pip install mkdocs-print-site-plugin

# renovate: datasource=pypi depName=mkdocs-kroki-plugin versioning=pep440
ENV MKDOCS_KROKI_VERSION="0.9.0"
RUN pip install mkdocs-kroki-plugin==${MKDOCS_KROKI_VERSION}

COPY mkdocs.yml .
COPY adr_theme adr_theme