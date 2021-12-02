"""
Memory connector based on the following doc https://trino.io/docs/current/connector/memory.html

Mostly used for testing and CI/CD

Example yaml config to use this connector
```yaml
offline_store:
    type: feast_trino.trino.TrinoOfflineStore
    host: localhost
    port: 8080
    catalog: memory
    dataset: ci
    connector:
        path: feast_trino.connectors.memory
```
"""

from typing import Any, Dict, Optional

import pandas as pd

from feast_trino.connectors.utils import (
    CREATE_SCHEMA_QUERY_TEMPLATE,
    INSERT_ROWS_QUERY_TEMPLATE,
    format_pandas_row,
    pandas_dataframe_fix_batches,
    trino_table_schema_from_dataframe,
)
from feast_trino.trino_utils import Trino


def upload_pandas_dataframe_to_trino(
    client: Trino,
    df: pd.DataFrame,
    table_ref: str,
    connector_args: Optional[Dict[str, Any]] = None,
) -> None:
    client.execute_query(
        CREATE_SCHEMA_QUERY_TEMPLATE.format(
            table_ref=table_ref,
            schema=trino_table_schema_from_dataframe(df=df),
            with_statement="",
        )
    )

    # Upload batchs of 1M rows at a time
    for batch_df in pandas_dataframe_fix_batches(df=df, batch_size=1000000):
        client.execute_query(
            INSERT_ROWS_QUERY_TEMPLATE.format(
                table_ref=table_ref,
                columns=",".join(batch_df.columns),
                values=format_pandas_row(batch_df),
            )
        )
