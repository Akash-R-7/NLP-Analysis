import streamlit as st
import pandas as pd
from poke_dataloader import all_pokemon, colours
from annotated_text import annotated_text
from visualizations import plot_grouped_bar_chart, plot_scatter_line_chart


def build_sidebar():
    
    poke_name = st.sidebar.selectbox('Select Pokemon 1', all_pokemon, index=100)
    poke_name_2 = st.sidebar.selectbox('Select Pokemon 2', all_pokemon, index=200)

    submit = st.sidebar.button("Compare", type="primary")
    # reset_button = st.sidebar.button("Reset", type="primary")
    if submit:
        return (poke_name, poke_name_2)
    else:
        return (None, None)
    

def comaparsion_columns(pokemon_data, pokemon_data_2, colours):
    poke_type_colors = []

    col1, col2 = st.columns(2, gap="medium")

    with st.container():
        with col1:
            st.header(pokemon_data.get('name').capitalize())
            st.image(pokemon_data.get('sprites').get('front_default'))
            st.write('Pokemon Weight',pokemon_data.get('weight'))
            poke_type = pokemon_data.get('types')[0].get('type').get('name') 
            annotated_text(
                (poke_type,"", colours[poke_type]),
            )
            poke_type_colors.append(colours[poke_type])

        # with col2:
        #     st.header('vs')

        with col2:
            st.header(pokemon_data_2.get('name').capitalize())
            st.image(pokemon_data_2.get('sprites').get('front_default'))
            st.write('Pokemon Weight',pokemon_data_2.get('weight'))
            poke_type = pokemon_data_2.get('types')[0].get('type').get('name') 
            annotated_text(
                (poke_type,"", colours[poke_type]),
            )    
            poke_type_colors.append(colours[poke_type])

    return poke_type_colors


def build_dataframe(pokemon_data, pokemon_data_2, poke_name, poke_name_2):
    stats_data = {stat.get('stat').get('name').capitalize(): stat.get('base_stat') for stat in pokemon_data.get('stats')}
    stats_data_2 = {stat.get('stat').get('name').capitalize(): stat.get('base_stat') for stat in pokemon_data_2.get('stats')}
    stats_df = pd.DataFrame([stats_data,stats_data_2])

    name_col = [poke_name.capitalize(), poke_name_2.capitalize()]

    # Renaming indexes
    stats_df = stats_df.rename(index={0: name_col[0], 1: name_col[1]})
    # stats_df

    transposed_df = stats_df.T
    # transposed_df

    return transposed_df


def build_plots(df, poke_type_colors):
    tab1, tab2 = st.tabs(["Bar Plot", "Line Plot"])

    with st.container():
        with tab1:
            fig = plot_grouped_bar_chart(df, poke_type_colors)
            # with st.container():
            st.plotly_chart(fig)

        with tab2:
            fig = plot_scatter_line_chart(df, poke_type_colors)
            # with st.container():
            st.plotly_chart(fig)