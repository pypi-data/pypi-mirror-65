Testery CLI
v1.1.1

To install you must have Python 3 installed and pip, then,

```
pip install --upgrade testery
```

To kick off a test run,

```
testery create-test-run --token <yourTesteryApiToken> --project <projectKeyFromTestery> --build-id <uniqueBuildIdOfYourChoice> --environment <environmentToBeTested> --wait-for-results --output pretty
```

When set, `--fail-on-failure`, will return an exit code of 1 if there are test failures.


*Output Formats*

- teamcity
- pretty
- json
- appveyor
- octopus


