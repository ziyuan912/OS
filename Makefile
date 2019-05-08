CFLAG = -DDEBUG -Wall -std=c99

main: main.o schedule.o processer.o
	gcc $(CFLAG) main.o schedule.o processer.o -o main
main.o: main.c Makefile
	gcc $(CFLAG) main.c -c
schedule.o: schedule.c schedule.h Makefile
	gcc $(CFLAG) schedule.c -c
processer.o: processer.c processer.h Makefile
	gcc $(CFLAG) processer.c -c
clean:
	rm -rf *o
run:
	sudo ./main
