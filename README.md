# 📱 PhonePe Pulse Data Visualization and Exploration

This project is an interactive data visualization dashboard for **PhonePe Pulse** metrics, built using **Streamlit** and **Plotly**. The goal is to provide insightful and visually appealing representations of transaction and user data across different states in India over time, using real data from the PhonePe Pulse GitHub repository.

## 📄 Project Overview

PhonePe Pulse is a public repository containing extensive data on digital transactions across India. This project extracts, transforms, and loads this data into a MySQL database and then visualizes it in a user-friendly dashboard. The dashboard includes maps, graphs, and widgets that allow users to explore various aspects of transaction data, including the number of registered users, transaction amounts, and counts per state and quarter.

## 🛠 Features

- **User-Friendly Dashboard**: Built with Streamlit for an interactive, responsive experience.
- **Geo Visualization**: Visualize transaction data on a map of India, with details per state.
- **Quarterly and Yearly Trends**: Track trends across quarters and years using line graphs.
- **Transaction & User Analytics**: View top states for users, transactions, and amounts with metrics and bar charts.
- **Interactive Widgets**: Filter data by year, quarter, state, and transaction type.
- **Secure and Efficient Data Storage**: MySQL backend for efficient data handling and querying.

## 📈 Dashboard Sections

1. **Overview Widgets**: Displays top states by user count, transaction count, and transaction amount.
2. **Statewise Geo Visualization**: Interactive choropleth map of India, showing transaction data per state.
3. **Transaction Count and Amount Analysis**: Charts to show transaction types by count and amount.
4. **Quarterly Trends**: Line charts displaying transaction and user data across quarters and years.

## 🛠️ Tech Stack

- **Python**: Data processing and dashboard development.
- **Streamlit**: Interactive dashboard and UI.
- **Plotly**: Data visualization (maps, bar charts, line graphs, and pie charts).
- **MySQL**: Database for storing processed data.
- **Pandas**: Data transformation and manipulation.
- **Regular Expressions**: Standardizing state names.
- **Git**: Repository management and data extraction from GitHub.

## 🗄️ Database Schema

The database consists of the following main tables:

- `map_user`: Contains data on the number of registered users per state, year, and quarter.
- `map_transaction`: Holds data on transaction amounts and counts per state, year, and quarter.
- `aggregated_transaction`: Contains data grouped by transaction type, year, and quarter.

## 🔧 Installation & Setup

### Prerequisites

- **Python 3.7+**
- **MySQL Server**
- **Git**
- Required Python packages listed in `requirements.txt`

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/PhonePe_Pulse_Data_Viz.git
    cd PhonePe_Pulse_Data_Viz
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up MySQL Database**:
    - Create a new MySQL database.
    - Load the data from the PhonePe Pulse repository into the MySQL tables (`map_user`, `map_transaction`, and `aggregated_transaction`).

4. **Run the Streamlit App**:
    ```bash
    streamlit run app.py
    ```

5. **Access the Dashboard**: Open `http://localhost:8501` in your browser.

## 📊 Dashboard Usage

- **Main Menu**:
    - **Dashboard**: Access the visualizations and analysis.
    - **About**: Information about the project.

- **Widgets**:
    - **Select Year, Quarter, State, and Type (Transactions/Users)**: Filter data for in-depth analysis.

## 🌐 Live Demo

A live version of this dashboard can be hosted on platforms like Streamlit Sharing, Heroku, or any cloud platform that supports Python web applications.

## 🚀 Future Enhancements

- **Real-Time Data Updates**: Automatically pull data from PhonePe’s repository to keep the dashboard updated.
- **Advanced Filters**: Add more filters for transaction types and regions.
- **User Segmentation**: Analyze user demographics and behavior based on transaction data.
- **Mobile Optimization**: Improve the UI for mobile devices.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request, open an issue, or suggest any improvements.

## 📄 License

This project is licensed under the MIT License.

## 👏 Acknowledgments

- **PhonePe Pulse** for making the data publicly available.
- **Streamlit** and **Plotly** for providing excellent tools for data visualization.
