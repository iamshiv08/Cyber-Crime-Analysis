import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Sidebar for user input
with st.sidebar:
    st.title("Cyber Crime Analysis")
    st.subheader("Analysis by Year and Fraud Categories")

    # Button to preview the data
    preview = st.button("Data Preview")

    # Dropdown to select a year for analysis
    years = ["2018", "2019", "2020", "2021", "2022", "Overall"]
    selected_year = st.selectbox(
        "Select a Year for Analysis", options=years, index=None
    )

# Main content of the dashboard
st.title("Cyber Crime Dashboard")
st.text("(data from data.gov.in)")

# Load the dataset
df = pd.read_csv("cyber.csv")

# Clean column names by removing spaces and special characters
df.columns = df.columns.str.strip().str.replace(" - ", "_").str.replace(" ", "_")

# Fill missing values with 0
df.fillna(0, inplace=True)

if selected_year is None:
    st.write("### Year not selected. Please select a year from the sidebar.")

if preview:
    st.subheader("Dataset Preview")
    st.dataframe(df.head(10))

# fraud categories to their names
fraud_categories = {
    "A": "Credit/Debit Card Frauds",
    "B": "ATM Frauds",
    "C": "Online Banking Frauds",
    "D": "OTP Frauds",
    "E": "Other Frauds",
}

if selected_year:

    # Overall
    if selected_year == "Overall":
        # Sum total cybercrime cases for each year
        columns_to_plot = [
            "2018_Total",
            "2019_Total",
            "2020_Total",
            "2021_Total",
            "2022_Total",
        ]
        total_crimes = df[columns_to_plot].sum()
        # 2018_Total = 10059.0
        # 2019_Total = 18687.0
        # 2020_Total = 31185.0
        # 2021_Total = 42021.0
        # 2022_Total = 52410.0

        # Plot total cybercrime cases per year
        st.subheader("Total Cybercrime Cases Per Year")
        plt.figure(figsize=(10, 6))
        plt.bar(
            ["2018", "2019", "2020", "2021", "2022"],
            total_crimes,
            color="skyblue",
            alpha=0.8,
        )
        plt.title("Total Cybercrime Cases Per Year", fontsize=16)
        plt.ylabel("Number of Cases", fontsize=14)
        
        plt.xlabel("Year", fontsize=14)
        
        st.pyplot(plt)

        # Display analysis description
        st.write(
            """
            **Analysis of Total Cybercrime Cases Per Year:**
This chart shows a sharp rise in cybercrime cases from 2018 to 2022. The number of cases has increased significantly, especially after 2019, indicating a growing trend in cyber-related crimes.        """
        )

        # Plot year-wise cybercrime trends for all states
        st.subheader("Year-wise Cybercrime Trends for All States")
        plt.figure(figsize=(16, 10))
        states = df["State/UT"].unique() # Gives all states name unique because it take only one time name
        years = ["2018", "2019", "2020", "2021", "2022"]
        for state in states:
            state_data = df[df["State/UT"] == state] #Filters the dataset to only include rows where State/UT matches the current state
            values = state_data[columns_to_plot].values.flatten() # values converts the selected columns into a NumPy array and flatten convert in 1D array
            if not values.any():  # Skip states with no data
                continue
            plt.plot(years, values, marker="o", label=state)
        plt.title("Year-wise Cybercrime Trends for All States", fontsize=18)
        plt.xlabel("Year", fontsize=14)
        plt.ylabel("Number of Cases", fontsize=14)
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1), title="States", ncol=2)
        
        st.pyplot(plt)

        # Display analysis description
        st.write(
            """
            **Analysis of Year-wise Cybercrime Trends for All States:**
The graph shows a sharp rise in cybercrime cases across states from 2018 to 2022, with Telangana and Maharashtra leading. While most states show an upward trend, a few remain stable. The overall surge highlights growing digital threats and reporting.        """
        )

        # Pie Chart for Fraud Categories
        st.subheader("Distribution of Cybercrime Cases by Fraud Categories")
        category_columns = [
            f"{year}_{i}"
            for i in fraud_categories.keys()
            for year in ["2018", "2019", "2020", "2021", "2022"]
        ]  # ['2018_A', '2019_A', '2020_A', '2021_A', '2022_A', '2018_B', '2019_B', '2020_B', '2021_B', '2022_B', '2018_C', '2019_C', '2020_C', '2021_C', '2022_C', '2018_D', '2019_D', '2020_D', '2021_D', '2022_D', '2018_E', '2019_E', '2020_E', '2021_E', '2022_E']
        total_category_cases = df[category_columns].sum()
        # 2018_A 927.0, 2019_A 1101.0, 2020_A 3582.0, 2021_A 4872.0, 2022_A 4995.0, 2018_B 3852.0, 2019_B 6201.0, 2020_B 6480.0, 2021_B 5697.0, 2022_B 5070.0, 2018_C 2904.0, 2019_C 6279.0, 2020_C 12141.0, 2021_C 14469.0, 2022_C 19473.0, 2018_D 957.0, 2019_D 1647.0, 2020_D 3279.0, 2021_D 6084.0, 2022_D 8730.0, 2018_E 1419.0, 2019_E 3459.0, 2020_E 5703.0, 2021_E 10899.0, 2022_E 14142.0
        fraud_summary = {
            cat_name: total_category_cases.filter(like=cat).sum()
            for cat, cat_name in fraud_categories.items()
        } # {'Credit/Debit Card Frauds': np.float64(15477.0), 'ATM Frauds': np.float64(27300.0), 'Online Banking Frauds': np.float64(55266.0), 'OTP Frauds': np.float64(20697.0), 'Other Frauds': np.float64(35622.0)}
        # Plot Pie Chart
        plt.figure(figsize=(8, 8))
        plt.pie(
            fraud_summary.values(),
            labels=fraud_summary.keys(),
            autopct="%1.1f%%",
            startangle=140,
            colors=["skyblue", "lightgreen", "lightcoral", "gold", "violet"],
        )
        plt.title(
            "Overall Distribution of Cybercrime Cases by Fraud Categories", fontsize=16
        )
        st.pyplot(plt)

        # Display analysis description
        st.write(
            """
            **Analysis of Distribution of Cybercrime Cases by Fraud Categories:**
The pie chart shows that online banking frauds account for the largest share (35.8%) of cybercrimes, followed by Other Frauds (23.1%) and ATM frauds (17.7%). OTP and credit/debit card frauds make up the remaining portion.        """
        )

    elif selected_year == "2018":
        selected_year_data = df[
            [f"2018_{cat}" for cat in fraud_categories.keys()]
        ].sum() # 2018_A 927.0 2018_B 3852.0 2018_C 2904.0 2018_D 957.0 2018_E 1419.0
        
        # Plot total fraud cases for each category in the selected year
        st.subheader(f"Total Fraud Cases for Each Category in 2018")
        plt.figure(figsize=(10, 6))
        plt.bar(
            [fraud_categories[cat] for cat in fraud_categories.keys()],
            selected_year_data,
            color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
        )
        plt.title(f"Total Fraud Cases in 2018", fontsize=16)
        plt.ylabel("Number of Cases", fontsize=14)
        plt.xlabel("Fraud Categories", fontsize=14)
        
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of Total Fraud Cases in 2018:**
            The graph shows that ATM Frauds had the highest cases in 2018, followed by Online Banking Frauds. Credit/Debit Card Frauds and OTP Frauds had significantly lower occurrences, while Other Frauds were moderate.
        """
        )

        # State-wise Fraud Cases (Bar Graph)
        st.subheader(f"State-wise Cybercrime Cases in 2018")
        state_data = df[["State/UT", f"2018_Total"]] # Gives 2018 total
        state_data = state_data.sort_values(by=f"2018_Total", ascending=False) # Decending order
        # Plot Bar Graph for State-wise Cases
        plt.figure(figsize=(12, 8))
        plt.barh(
            state_data["State/UT"],
            state_data[f"2018_Total"],
            color="skyblue",
            alpha=0.8,
        )
        plt.title(f"State-wise Cybercrime Cases in 2018", fontsize=16)
        plt.xlabel("Number of Cases", fontsize=14)
        plt.ylabel("State/UT", fontsize=14)
        plt.gca().invert_yaxis()  # Invert y-axis to show highest cases on top
       
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of State-wise Cybercrime Cases in 2018:**
            Maharashtra and Uttar Pradesh reported the highest cybercrime cases in 2018. Other states like Odisha, Bihar, and Telangana also had significant cases, while several smaller states had minimal incidents.
        """
        )

        # Detailed analysis per category
        state_data = df[
            ["State/UT"] + [f"2018_{cat}" for cat in fraud_categories.keys()]
        ] # Gives state name and their total case in catogary(Debit Card,Online Banking...)
        st.subheader(f"Detailed Analysis by Category in 2018")
        for cat, cat_name in fraud_categories.items():
            st.write(f"### {cat_name}")
            top_states = (
                state_data[["State/UT", f"2018_{cat}"]]
                .sort_values(by=f"2018_{cat}", ascending=False)
                .iloc[2:7]  # Skip the first two rows (totals)
            )
            top_states.rename(
                columns={f"2018_{cat}": f"{cat_name} Cases"}, inplace=True
            ) # rename column name
            st.write(f"Top 5 States with Highest {cat_name} Cases:")
            st.table(top_states) # make table for this data
    elif selected_year == "2019":
        # If a specific year is selected, analyze data for that year
        selected_year_data = df[
            [f"2019_{cat}" for cat in fraud_categories.keys()]
        ].sum()

        # Plot total fraud cases for each category in the selected year
        st.subheader(f"Total Fraud Cases for Each Category in 2019")
        plt.figure(figsize=(10, 6))
        plt.bar(
            [fraud_categories[cat] for cat in fraud_categories.keys()],
            selected_year_data,
            color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
        )
        plt.title(f"Total Fraud Cases in 2019", fontsize=16)
        plt.ylabel("Number of Cases", fontsize=14)
        plt.xlabel("Fraud Categories", fontsize=14)
        
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of Total Fraud Cases in 2019:**
            In 2019, ATM and online banking fraud cases were the highest, each exceeding 6,000 cases. Other frauds also increased significantly compared to 2018, while OTP and credit/debit card frauds saw a moderate rise.
        """
        )

        # State-wise Fraud Cases (Bar Graph)
        st.subheader(f"State-wise Cybercrime Cases in 2019")
        state_data = df[["State/UT", f"2019_Total"]]
        state_data = state_data.sort_values(by=f"2019_Total", ascending=False)

        # Plot Bar Graph for State-wise Cases
        plt.figure(figsize=(12, 8))
        plt.barh(
            state_data["State/UT"],
            state_data[f"2019_Total"],
            color="skyblue",
            alpha=0.8,
        )
        plt.title(f"State-wise Cybercrime Cases in 2019", fontsize=16)
        plt.xlabel("Number of Cases", fontsize=14)
        plt.ylabel("State/UT", fontsize=14)
        plt.gca().invert_yaxis()  # Invert y-axis to show highest cases on top
       
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of State-wise Cybercrime Cases in 2019:**
            In 2019, Maharashtra reported the highest number of cybercrime cases, followed by Bihar, Odisha, and Uttar Pradesh. Overall, cybercrime incidents increased compared to 2018.
        """
        )

        # Detailed analysis per category
        state_data = df[
            ["State/UT"] + [f"2019_{cat}" for cat in fraud_categories.keys()]
        ]
        st.subheader(f"Detailed Analysis by Category in 2019")
        for cat, cat_name in fraud_categories.items():
            st.write(f"### {cat_name}")
            top_states = (
                state_data[["State/UT", f"2019_{cat}"]]
                .sort_values(by=f"2019_{cat}", ascending=False)
                .iloc[2:7]  # Skip the first two rows (totals)
            )
            top_states.rename(
                columns={f"2019_{cat}": f"{cat_name} Cases"}, inplace=True
            )
            st.write(f"Top 5 States with Highest {cat_name} Cases:")
            st.table(top_states)
    elif selected_year == "2020":
        # If a specific year is selected, analyze data for that year
        selected_year_data = df[
            [f"2020_{cat}" for cat in fraud_categories.keys()]
        ].sum()

        # Plot total fraud cases for each category in the selected year
        st.subheader(f"Total Fraud Cases for Each Category in 2020")
        plt.figure(figsize=(10, 6))
        plt.bar(
            [fraud_categories[cat] for cat in fraud_categories.keys()],
            selected_year_data,
            color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
        )
        plt.title(f"Total Fraud Cases in 2020", fontsize=16)
        plt.ylabel("Number of Cases", fontsize=14)
        plt.xlabel("Fraud Categories", fontsize=14)
        
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of Total Fraud Cases in 2020:**
            In 2020, online banking frauds saw a significant rise compared to 2019, exceeding 12,000 cases. Credit/Debit card frauds and OTP frauds also increased. This trend could be attributed to the growing reliance on digital transactions during the pandemic.
        """
        )

        # State-wise Fraud Cases (Bar Graph)
        st.subheader(f"State-wise Cybercrime Cases in 2020")
        state_data = df[["State/UT", f"2020_Total"]]
        state_data = state_data.sort_values(by=f"2020_Total", ascending=False)

        # Plot Bar Graph for State-wise Cases
        plt.figure(figsize=(12, 8))
        plt.barh(
            state_data["State/UT"],
            state_data[f"2020_Total"],
            color="skyblue",
            alpha=0.8,
        )
        plt.title(f"State-wise Cybercrime Cases in 2020", fontsize=16)
        plt.xlabel("Number of Cases", fontsize=14)
        plt.ylabel("State/UT", fontsize=14)
        plt.gca().invert_yaxis()  # Invert y-axis to show highest cases on top
       
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of State-wise Cybercrime Cases in 2020:**
            From 2019 to 2020, cybercrime cases saw a significant increase across India. In 2020, Telangana reported the highest number of cases, surpassing Maharashtra, which was leading in 2019. This rise in cybercrimes might be due to the rapid digitalization during the pandemic, which increased the attack surface for cybercriminals.
        """
        )

        # Detailed analysis per category
        state_data = df[
            ["State/UT"] + [f"2020_{cat}" for cat in fraud_categories.keys()]
        ]
        st.subheader(f"Detailed Analysis by Category in 2020")
        for cat, cat_name in fraud_categories.items():
            st.write(f"### {cat_name}")
            top_states = (
                state_data[["State/UT", f"2020_{cat}"]]
                .sort_values(by=f"2020_{cat}", ascending=False)
                .iloc[2:7]  # Skip the first two rows (totals)
            )
            top_states.rename(
                columns={f"2020_{cat}": f"{cat_name} Cases"}, inplace=True
            )
            st.write(f"Top 5 States with Highest {cat_name} Cases:")
            st.table(top_states)
    elif selected_year == "2021":
        # If a specific year is selected, analyze data for that year
        selected_year_data = df[
            [f"2021_{cat}" for cat in fraud_categories.keys()]
        ].sum()

        # Plot total fraud cases for each category in the selected year
        st.subheader(f"Total Fraud Cases for Each Category in 2021")
        plt.figure(figsize=(10, 6))
        plt.bar(
            [fraud_categories[cat] for cat in fraud_categories.keys()],
            selected_year_data,
            color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
        )
        plt.title(f"Total Fraud Cases in 2021", fontsize=16)
        plt.ylabel("Number of Cases", fontsize=14)
        plt.xlabel("Fraud Categories", fontsize=14)
        
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of Total Fraud Cases in 2021:**
            Comparing fraud cases between 2020 and 2021, there is a noticeable increase in all categories. Online banking frauds remain the highest, with a further rise in cases. OTP frauds and other frauds have also significantly increased, suggesting that cybercriminals are adapting and exploiting new vulnerabilities.
        """
        )

        # State-wise Fraud Cases (Bar Graph)
        st.subheader(f"State-wise Cybercrime Cases in 2021")
        state_data = df[["State/UT", f"2021_Total"]]
        state_data = state_data.sort_values(by=f"2021_Total", ascending=False)

        # Plot Bar Graph for State-wise Cases
        plt.figure(figsize=(12, 8))
        plt.barh(
            state_data["State/UT"],
            state_data[f"2021_Total"],
            color="skyblue",
            alpha=0.8,
        )
        plt.title(f"State-wise Cybercrime Cases in 2021", fontsize=16)
        plt.xlabel("Number of Cases", fontsize=14)
        plt.ylabel("State/UT", fontsize=14)
        plt.gca().invert_yaxis()  # Invert y-axis to show highest cases on top
       
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of State-wise Cybercrime Cases in 2021:**
            This graph shows state-wise cybercrime cases in 2021. Comparing this with the 2020 data, it appears that the number of cybercrime cases has increased across multiple states, with Telangana and Maharashtra continuing to report the highest numbers. This suggests a growing trend in cybercrimes, requiring stronger enforcement and cybersecurity measures.
        """
        )

        # Detailed analysis per category
        state_data = df[
            ["State/UT"] + [f"2021_{cat}" for cat in fraud_categories.keys()]
        ]
        st.subheader(f"Detailed Analysis by Category in 2021")
        for cat, cat_name in fraud_categories.items():
            st.write(f"### {cat_name}")
            top_states = (
                state_data[["State/UT", f"2021_{cat}"]]
                .sort_values(by=f"2021_{cat}", ascending=False)
                .iloc[2:7]  # Skip the first two rows (totals)
            )
            top_states.rename(
                columns={f"2021_{cat}": f"{cat_name} Cases"}, inplace=True
            )
            st.write(f"Top 5 States with Highest {cat_name} Cases:")
            st.table(top_states)
    elif selected_year == "2022":
        # If a specific year is selected, analyze data for that year
        selected_year_data = df[
            [f"2022_{cat}" for cat in fraud_categories.keys()]
        ].sum()

        # Plot total fraud cases for each category in the selected year
        st.subheader(f"Total Fraud Cases for Each Category in 2022")
        plt.figure(figsize=(10, 6))
        plt.bar(
            [fraud_categories[cat] for cat in fraud_categories.keys()],
            selected_year_data,
            color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
        )
        plt.title(f"Total Fraud Cases in 2022", fontsize=16)
        plt.ylabel("Number of Cases", fontsize=14)
        plt.xlabel("Fraud Categories", fontsize=14)
        
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of Total Fraud Cases in 2022:**
            This bar chart displays the total fraud cases in 2022 across different fraud categories. Compared to the 2021 data, it appears that online banking frauds and OTP frauds have significantly increased, highlighting a growing concern in digital financial security. Strengthening cybersecurity measures and increasing awareness could help mitigate these threats.
        """
        )

        # State-wise Fraud Cases (Bar Graph)
        st.subheader(f"State-wise Cybercrime Cases in 2022")
        state_data = df[["State/UT", f"2022_Total"]]
        state_data = state_data.sort_values(by=f"2022_Total", ascending=False)

        # Plot Bar Graph for State-wise Cases
        plt.figure(figsize=(12, 8))
        plt.barh(
            state_data["State/UT"],
            state_data[f"2022_Total"],
            color="skyblue",
            alpha=0.8,
        )
        plt.title(f"State-wise Cybercrime Cases in 2022", fontsize=16)
        plt.xlabel("Number of Cases", fontsize=14)
        plt.ylabel("State/UT", fontsize=14)
        plt.gca().invert_yaxis()  # Invert y-axis to show highest cases on top
       
        st.pyplot(plt)

        # Display analysis description
        st.write(
            f"""
            **Analysis of State-wise Cybercrime Cases in 2022:**
            This chart represents the state-wise cybercrime cases in India for 2022. Telangana continues to report a high number of cases, similar to 2021, followed by Maharashtra, Bihar, and Andhra Pradesh.
        """
        )

        # Detailed analysis per category
        state_data = df[
            ["State/UT"] + [f"2022_{cat}" for cat in fraud_categories.keys()]
        ]
        st.subheader(f"Detailed Analysis by Category in 2022")
        for cat, cat_name in fraud_categories.items():
            st.write(f"### {cat_name}")
            top_states = (
                state_data[["State/UT", f"2022_{cat}"]]
                .sort_values(by=f"2022_{cat}", ascending=False)
                .iloc[2:7]  # Skip the first two rows (totals)
            )
            top_states.rename(
                columns={f"2022_{cat}": f"{cat_name} Cases"}, inplace=True
            )
            st.write(f"Top 5 States with Highest {cat_name} Cases:")
            st.table(top_states)
