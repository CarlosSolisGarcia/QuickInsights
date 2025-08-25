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
    ### Setting up the statistics to show:
    dataframe_num_rows = dataframe.shape[0]
    dataframe_num_cols = dataframe.shape[1]
    dataframe_num_missing_values = dataframe.isna().sum().sum()
    dataframe_percentage_missing_values = dataframe.isna().sum().sum() / dataframe.size * 100
    dataframe_num_duplicates = dataframe.duplicated().sum()
    dataframe_percentage_duplicates = dataframe_num_duplicates / dataframe_num_rows * 100

    st.subheader("📊 Exploratory Data Analysis")
    st.markdown(
        f"""
            #### Dataset shape:
            - **Number of observations (rows)**: {dataframe_num_rows}
            - **Number of variables (columns)**: {dataframe_num_cols}            
            #### Missing values:
            - Number of missing values: {dataframe_num_missing_values}
            - % of missing values: {dataframe_percentage_missing_values:.2f} %
            #### Duplicates:
            - Number of duplicates: {dataframe_num_duplicates}
            - % of duplicate rows: {dataframe_percentage_duplicates:.2f} % 
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
    selected_variable = st.segmented_control(label="Select a variable to preview",
                                             options=columns,
                                             key="Variable_previsualization_selector")

    ### Descripción de la variable:
    # Tipo de dato:
    if selected_variable is not None:

        series_to_analyze = dataframe[selected_variable]

        st.subheader(selected_variable)

        if series_to_analyze.dtype == "object":
            ### Check if the object might be an ID or similar
            # if series_to_analyze.nunique() / len(series_to_analyze) > 0.9:
            #     st.write("Probably and ID")
            #
            # else:
            #     st.write("TBD")

            data_info_tab, object_graphs_tab = st.tabs(["Data info", "Graphs"])

            with data_info_tab:
                col1, col2, col3 = st.columns(3)

                with col3:
                    top_n = st.slider(label="Top N", min_value=1, value=5)
                    rare_freq = st.slider(label="Rare freq", min_value=1, value=10)


                with col1:
                    st.subheader("General info")
                    st.write(f"Data type: {series_to_analyze.dtype}")
                    st.write(f"Number of unique values: {series_to_analyze.nunique(dropna=True)}")
                    st.write(f"Missing values: {pd.isna(series_to_analyze).sum()}")
                    st.write(f"Missing values %: {pd.isna(series_to_analyze).sum() / dataframe.shape[0] * 100:.2f}")
                    st.write(f"Memory usage (kB):  {series_to_analyze.memory_usage() / 1024:.2f} kb")

                with col2:
                    #Precalc_vars:
                    string_lengths = series_to_analyze.dropna().astype(str).str.len()
                    top_values = series_to_analyze.value_counts(dropna=False).head(top_n)
                    top_prop = top_values.iloc[0] / len(series_to_analyze)
                    top_category_name = top_values.index[0]

                    value_counts = series_to_analyze.value_counts()
                    rare_mask = value_counts < rare_freq
                    rare_values = rare_mask.sum()
                    rare_categories = value_counts[rare_mask].index.tolist()

                    ### Display info:
                    st.subheader("Statistical info")
                    st.write(f"Min. length: {string_lengths.min()}")
                    st.write(f"Max. length: {string_lengths.max()}")
                    st.write(f"Average length: {string_lengths.mean():.2f}")
                    st.write(f"Top category: {top_category_name}")
                    st.write(f"Top category occurrences: {top_values.iloc[0]}")
                    st.write(f"Top category proportion: {top_prop:.2f}")
                    st.write(f"Rare categories (<{rare_freq} appearances): {rare_categories}")

            with object_graphs_tab:
                fig, ax = plt.subplots()
                sns.barplot(x=top_values.values, y=top_values.index, palette="viridis", ax=ax)
                ax.set_xlabel("Count")
                ax.set_ylabel("Category")
                ax.set_title(f"Top {top_n} categories for '{series_to_analyze.name}'")
                st.pyplot(fig)

        elif series_to_analyze.dtype == "datetime":
            pass

        else:

            data_info_tab, histogram_tab = st.tabs(["Data info", "Histogram"])

            with data_info_tab:
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("General info")
                    st.write(f"Data type: {series_to_analyze.dtype}")
                    st.write(f"Missing values: {pd.isna(series_to_analyze).sum()}")
                    st.write(f"Missing values %: {pd.isna(series_to_analyze).sum() / dataframe.shape[0] * 100:.2f}")
                    st.write(f"Memory usage (kB):  {series_to_analyze.memory_usage() / 1024:.2f} kb")

                with col2:
                    st.subheader("Statistical info")
                    st.write(f"Mean: {series_to_analyze.mean():.2f}")
                    st.write(f"Median: {series_to_analyze.median()}")
                    st.write(f"Standard deviation: {series_to_analyze.std():.2f}")
                    st.write(f"Max: {series_to_analyze.max()}")
                    st.write(f"Min: {series_to_analyze.min()}")

            with histogram_tab:

                fig, ax = plt.subplots()
                ax.hist(series_to_analyze, bins = 20)
                ax.set_title(str(selected_variable))
                st.pyplot(fig)

    st.divider()

    st.subheader("🎯📌 Target and feature selection")

    target_variable = st.segmented_control("Select the target variable",
                                           options=columns,
                                           key="Target_variable_selector",
                                           selection_mode="single")

    if target_variable is not None:

        y_data = dataframe[target_variable]

        filtered_options = list(columns).copy()
        filtered_options.remove(target_variable)
        explored_variables = st.segmented_control("Select the variables to explore",
                                                  options = filtered_options,
                                                  selection_mode="multi")

        if explored_variables:
            X_data = dataframe[explored_variables]
            #st.write(X_data.head())

            ### correlations
            corr_matrix = X_data.corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
            st.pyplot(fig)


    # st.write(dataframe.dtypes)