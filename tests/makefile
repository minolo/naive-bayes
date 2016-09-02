TESTS_DIR=../tests
SRC_DIR=../src
TESTER=tester.sh
PLOTTER=python ${SRC_DIR}/plotter.py

TESTS=$(wildcard *.test)
OUTS=$(wildcard *.out)
PNGS=$(TESTS:.test=.png)

# Do not delete my precious data if plotter fails! >:(
.SECONDARY: $(OUTS)

all: ${PNGS}

%.png: %.out
	$(PLOTTER) -d $<

%.out: %.test
	cd $(SRC_DIR) && $(TESTER) -t $(TESTS_DIR)/$<

clean:
	@-rm -vf *.png

mrproper:
	@-rm -vf *.png
	@-rm -vf *.out
