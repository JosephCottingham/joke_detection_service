FROM public.ecr.aws/lambda/python:3.8

# Install OS packages for Pillow-SIMD
# RUN yum -y install tar gzip zlib freetype-devel \
#     gcc \
#     ghostscript \
#     lcms2-devel \
#     libffi-devel \
#     libimagequant-devel \
#     libjpeg-devel \
#     libraqm-devel \
#     libtiff-devel \
#     libwebp-devel \
#     make \
#     openjpeg2-devel \
#     rh-python36 \
#     rh-python36-python-virtualenv \
#     sudo \
#     tcl-devel \
#     tk-devel \
#     tkinter \
#     which \
#     xorg-x11-server-Xvfb \
#     zlib-devel \
#     && yum clean all

COPY requirements.txt ./
RUN python3.8 -m pip install -r requirements.txt
COPY app.py ./
COPY load_model.py ./
COPY .env ./
RUN python3.8 load_model.py
CMD ["app.lambda_handler"]