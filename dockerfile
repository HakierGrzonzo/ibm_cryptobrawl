FROM archlinux

RUN pacman -Syu python python-pip geckodriver firefox --noconfirm
RUN pip3 install selenium pycoingecko

COPY ./api/ /api

WORKDIR /
ENTRYPOINT python3 -m api
