NAME ?= kafka_exporter

up:
	docker build --no-cache -t $(NAME) .
	docker run -p 5557:5557 $(NAME)
