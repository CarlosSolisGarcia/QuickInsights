import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Loading the dataset
st.title("Data analyzer demo")
st.write("Welcome to the data analyzer demo, with this app you'll be able to get a quick view of your data")
st.write("Stay tuned for more updates!")

uploaded_file = st.file_uploader(label="Upload the dataset you'd like to preview. Please use a Pandas friendly input file:",
                        )

if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    # Displaying the dataframe:
    st.dataframe(data=dataframe.head())

    ## EDA
    st.subheader("📊 Exploratory Data Analysis")
    st.markdown(
        f"""
            #### Dataset shape:
            - **Number of observations (rows)**: {dataframe.shape[0]}
            - **Number of variables (columns)**: {dataframe.shape[1]} 
        """
                )

    ### Vamos a analizar, columna por columna, el tipo de variable y su info básica
    ### Esta info va a ser:
    # Tipo: numérica, categoríca, texto
    # Número de filas vacías y % sobre total
    # Estadísticas básicas: media, mediana, min, max, std, etc.
    # Distribución de la variable (Testear para tipos: Binomial, Poison, Xi-squared, etc.)

    # Info global del dataset:
    # ¿Hay filas duplicadas? (núm y % sobre total) --> Indicar cómo generar las claves para el recuento

    columns = dataframe.columns
    selected_variable = st.segmented_control(label="Variable",
                          options = columns)

    ### Descripción de la variable:
    # Tipo de dato:
    if selected_variable is not None:

        series_to_analyze = dataframe[selected_variable]

        data_info_tab, data_chart_tab = st.tabs(["Data info", "Chart"])

        with data_info_tab:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("General info")
                st.write(f"Data type: ", series_to_analyze.dtype)
                st.write(f"Missing cells: ", pd.isna(series_to_analyze).sum())
                st.write(f"Missing cells %: ", pd.isna(series_to_analyze).sum() / dataframe.shape[0] * 100)
                st.write(f"Memory usage (kB): ", series_to_analyze.memory_usage() / 1024)

            with col2:
                st.subheader("Statistical info")
                st.write(f"Mean: ", series_to_analyze.mean())
                st.write(f"Median: ", series_to_analyze.median())
                st.write(f"Standard deviation: ", series_to_analyze.std())
                st.write(f"Max: ", series_to_analyze.max())
                st.write(f"Min: ", series_to_analyze.min())

        with data_chart_tab:

            fig, ax = plt.subplots()
            ax.hist(series_to_analyze, bins = 20)
            st.pyplot(fig)

    st.divider()

    st.write(dataframe.describe(include="all"))
    # st.write(dataframe.dtypes)