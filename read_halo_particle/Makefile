#CODE="python"
CODE="C"

#================================================================================
FFTW_INCL  = #-I/home/maotx/local/fftw-3.3.5/include
FFTW_LIBS  = #-L/home/maotx/local/fftw-3.3.5/lib -lfftw3
#================================================================================
ifeq ($(CODE),"C")
EXEC   	=  	run
#OBJS   	=  	mygroupstuff.o show_group.o
OBJS   	=  	mygroupstuff.o get_spherical_region.o
OPTIMIZE= 	-Wall -O -g
endif

ifeq ($(CODE),"python")
EXEC   	=  	pylib.so
OBJS   	=  	mygroupstuff.o show_group_py.o
OPTIMIZE= 	-Wall -O -g -fPIC -shared
endif

CC     	= 	gcc
INCL  	=  	$(FFTW_INCL)
CFLAGS 	=   $(OPTIMIZE) $(OPT) $(INCL)
LIBS   	=   -lm $(FFTW_LIBS)
#****************************************
$(EXEC): $(OBJS) 
	$(CC) $(OBJS) $(LIBS) $(CFLAGS) -o $(EXEC)  

clean:
	rm -f $(OBJS) $(EXEC)
#================================================================================
