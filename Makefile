run-local-services:
	docker compose -f _DEV/docker-compose.yaml up -d
stop-local-services:
	docker compose -f _DEV/docker-compose.yaml down
	docker compose -f _TEST/docker-compose-test.yaml down
clear-docker:
	docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)
build-test:
	DOCKER_BUILDKIT=1 docker build -f _TEST/dockerfile_test -t fastapi-skeleton-image .
run-test:
	docker-compose -f _TEST/docker-compose-test.yaml run --rm fastapi-skeleton-app
build-benchmark:
	DOCKER_BUILDKIT=1 docker build -f _BENCHMARK/dockerfile -t fastapi-skeleton-benchmark-image .
run-benchmark:
	docker compose -f _BENCHMARK/docker-compose.yaml up -d
	locust -f _BENCHMARK/locustfile.py -H http://localhost