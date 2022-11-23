import datetime
from pathlib import Path
from typing import (List, Tuple)

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


def prod_per_month(production_df: pd.DataFrame) -> pd.DataFrame:
    def _map_to_first_day_of_month(in_date: datetime.date) -> datetime.date:
        return datetime.date(year=in_date.year, month=in_date.month, day=1)

    start_date = datetime.date(year=2021, month=11, day=1)
    end_date_max = _map_to_first_day_of_month(datetime.date.today())

    months_of_prod = [start_date]
    end_date = start_date
    while end_date < end_date_max:
        end_date = _map_to_first_day_of_month(end_date + datetime.timedelta(days=32))
        months_of_prod.append(end_date)

    empty_df = pd.DataFrame({'date': months_of_prod, 'volume': [0] * len(months_of_prod)})

    production_df['date'] = production_df['date'].apply(_map_to_first_day_of_month)
    production_df = production_df.groupby('date')['volume'].sum().reset_index()

    merged_df = empty_df.merge(production_df, how='left', on='date').fillna(0)
    merged_df['volume'] = merged_df['volume_x'] + merged_df['volume_y']
    merged_df = merged_df.drop(['volume_x', 'volume_y'], axis=1)

    # add avg
    merged_df['Type'] = ['L/month'] * len(merged_df)

    avg_df = merged_df.copy()
    avg_df.loc[:, 'Type'] = ['All time average'] * len(avg_df)
    avg_df.loc[:, 'volume'] = [round(merged_df['volume'].mean(), 1)] * len(avg_df)

    return pd.concat([merged_df, avg_df])


def get_sales_df(df_path: Path) -> pd.DataFrame:
    def _convert_sales_df(df: pd.DataFrame) -> pd.DataFrame:
        return df
    in_df = pd.read_excel(df_path)
    return _convert_sales_df(in_df)


def merge_spend_and_production(
        spend_df: pd.DataFrame,
        production_df: pd.DataFrame,
        type_filter: List[str] = EXPENSE_TYPES,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    filtered_spend_df = _spend_filter(spend_df, type_filter)
    mergeable_spend_df = filtered_spend_df[['date', 'Prix Total', 'Type']]
    mergeable_spend_df['volume'] = 0

    mergeable_production_df = production_df[['date', 'volume']]
    mergeable_production_df['Prix Total'] = 0
    mergeable_production_df['Type'] = 'na'

    cost_df = mergeable_spend_df.merge(mergeable_production_df, how='outer')

    cost_per_litre_df = cost_df.sort_values(by=['date']).groupby('date')['Prix Total', 'volume'].sum().reset_index()
    cost_per_litre_df['prix_cum'] = cost_per_litre_df['Prix Total'].cumsum()
    cost_per_litre_df['volume_cum'] = cost_per_litre_df['volume'].cumsum()
    cost_per_litre_df['prix_total_par_litre'] = cost_per_litre_df['prix_cum']/cost_per_litre_df['volume_cum']
    cost_per_litre_df['prix_total_par_litre'] = cost_per_litre_df['prix_total_par_litre'].apply(lambda x: round(min(100, x), 1))
    return cost_per_litre_df


def cost_per_kg(spend_df: pd.DataFrame) -> pd.DataFrame:
    sub_spend_df = spend_df[spend_df.Type.isin(['Malt', 'Houblons', 'Levures'])]

    def lambda_func(row: pd.Series):
        if row.loc['Type'] == 'Levures':
           return row.loc['Quantite'] / 10
        elif row.loc['Type'] == 'Houblons':
            return row.loc['Quantite'] * 20
        else:
            return row.loc['Quantite']

    sub_spend_df['weight'] = sub_spend_df.apply(lambda_func, axis=1)
    sub_spend_df.sort_values(by=['Date', 'Type'])
    sub_spend_df['cost_per_package_weight'] = 0 * len(sub_spend_df)
    sub_spend_df['weight_cum'] = 0 * len(sub_spend_df)
    sub_spend_df['cost_cum'] = 0 * len(sub_spend_df)
    for t in ['Malt', 'Houblons', 'Levures']:
        type_sub_spend_df = sub_spend_df[sub_spend_df.Type == t]
        type_sub_spend_df.loc[:, 'weight_cum'] = type_sub_spend_df['weight'].cumsum()
        type_sub_spend_df.loc[:, 'cost_cum'] = type_sub_spend_df['Prix Total'].cumsum()
        sub_spend_df.loc[type_sub_spend_df.index, 'cost_per_package_weight'] = type_sub_spend_df['cost_cum']/ type_sub_spend_df['weight_cum']

    # sub_spend_df['cost_per_package_weight'] = sub_spend_df['Prix Total'] / sub_spend_df['weight']
    return sub_spend_df


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
    prod_per_month_df = prod_per_month(production_df)
    spend_df = get_spend_df(SPEND_DF_PATH)
    cost_per_kg_df = cost_per_kg(spend_df)

    cost_per_litre_df = merge_spend_and_production(spend_df, production_df)

    print()
