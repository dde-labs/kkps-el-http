# KKPS: EL-Http

**KKPS Assignment** that Extract & Load data from the [FMP](https://site.financialmodelingprep.com/developer/docs) to Some Local
Database.

It able to use native libs for this case if it does not have any transform or prepare
business logic on this data. If the requirement want to scale the code that able
to implement any business logic in the future, it will refactor the code from native
libs to `duckdb` or `polars` for DataFrame API.

## Prerequisite

- Install Python Dependency requirements,
  ```shell
  python -m pip install -U pip
  pip install -r requirements
  ```

- Getting API token from the FMP and test request the data from below URLs:
  - [Historical Dividends](https://site.financialmodelingprep.com/developer/docs/historical-stock-dividends-api)
  - [Delisted Companies](https://site.financialmodelingprep.com/developer/docs/delisted-companies-api/)

- Provisioning MySQL database with Docker Compose

  - Provisioning

    ```shell
    docker compose -f ./.container/docker-compose.yml --env-file ./.env up -d
    ```

  - Drop
  
    ```shell
    docker compose -f ./.container/docker-compose.yml --env-file ./.env down
    ```
