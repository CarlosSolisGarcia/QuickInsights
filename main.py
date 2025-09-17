import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from helpers import parse_uploaded_file

# Step 1: Loading the dataset
st.title("QuickInsights")
st.write("Welcome to the QuickInsights demo, with this app you'll be able to get a quick view of your data")
st.write("Stay tuned for more updates!")

uploaded_file = st.file_uploader(label="Upload the dataset you'd like to preview. Please use a Pandas friendly input file:",
                                 type=[".csv", ".xls", ".xlsx"]
                                 )

if uploaded_file is not None:

    dataframe, error = parse_uploaded_file(uploaded_file)
    # Displaying the dataframe:
    if error:
        st.error(error)
    else:
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
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", f"{dataframe_num_rows:,}")
        col2.metric("Columns", f"{dataframe_num_cols:,}")
        col3.metric("Duplicate rows", f"{dataframe_num_duplicates:,}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Total missing values", f"{dataframe_num_missing_values:,}")
        col5.metric("Missing values %", f"{dataframe_percentage_missing_values:.2f}%")
        col6.metric("Duplicate rows %", f"{dataframe_percentage_duplicates:.2f}%")

        st.markdown("#### Missing values per column")
        missing_per_column = dataframe.isna().sum()
        if missing_per_column.sum() > 0:
            st.bar_chart(missing_per_column)
        else:
            st.write("No missing values found in any column.")

        columns = dataframe.columns
        selected_variable = st.segmented_control(label="Select a variable to preview",
                                                 options=columns,
                                                 key="Variable_previsualization_selector")

        ### Var descriptions
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
                    col1, col2 = st.columns(2)

                    ### General info
                    with col1:
                        st.subheader("General info")
                        st.write(f"Data type: {series_to_analyze.dtype}")
                        st.write(f"Number of unique values: {series_to_analyze.nunique(dropna=True)}")
                        st.write(f"Missing values: {pd.isna(series_to_analyze).sum()}")
                        st.write(
                            f"Missing values %: {pd.isna(series_to_analyze).sum() / dataframe.shape[0] * 100:.2f}")
                        st.write(f"Memory usage (kB):  {series_to_analyze.memory_usage() / 1024:.2f} kb")

                    ### String length stats
                    with col2:
                        string_lengths = series_to_analyze.dropna().astype(str).str.len()
                        st.subheader("Text length info")

                        st.write(f"Min length: {string_lengths.min()}")
                        st.write(f"25th percentile: {string_lengths.quantile(0.25):.0f}")
                        st.write(f"Median length: {string_lengths.median():.0f}")
                        st.write(f"75th percentile: {string_lengths.quantile(0.75):.0f}")
                        st.write(f"Max length: {string_lengths.max()}")
                        st.write(f"Mean length: {string_lengths.mean():.0f}")
                        st.write(f"Std deviation: {string_lengths.std():.2f}")

                    ### Category details
                    st.subheader("Category details")

                    top_n = st.slider("Top N categories", min_value=1, max_value=20, value=5)
                    rare_freq = st.slider("Rare category threshold", min_value=1, max_value=50, value=10)
                    value_counts = series_to_analyze.value_counts(dropna=False)
                    top_col, rare_col = st.columns(2)
                    top_values = value_counts.head(top_n)
                    with top_col:
                        st.markdown("**Top categories**")
                        st.dataframe(top_values.rename("Count").to_frame())

                    rare_values = value_counts[value_counts < rare_freq]
                    with rare_col:
                        st.markdown(f"**Rare categories (<{rare_freq})**")
                        if rare_values.empty:
                            st.write("No rare categories found ✅")
                        else:
                            st.dataframe(rare_values.rename("Count").to_frame())

                with object_graphs_tab:
                    st.subheader(f"Top {top_n} categories for '{series_to_analyze.name}'")
                    top_values = series_to_analyze.value_counts().head(top_n)
                    st.bar_chart(top_values, horizontal=True)

                    # Rare categories
                    rare_values = series_to_analyze.value_counts()[series_to_analyze.value_counts() < rare_freq]
                    st.subheader(f"Rare categories (<{rare_freq} appearances)")

                    if rare_values.empty:
                        st.write("No rare categories found ✅")
                    else:
                        st.bar_chart(rare_values, horizontal=True)


            elif series_to_analyze.dtype == "datetime":
                pass

            else:

                data_info_tab, graph_tab = st.tabs(["Data info", "Graphs"])

                with data_info_tab:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("General info")
                        st.write(f"Data type: {series_to_analyze.dtype}")
                        st.write(f"Missing values: {pd.isna(series_to_analyze).sum()}")
                        st.write(f"Missing values %: {pd.isna(series_to_analyze).sum() / dataframe.shape[0] * 100:.2f}")
                        st.write(f"Number of unique values: {series_to_analyze.nunique(dropna=True)}")
                        st.write(f"Memory usage (kB):  {series_to_analyze.memory_usage() / 1024:.2f} kb")

                    with col2:
                        st.subheader("Statistical info")
                        mean_val = series_to_analyze.mean()
                        median_val = series_to_analyze.median()
                        std_val = series_to_analyze.std()
                        min_val = series_to_analyze.min()
                        q25 = series_to_analyze.quantile(0.25)
                        q75 = series_to_analyze.quantile(0.75)
                        max_val = series_to_analyze.max()
                        sum_val = series_to_analyze.sum()
                        skew_val = series_to_analyze.skew()
                        kurt_val = series_to_analyze.kurt()

                        subcol1, subcol2 = st.columns(2)

                        with subcol1:
                            st.markdown("**Basic stats**")
                            st.write(f"Mean: {series_to_analyze.mean():.2f}")
                            st.write(f"Median: {series_to_analyze.median()}")
                            st.write(f"Standard deviation: {series_to_analyze.std():.2f}")
                            st.write(f"Min: {series_to_analyze.min()}")
                            st.write(f"25th percentile: {q25:.2f}")
                            st.write(f"75th percentile: {q75:.2f}")
                            st.write(f"Max: {max_val:.2f}")

                        with subcol2:
                            st.markdown("**Advanced stats**")
                            st.write(f"Sum: {sum_val:.2f}")
                            st.write(f"Skewness: {skew_val:.2f}")
                            st.write(f"Kurtosis: {kurt_val:.2f}")

                with graph_tab:

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