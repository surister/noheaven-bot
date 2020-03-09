FROM python:alpine3.7

RUN mkdir app
COPY . /app
WORKDIR app

RUN apk add --no-cache --virtual .build-deps \
            gcc \
            linux-headers \
            musl-dev \
            libffi-dev \
            git \
	    ffmpeg \
            #Pynacl
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

            pip install -r requirements.txt && \
            apk del .build-deps && \
            rm -rf /var/cache/apk/*


ENTRYPOINT ["python"]
CMD ["-m", "noheavenbot"]
