SRC_DIR = src
RES_DIR = res
TST_DIR = tests
DOC_DIR = ${RES_DIR}/doc

.PHONY: download_res tests clean

all: download_res tests

download_res:
	cd ${RES_DIR} && ${MAKE}

tests:
	cd ${TST_DIR} && ${MAKE}

clean:
	cd ${RES_DIR} && ${MAKE} clean
	cd ${TST_DIR} && ${MAKE} clean
