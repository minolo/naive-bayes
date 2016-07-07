SRC_DIR = src
RES_DIR = res
DOC_DIR = ${RES_DIR}/doc

.PHONY: download_res clean

all: download_res

download_res:
	cd ${RES_DIR} && ${MAKE}

clean:
	cd ${RES_DIR} && ${MAKE} clean
