import datetime
from pathlib import Path
from typing import List

import pandas as pd


DATA_FOLDER = Path('data')
SPEND_DF_PATH = DATA_FOLDER.joinpath('spend.xlsx')
PRODUCTION_DF_PATH = DATA_FOLDER.joinpath('production.xlsx')
SALES_DF_PATH = DATA_FOLDER.joinpath('sales.xlsx')

EXPENSE_TYPES = ['Materiel', 'Malt', 'Houblons', 'Levures', 'Adjuncts', 'Extra', 'Bouteilles', 'Livraison']


def _spend_filter(df: pd.DataFrame, expense_types: List[str]) -> pd.DataFrame:
    """Return sum of spend for a particular expense_type"""
    return df[df.Type.isin(expense_types)]


def spend_filter_and_agg(df: pd.DataFrame, expense_types: List[str], agg_col: str = "Prix Total") -> int:
    return int(_spend_filter(df, expense_types)[agg_col].sum())


def get_spend_df(df_path: Path) -> pd.DataFrame:
    def _convert_spend_df(in_df: pd.DataFrame) -> pd.DataFrame:
        df = in_df.dropna(how='all')
        df.index = range(len(df))
        df['date'] = df.Date.apply(lambda x: x.date())
        df.drop(columns=['Date'])
        return df

    in_df = pd.read_excel(df_path)
    return _convert_spend_df(in_df)


def get_production_df(df_path: Path) -> pd.DataFrame:
    def _convert_production_df(df: pd.DataFrame) -> pd.DataFrame:
        df.columns = ['date', 'beer_name', 'volume']
        df['date'] = df['date'].apply(excel_date_processor)
        return df

    in_df = pd.read_excel(df_path)
    return _convert_production_df(in_df)


def get_sales_df(df_path: Path) -> pd.DataFrame:
    def _convert_sales_df(df: pd.DataFrame) -> pd.DataFrame:
        return df
    in_df = pd.read_excel(df_path)
    return _convert_sales_df(in_df)


def merge_spend_and_production(
        spend_df: pd.DataFrame,
        production_df: pd.DataFrame,
        type_filter: List[str] = EXPENSE_TYPES
) -> pd.DataFrame:
    filtered_spend_df = _spend_filter(spend_df, type_filter)
    mergeable_spend_df = filtered_spend_df[['date', 'Prix Total']]
    mergeable_spend_df['volume'] = 0

    mergeable_production_df = production_df[['date', 'volume']]
    mergeable_production_df['Prix Total'] = 0

    cost_df = mergeable_spend_df.merge(mergeable_production_df, how='outer')
    cost_df = cost_df.sort_values(by=['date']).groupby('date').sum()
    cost_df['prix_cum'] = cost_df['Prix Total'].cumsum()
    cost_df['volume_cum'] = cost_df['volume'].cumsum()
    cost_df['prix_total_par_litre'] = cost_df['prix_cum']/cost_df['volume_cum']
    cost_df['prix_total_par_litre'] = cost_df['prix_total_par_litre'].apply(lambda x: round(min(100, x), 1))
    cost_df['date'] = cost_df.index
    return cost_df


def excel_date_processor(str_full_date: str) -> datetime.date:
    """'lundi, novembre 01, 2022' -> """
    month_str_to_int_map = {
        'janvier': 1,
        'février': 2,
        'mars': 3,
        'avril': 4,
        'mai': 5,
        'juin': 6,
        'juillet': 7,
        'août': 8,
        'septembre': 9,
        'octobre': 10,
        'novembre': 11,
        'décembre': 12,
    }
    date_split = str_full_date.split(',')
    year = int(date_split[2])
    day = int(date_split[1].strip(' ').split(' ')[1])
    month = month_str_to_int_map[date_split[1].strip(' ').split(' ')[0]]
    return datetime.date(day=day, month=month, year=year)


if __name__ == "__main__":
    sales_df = get_sales_df(SALES_DF_PATH)
    production_df = get_production_df(PRODUCTION_DF_PATH)
    spend_df = get_spend_df(SPEND_DF_PATH)

    cost_per_litre_df = merge_spend_and_production(spend_df, production_df)
    import plotly.express as px
    px.line(cost_per_litre_df, x=cost_per_litre_df['date'], y=cost_per_litre_df['prix_total_par_litre'])
    print()
