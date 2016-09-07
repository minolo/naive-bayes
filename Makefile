SRC_DIR = src
RES_DIR = res
TST_DIR = tests
DOC_DIR = doc

.PHONY: download_res tests doc clean

all: download_res doc

download_res:
	cd ${RES_DIR} && ${MAKE}

doc: tests
	cd ${DOC_DIR} && ${MAKE}

tests:
	cd ${TST_DIR} && ${MAKE}

clean:
	cd ${DOC_DIR} && ${MAKE} clean
	cd ${RES_DIR} && ${MAKE} clean
	cd ${TST_DIR} && ${MAKE} clean

mrproper:
	cd ${DOC_DIR} && ${MAKE} clean
	cd ${RES_DIR} && ${MAKE} clean
	cd ${TST_DIR} && ${MAKE} mrproper
