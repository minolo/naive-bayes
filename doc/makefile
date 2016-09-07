PDF_NAME = bayesian_spam_filter.pdf
TMP_DIR = ./tmp.latex
IMG_DIR = img

SRCS = $(wildcard ./*.tex)
IMGS = $(wildcard ./$(IMG_DIR)/*)

PDFLATEX_FLAGS = -interaction=nonstopmode -file-line-error -output-directory=$(TMP_DIR)
PDFLATEX = pdflatex $(PDFLATEX_FLAGS) main.tex | grep '.*:.*:.*' -A 4


.PHONY: all clean

all: $(PDF_NAME)

$(PDF_NAME) : $(TMP_DIR)/main.pdf | $(PDF_DIR)
	cp "${TMP_DIR}/$(notdir $<)" $@

$(TMP_DIR)/main.pdf : main.tex $(SRCS) $(IMGS) bib.bib | $(TMP_DIR)
	@-$(PDFLATEX)
	@-bibtex ${TMP_DIR}/main.aux
	$(PDFLATEX)
	@test -e $@ # Force fail if pdf no exits

$(TMP_DIR) :
	@-mkdir -pv $(TMP_DIR)

$(PDF_DIR) :
	@-mkdir -pv $(PDF_DIR)

clean:
	@-rm -fv $(PDF_NAME) 2>/dev/null; true
	@-rm -frv $(TMP_DIR) 2>/dev/null; true

# vim:filetype=make
