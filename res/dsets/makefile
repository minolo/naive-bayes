BASE_URL = http://www.aueb.gr/users/ion/data/enron-spam/preprocessed/
ENRONS_NAMES = \
	enron1 \
	enron2 \
	enron3 \
	enron4 \
	enron5 \
	enron6
ENRONS_SUFFIX = .tar.gz
ENRONS = $(addprefix $(BASE_URL), $(ENRONS_NAMES))

all: $(ENRONS_NAMES)

enron%:
	@echo "Downloading $@"
	@wget -nv --show-progress -O - $(addprefix $(BASE_URL), $@) | tar xz

clean:
	-@rm -vfr enron? 2>/dev/null
