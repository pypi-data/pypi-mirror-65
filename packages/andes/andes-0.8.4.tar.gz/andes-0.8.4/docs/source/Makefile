TXTDIR=markdown
RSTS =$(wildcard *.rst)
MDS=$(patsubst %.rst,$(TXTDIR)/%.md, $(RSTS))

.PHONY : all

all : $(MDS)

$(TXTDIR) :
	mkdir $(TXTDIR)

$(TXTDIR)/%.md : %.rst $(TXTDIR)
	pandoc -f rst -t gfm -s $< -o $@
