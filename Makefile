app_tag_name = kennyopennix/yc-status-exporter
version = v1.0.0
.PHONY: help
help: ## Help for usage
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build exporter docker image
	docker build -t $(app_tag_name):$(version) -f .
push: ## Push exporter docker image to dockerhub
	docker push $(app_tag_name):$(version)

install-requirements: ## Install requirements from requirements.txt
	pip3 install -r requirements.txt

install-dev-requirements: ## Install requirements from requirements-dev.txt
	pip3 install -r requirements-dev.txt

run-local: ## Run docker compose
	docker compose up -d --build

run-tests: ## Run pytests
	pytest  -v --capture=sys -x --tb=long

stop-local: ## Stop docker compose
	docker compose stop

create-tag: ## Create git tag
	git tag -a $(version)
	git push origin --tags

pre-commit: ## Run pre-commit without committing changes
	git add .
	pre-commit run -a
