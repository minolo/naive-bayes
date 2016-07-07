BIB_DIR = bib
DTS_DIR = dsets

DOWNLOAD_SCRIPT = download_bib.sh

.PHONY: download_bib download_dsets clean

all: download_bib download_dsets

download_bib:
	cd ${BIB_DIR} && ./${DOWNLOAD_SCRIPT}

download_dsets:
	cd ${DTS_DIR} && ${MAKE}

clean:
	-@ cd ${BIB_DIR} && rm -fv *.pdf 2> /dev/null
	cd ${DTS_DIR} && ${MAKE} clean
