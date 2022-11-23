import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import (
    get_production_df,
    get_sales_df,
    get_spend_df,
    merge_spend_and_production,
    spend_filter_and_agg,
    PRODUCTION_DF_PATH,
    SALES_DF_PATH,
    SPEND_DF_PATH,
)


def set_session_states():
    if "page" not in st.session_state:
        # Initialize session state.
        st.session_state.update(
            {
                # Default page.
                "page": "Beginner",
                # Default widget values.
                "text": False,
                "button": False,
                "checkbox": False,
                "radio": False,
                "select": False,
                "slider": False,
                "input": False,
                "media": False,
                "columns": False,
                "load": False,
                "expander": False,
                "form": False,
                "metric": False,
                "dataframe": False,
                "pprofiling": False,
                "lottie": False,
                "aggrid": False,
                "sessionstate": False,
                "theme": False,
                "cache": False,
                "multipages": False,
                "leon": False,
                "keyvault": False,
                "ex1": False,
                "ex2": False,
                "ex3": False,
                "ex4": False,
                "ex5": False,
                "ex6": False,
                "ex7": False,
                "ex8": False,
                "ex9": False,
                "ex10": False,
            }
        )


def homepage_content():
    st.subheader("Footsteps Brewing: Spends and Gains")
    st.image("data/Banner.png")
    spend_df = get_spend_df(SPEND_DF_PATH)
    production_df = get_production_df(PRODUCTION_DF_PATH)
    sales_df = get_sales_df(SALES_DF_PATH)

    def matieres_premieres():
        st.subheader("Matières Premières")

        st.markdown(f"**Montant Total:  [{int(spend_df['Prix Total'].sum())}] euros**")
        st.markdown(f"Materiel:  [{int(spend_filter_and_agg(spend_df, ['Materiel']))}] euros")

        expense_summary = []
        for expense_type in [['Malt'], ['Houblons'], ['Levures']]:
            weight_unit = 'Kg'
            if expense_type == "Levures":
                weight_unit = 'g'
            expense_summary.append(
                [
                    expense_type,
                    f'{int(spend_filter_and_agg(spend_df, expense_type, "Quantite"))} {weight_unit}',
                    f'{int(spend_filter_and_agg(spend_df, expense_type, "Prix Total"))} euros',
                ]
            )

        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """

        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        expense_summary = pd.DataFrame(expense_summary, columns=['Type', 'Poids', 'Montant'])
        st.table(expense_summary)

        # st.caption(f"**Montant Total [{int(spend_df['Prix Total'].sum())}] euros**")

    def production():
        st.subheader("Production")
        st.markdown(f"**Volume Total:  [{int(production_df['volume'].sum())}] L**")

    def sales():
        st.subheader("Sales")
        st.markdown(f"**Montant Total:  [{int(sales_df['Payé'].sum())}] Euros**")

    def cost_per_litre():
        st.subheader("Current Avg Cost per Litre")
        avg_cost_per_litre = round(int(spend_df['Prix Total'].sum())/int(production_df['volume'].sum()), 2)
        st.markdown(f"**{avg_cost_per_litre} Euros/L**")

        cost_per_litre_df = merge_spend_and_production(spend_df, production_df)
        fig = px.line(cost_per_litre_df, x=cost_per_litre_df['date'], y=cost_per_litre_df['prix_total_par_litre'])
        # fig.add_shape(
        #     type='line',
        #     x0=cost_per_litre_df.iloc[0]['date'],
        #     y0=avg_cost_per_litre,
        #     x1=cost_per_litre_df.iloc[-1]['date'],
        #     y1=avg_cost_per_litre,
        #     line=dict(color='Red', ),
        #     xref='x',
        #     yref='y'
        # )
        st.plotly_chart(fig, use_container_width=True)

    cost_per_litre()
    matieres_premieres()
    production()
    sales()


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    set_session_states()
    homepage_content()
