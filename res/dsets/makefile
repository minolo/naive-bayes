BASE_URL = http://www.aueb.gr/users/ion/data/enron-spam/preprocessed/
ENRONS_NAMES = \
	enron1 \
	enron2 \
	enron3 \
	enron4 \
	enron5 \
	enron6
ENRONS_SUFFIX = .tar.gz

all: $(ENRONS_NAMES)

enron%:
	@echo "Downloading $@"
	@wget -nv --show-progress -O - $(addsuffix $(ENRONS_SUFFIX), $(addprefix $(BASE_URL), $@)) | tar xz

clean:
	-@rm -fr enron? 2>/dev/null
