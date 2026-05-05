run-stress-test-windows:
	powershell -Command "$$env:K6_NO_USAGE_REPORT='true'; k6 run test/test.js"
	powershell -Command "Get-Content test/results.json | ConvertFrom-Json | ConvertTo-Json -Depth 10"

run-stress-test-unix:
	export K6_NO_USAGE_REPORT=true
	k6 run test/test.js > /dev/null 2>&1
	cat test/results.json | jq
