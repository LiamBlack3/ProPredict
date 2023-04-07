# ProPredict

**Background**

ProPredict Tool is a web application that leverages the power of Streamlit to enable users to explore and analyze NBA player and team data. The tool employs regression analysis and interactive graphing to help users arrive at meaningful conclusions about the data. Users can interact with the tool to filter and sort data, plot different variables against each other, and perform linear regression to uncover relationships between different metrics. The pro stands for "proactive," highlighting the tool's ability to provide insights and predictions that can help YOU stay ahead of the curve in their sports analysis.

The interface is designed to be user-friendly and accessible to users of all levels of expertise. Whether you are a data scientist, a sports analyst, or a casual fan, the tool can help you gain insights into player and team performance, identify trends, and make data-driven decisions. Some of the features of the tool include a dashboard for easy navigation, customizable graphs and charts, and the ability to export data and visualizations.

Users can explore a wide range of metrics, including player and team statistics, individual player ratings, team rankings, and more. The tool makes it easy to compare different players and teams, identify outliers, and uncover patterns in the data. By using regression analysis and interactive graphing, users can gain a deeper understanding of the factors that contribute to success in the NBA.

Whether you are a sports analyst, a coach, or a fan, the tool can help you make informed decisions and gain valuable insights into the world of professional basketball.

# Installation(s)

To install and run the web app, please follow these steps:

1. Install streamlit using pip:

```text
pip install streamlit
```

2. Clone the repository and navigate to the project directory:

```text
git clone https://github.com/username/repo-name.git
cd repo-name
```

3. Install the required packages using pip:

```text
pip install package_name
```

4. Run the app!

```text
streamlit run <name_of_python_file>
```

# Project Structure

`data` folder:

 - Contains the sports csv data set you would like to conduct research upon
 
NBA offensive team stats is located here as an example csv file

`src` folder:

 - Contains all source code located in `main.py` for the implementation of streamlit tool

# Usage

After all dependencies are installed you can run the following command : `streamlit run main.py`

- This will start the Streamlit app and open it in your default browser.
- If you encounter any errors or warnings, check the console output for details.

1. On the home page of the Streamlit app, on the left hand side-bar you will see a button that allows you to upload a CSV file.

- Click the "Browse files" button to select a CSV file from your computer.

2. Click the "Interactive Plots" button on the lower-left to analyze the selected dataset and display the results in a scatter plot

- The scatter plot shows the relationship between the X and Y elements, with each data point represented as a circle.
- The line of best fit  shows the slope, intercept, and R-squared value of the linear regression line.

3. Investigate and explore the data points by interacting with the graphs and the table.

- Use the zoom and pan controls on the scatter plot to focus on specific areas of the graph.
- Hover over a data point on the scatter plot to see its X and Y values.
- Click on a data point to see more detailed information in the table.

4. Repeat steps 3-5 to analyze other CSV files or different combinations of X and Y elements.

- The app supports uploading different CSV files and selecting different X and Y elements for each file.



5. Close the Streamlit app by pressing Ctrl+C in your terminal or closing the browser window.


# Results section: pending

The line of best fit is calculated by minimizing the sum of squared errors between the predicted values and the actual values in the training data set. Once the line of best fit is determined, the model can use it to predict values for new data points by plugging in the input values and computing the corresponding output values based on the equation of the line.

Conclusion:

Summarizes the key challenges and results
Captures the attention of the reader
Convinces the reader to explore rest of senior thesis
References details and results whenever possible!
To get started, use the abstract as a “project roadmap”
