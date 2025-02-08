from typing import List, Dict
import pandas as pd

from FinanceETL.utils.warren_buffet import WarrenBuffets


class DataTransformer:
    @staticmethod
    def transform_company(raw_data: List[Dict]):
        wb = WarrenBuffets()
        transformed_data = []
        for company in raw_data:
            df = pd.DataFrame(company)
            df = wb.applyAll(df)
            transformed_data.append(df)
        df_result = pd.concat(transformed_data, ignore_index=True)
        return df_result
        # check_company(df['symbol'].iloc[0])
