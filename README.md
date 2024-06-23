# KKPS: EL-Http

**KKPS Assignment** that Extract & Load data from the [FMP](https://site.financialmodelingprep.com/developer/docs) to Some Local
Database (This example use **MySQL**).

It able to use native libs for this case if it does not have any transform or prepare
business logic on this data. If the requirement want to scale the code that able
to implement any business logic in the future, it will refactor the code from native
libs to `duckdb` or `polars` for DataFrame API.

> [!NOTE]
> When I implement with native libs it also improve performance and less deps. So,
> it uses time to develop this EL around ~ 6-7 hours (1 MD).

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

  - Drop all resources without image
  
    ```shell
    docker compose -f ./.container/docker-compose.yml --env-file ./.env down -v
    ```

## Getting Started

- Create the dotenv file, `.env` and define the the value of necessary keys:

  ```dotenv
  FMP_API_TOKEN=????
  MYSQL_USER=????
  MYSQL_PASSWORD=????
  MYSQL_ROOT_PASSWORD=????
  ```
  
  Optional keys for dynamic symbol for EL the Historical Dividends data.

  ```dotenv
  FMP_HIST_DIVID_SYMBOLS=AAPL,AAQC,ACP
  ```

- Initial the Tables on Database
  
  ```console
  (env) $ python ./src/db.py
  Creating table hist_devidends: OK
  Creating table delisted_comp: OK
  ```

- Start Main Program

  ```console
  (env) $ python ./main.py
  Success EL: Historical Dividends (AAPL) with 83 rows.
  Success EL: Historical Dividends (ACP) with 159 rows.
  Success EL: Historical Dividends (AAQC) with 0 rows.
  Success EL: Delisted Companies with 100 rows.
  ```
