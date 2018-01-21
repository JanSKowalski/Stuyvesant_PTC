all:
	(. flask/bin/activate)
	sleep 2
	python run.py

clean:
	-rm -rf *~
	-rm -rf *.pyc
