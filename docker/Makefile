all: app

app:
	@make -s help

help:
	@echo "make help                         - show this help."
	@echo "make build                        - build docker and it's environment."
	@echo "make run							 - run docker."
	@echo "make clean                        - cleanup docker kitchen."

build:
	sudo touch ../weather_results.csv
	sudo docker-compose build

run:
	sudo docker-compose up

clean:
	sudo rm -rf ../htmlcov/
	sudo rm -f ../weather_results.csv
	sudo docker system prune -a --volumes
