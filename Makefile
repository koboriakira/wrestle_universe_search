cdk-test:
	cd cdk && npm run test

.PHONY: pull-episode
pull-episode:
	@cd src && python-lambda-local -f handler -t 900 pull_episode.py ../.events/pull_episode.json

dev:
	docker compose up -d
	open http://localhost:10125/docs
