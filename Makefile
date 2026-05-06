up:
	docker compose up --build

run-stress-test-windows:
	powershell -Command "$$env:K6_NO_USAGE_REPORT='true'; k6 run test/test.js"
	powershell -Command "Get-Content test/results.json | ConvertFrom-Json | ConvertTo-Json -Depth 10"

run-stress-test-unix:
	export K6_NO_USAGE_REPORT=true
	k6 run test/test.js > /dev/null 2>&1
	cat test/results.json | jq

install-k6:
	curl -fsSL https://dl.k6.io/key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/k6-archive-keyring.gpg
	echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
	sudo apt-get update
	sudo apt-get install k6
