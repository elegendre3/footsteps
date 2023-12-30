import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import (
    cost_per_kg,
    get_production_df,
    get_sales_df,
    get_spend_df,
    merge_spend_and_production,
    PRODUCTION_DF_PATH,
    prod_per_month,
    SALES_DF_PATH,
    SPEND_DF_PATH,
    spend_filter_and_agg,
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

        def show_table():
            expense_summary = []
            for expense_type in [['Malt'], ['Houblons'], ['Levures']]:
                weight_unit = 'Kg'
                if expense_type[0] == "Levures":
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
        show_table()

        def plot_pie_breakdown():
            spend_df_sum = spend_df.groupby('Type').sum().reset_index()
            fig = px.pie(spend_df_sum, values='Prix Total', names='Type', title="Cost breakdown")
            st.plotly_chart(fig, use_container_width=True)

        plot_pie_breakdown()

        def plot_spend_over_time():
            spend_df.sort_values(by=['date'])
            type_to_remove = ['Materiel', 'REDUC']

            spends_per_type = spend_df[~spend_df.Type.isin(type_to_remove)].sort_values(by=['date'])
            fig = px.area(
                spends_per_type.groupby(['date', 'Type'])['Prix Total'].sum().reset_index(),
                x='date',
                y='Prix Total',
                color='Type',
                title="Depenses dans le temps"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("NB: En excluant les dépenses 'Materiel'")
        plot_spend_over_time()

        def plot_cost_per_kg():
            cost_per_kg_df = cost_per_kg(spend_df)
            fig = px.line(cost_per_kg_df, x='Date', y='cost_per_package_weight', color='Type', title="Evolution des prix/poids")
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Malt/kg --  Houblons/50g -- Levures/10g")
        plot_cost_per_kg()

    def production():
        st.subheader("Production")
        st.markdown(f"**Volume Total:  [{int(production_df['volume'].sum())}] L**")

        def plot_prod_over_time():
            prod_per_month_df = prod_per_month(production_df)
            st.markdown(f"**Moyenne par mois:  [{prod_per_month_df[prod_per_month_df.Type == 'All time average'].iloc[0].volume}] L**")
            fig = px.line(
                prod_per_month_df,
                x='date',
                y='volume',
                color='Type',
                title="Production dans le temps"
            )
            # fig.add_shape(
            #     type='line',
            #     x0=prod_per_month_df.iloc[0]['date'],
            #     y0=avg_prod_per_month,
            #     x1=prod_per_month_df.iloc[-1]['date'],
            #     y1=avg_prod_per_month,
            #     line=dict(color='Red', ),
            #     # xref='x',
            #     # yref='y'
            # )
            st.plotly_chart(fig, use_container_width=True)
        plot_prod_over_time()

        st.caption("Time graph L/week for period of spend")

    def sales():
        st.subheader("Sales")
        st.markdown(f"**Montant Total:  [{int(sales_df['Payé'].sum())}] Euros**")

    def cost_per_litre():
        st.subheader("Current Avg [Cost] per Litre")
        avg_cost_per_litre = round(int(spend_df['Prix Total'].sum())/int(production_df['volume'].sum()), 2)
        st.markdown(f"**{avg_cost_per_litre} Euros/L**")

        cost_per_litre_df= merge_spend_and_production(spend_df, production_df)
        fig = px.line(cost_per_litre_df, x=cost_per_litre_df['date'], y=cost_per_litre_df['prix_total_par_litre'])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Current Avg [Cost - Materiel] per Litre")
        sub_spend_df = spend_df[~spend_df.Type.isin(['Materiel'])]
        avg_cost_per_litre = round(int(sub_spend_df['Prix Total'].sum()) / int(production_df['volume'].sum()), 2)
        st.markdown(f"**{avg_cost_per_litre} Euros/L**")

        cost_moins_materiel_per_litre_df = merge_spend_and_production(sub_spend_df, production_df)
        fig2 = px.line(cost_moins_materiel_per_litre_df, x='date', y='prix_total_par_litre')
        fig2.update_traces(line_color='#ca2b3b')
        st.plotly_chart(fig2, use_container_width=True)

    cost_per_litre()
    matieres_premieres()
    production()
    sales()


if __name__ == "__main__":
    st.set_page_config(page_title='FOOTSTEPS', page_icon='data/logo_footsteps_round.png', layout="wide")
    set_session_states()
    homepage_content()
