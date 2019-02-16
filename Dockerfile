FROM python:alpine3.7

RUN mkdir app
COPY . /app
WORKDIR app

RUN apk add gcc \
            linux-headers \
            musl-dev \
            libffi-dev \
            git \
            #Pynacl
            --virtual .pynacl_deps \
            build-base \
            # Pillow
            jpeg-dev \
            zlib-dev \
            freetype-dev \
            lcms2-dev \
            openjpeg-dev \
            tiff-dev \
            tk-dev \
            tcl-dev \
            harfbuzz-dev \
            fribidi-dev && \
            rm -rf /var/cache/apk/* && \
            pip install -r requirements.txt && \
            pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]


ENTRYPOINT ["python"]
CMD ["-m", "noheavenbot"]
