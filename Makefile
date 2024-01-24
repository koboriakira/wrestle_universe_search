cdk-test:
	cd cdk && npm run test

.PHONY: test-scraping
test-scraping:
	@python-lambda-local -f handler -t 900 src/handlers/scraping.py ./.events/scraping_sample.json
