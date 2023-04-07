#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from PIL import Image
from scipy import stats

st.set_page_config(layout="wide")

# Functions for each of the pages
def home(): #uploaded_file
    # if uploaded_file:
    #     st.header('Begin exploring the data using the menu on the left')
    # else:
    #     st.header('To begin please upload a file')
    # Set page header
    st.title("Welcome to My Streamlit App!")


# Add instructions
    st.write("Before you get started, look at these steps:")
    st.write("1. Upload your data file(s) on the left!")
    st.write("2. If you want to see your dataset select Data Summary")
    st.write("3. If you are ready to research select Interactive Plots!")
    st.write("4. Want to test out the predictive model? Select Predictive modeling!")

# Add image
    st.image("../img/homepage.png", caption="What will you explore...?", use_column_width=True)
    

def data_summary(df1,df2):
    st.header('Statistics of Dataframe')
    st.write(df1)
    st.write(df2)
    # st.write(df.describe())


def team_data(df1):
    # Create two columns
    col1, col2 = st.columns(2)

    # Select one or more teams from dropdown list
    sorted_unique_team = sorted(df1.TEAM.unique())
    team_option = ['All Teams'] + sorted_unique_team
    selected_teams = st.multiselect('Team', team_option, default='All Teams')

    try:
        # Select appropriate data based on selected team(s)
        if not selected_teams:
            raise ValueError('Please select at least one team.')
        elif 'All Teams' in selected_teams:
            df_selected_teams = df1.copy()
        else:
            df_selected_teams = df1[df1.TEAM.isin(selected_teams)].copy()
    except ValueError as e:
        st.warning(str(e))
        return

    # Select X and Y axes for scatter plot
    exclude_cols = ['TEAM']

    x_axis_options = [col for col in df_selected_teams.columns if col not in exclude_cols]
    x_axis_val = col1.selectbox('Select the X-axis', options=x_axis_options)
    y_axis_options = [col for col in df_selected_teams.columns if col not in exclude_cols]
    y_axis_val = col2.selectbox('Select the Y-axis', options=y_axis_options)

        # Create scatter plot with linear regression trendline
    plot = px.scatter(df_selected_teams, x=x_axis_val, y=y_axis_val, color=df_selected_teams.TEAM, trendline='ols',
                      trendline_color_override='green', hover_name="TEAM", hover_data=["YEAR", "W"])
    
    # Compute and display R-squared value
    X = df_selected_teams[x_axis_val]
    y = df_selected_teams[y_axis_val]
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
    r_squared = r_value ** 2
    st.write(f"Scatter plot R-squared value: {r_squared:.2f}")

        
            # Display scatter plot
    st.plotly_chart(plot, use_container_width=True)


def player_data(df2):
    # Create three columns
    col3, col4, col5 = st.columns(3)
    
    # Select one or more teams from dropdown list
    sorted_unique_team = sorted(df2.TEAM.unique())
    teams_option = ['All Teams'] + sorted_unique_team
    selected_teams = col5.multiselect('Team', teams_option, default='All Teams')

    try:
        # Select appropriate data based on selected team(s)
        if not selected_teams:
            raise ValueError('Please select at least one team.')
        elif 'All Teams' in selected_teams:
            df_selected_teams = df2.copy()
        else:
            df_selected_teams = df2[df2.TEAM.isin(selected_teams)].copy()
    except ValueError as e:
        st.warning(str(e))
        return

    players = df_selected_teams['Player'].unique()
    selected_player = col5.selectbox("Select player", players)
    filtered_data_players = df_selected_teams[df_selected_teams['Player'] == selected_player]

    # Select X and Y axes for scatter plot
    # exlude unnecessary collumns (ones that contain stringified dates)
    exclude_cols = ['TEAM', 'Player']
    x_axis_options = [col for col in filtered_data_players.columns if col not in exclude_cols]
    y_axis_options = [col for col in filtered_data_players.columns if col not in exclude_cols]

    x_axis_val = col3.selectbox('Select the X-axis', options=x_axis_options, key="3")
    y_axis_val = col4.selectbox('Select the Y-axis', options=y_axis_options, key="4")

    

    plot = px.scatter(filtered_data_players, x=x_axis_val, y=y_axis_val, color='TEAM', trendline='ols',
                      trendline_color_override='green', hover_name="Player", hover_data=["TEAM", "YEAR"])
    
    # Compute and display R-squared value
    X = filtered_data_players[x_axis_val]
    y = filtered_data_players[y_axis_val]
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
    r_squared = r_value ** 2
    st.write(f"Scatter plot R-squared value: {r_squared:.2f}")

    
    # Display scatter plot
    st.plotly_chart(plot, use_container_width=True)


def predictive_team_data(df1):
    
    # Create two columns
    col1, col2 = st.columns(2)

    # Select one or more teams from dropdown list
    sorted_unique_team = sorted(df1.TEAM.unique())
    team_option = ['All Teams'] + sorted_unique_team
    selected_teams = st.multiselect('Team', team_option, default='All Teams')

    try:
        # Select appropriate data based on selected team(s)
        if not selected_teams:
            raise ValueError('Please select at least one team.')
        elif 'All Teams' in selected_teams:
            df_selected_teams = df1.copy()
        else:
            df_selected_teams = df1[df1.TEAM.isin(selected_teams)].copy()
    except ValueError as e:
        st.warning(str(e))
        return

    # Select Y axis for scatter plot
    exclude_cols = ['YEAR', 'TEAM']
    y_axis_options = [col for col in df_selected_teams.columns if col not in exclude_cols]
    y_axis_val = col1.selectbox('Select the Y-axis', options=y_axis_options)

    # Create scatter plot with linear regression trendline
    plot = px.scatter(df_selected_teams, x='YEAR', y=y_axis_val, color=df_selected_teams.TEAM, trendline='ols',
                    trendline_color_override='green', hover_name="TEAM", hover_data=["YEAR", "W"])

    # Compute and display R-squared value
    y = df_selected_teams[y_axis_val]
    slope, intercept, r_value, p_value, std_err = stats.linregress(df_selected_teams.YEAR, y)
    r_squared = r_value ** 2
    st.write(f"Scatter plot R-squared value: {r_squared:.2f}")

    # Add prediction for next season
    if y_axis_val != 'YEAR':
        X_train = df_selected_teams[df_selected_teams.YEAR < 2022][['YEAR']]
        y_train = df_selected_teams[df_selected_teams.YEAR < 2022][y_axis_val]
        X_test = np.array([2022]).reshape(-1, 1)


        # Hyperparameter tuning for linear regression model
        lr_param_grid = {'fit_intercept': [True, False]}
        lr = LinearRegression()
        lr_grid = GridSearchCV(lr, lr_param_grid, cv=5, scoring='r2')
        lr_grid.fit(X_train, y_train)
        lr_best = lr_grid.best_estimator_

        # Evaluate linear regression model
        y_pred_lr = lr_best.predict(X_train)
        r2_lr = r2_score(y_train, y_pred_lr)

        if round(r2_lr,1) >= 0.5:  # Use linear regression model if R-squared value is significant
            next_stat = lr_best.predict(X_test)
            st.write(f"Predicted {y_axis_val} for 2022: {next_stat[0]:.2f}")
            plot.add_trace(
                go.Scatter(
                    x=[2022],
                    y=[next_stat[0]],
                    mode='markers',
                    name='Next season prediction',
                    marker=dict(
                        color='red',
                        size=10,
                        symbol='circle'
                    )
                )
            )
            # Evaluation metrics
            mse_lr = mean_squared_error(y_train, y_pred_lr)
            st.write(f"Linear Regression Model Training set mean squared error: {mse_lr:.2f}")
            st.write(f"Linear Regression Model Training set R-squared: {r2_lr:.2f}")
        else:  # Use random forest model if R-squared value is not significant
            rf_param_grid = {
                'n_estimators': [10, 50, 100],
                'max_depth': [3, 5, 10],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            rf = RandomForestRegressor(random_state=42)
            n_splits = min(5, len(X_train))  # set maximum number of splits to the number of samples in X_train
            rf_grid = GridSearchCV(rf, rf_param_grid, cv=n_splits, scoring='r2')
            rf_grid.fit(X_train, y_train)
            rf_best = rf_grid.best_estimator_


            # Predict next season's statistics
            next_stat = rf_best.predict(X_test)
            st.write(f"Predicted {y_axis_val} for 2022: {next_stat[0]:.2f}")
            plot.add_trace(
                go.Scatter(
                    x=[2022],
                    y=[next_stat[0]],
                    mode='markers',
                    name='Next season prediction',
                    marker=dict(
                        color='red',
                        size=10,
                        symbol='circle'
                    )
                )
            )

            # Evaluation metrics
            y_pred_train_rf = rf_best.predict(X_train)
            mse_train_rf = mean_squared_error(y_train, y_pred_train_rf)
            r2_train_rf = r2_score(y_train, y_pred_train_rf)
            st.write(f"Random Forest Model Training set mean squared error: {mse_train_rf:.2f}")
            st.write(f"Random Forest Model Training set R-squared: {r2_train_rf:.2f}")

        


            # Display scatter plot
        st.plotly_chart(plot, use_container_width=True)






def predictive_player_data(df2):
    # Create three columns
    col3, col4, col5 = st.columns(3)
    
    # Select one or more teams from dropdown list
    sorted_unique_team = sorted(df2.TEAM.unique())
    teams_option = ['All Teams'] + sorted_unique_team
    selected_teams = col5.multiselect('Team', teams_option, default='All Teams')
    try:
        # Select appropriate data based on selected team(s)
        if not selected_teams:
            raise ValueError('Please select at least one team.')
        elif 'All Teams' in selected_teams:
            df_selected_teams = df2.copy()
        else:
            df_selected_teams = df2[df2.TEAM.isin(selected_teams)].copy()
    except ValueError as e:
        st.warning(str(e))
        return
    players = df_selected_teams['Player'].unique()
    selected_player = col5.selectbox("Select player", players)
    filtered_data_players = df_selected_teams[df_selected_teams['Player'] == selected_player]
    # Select X and Y axes for scatter plot
    # exlude unnecessary collumns (ones that contain stringified dates)
    exclude_cols = ['TEAM', 'Player']
    x_axis_options = [col for col in filtered_data_players.columns if col not in exclude_cols]
    y_axis_options = [col for col in filtered_data_players.columns if col not in exclude_cols]
    x_axis_val = col3.selectbox('Select the X-axis', options=x_axis_options, key="3")
    y_axis_val = col4.selectbox('Select the Y-axis', options=y_axis_options, key="4")
    
    plot = px.scatter(filtered_data_players, x=x_axis_val, y=y_axis_val, color='TEAM', trendline='ols',
                      trendline_color_override='green', hover_name="Player", hover_data=["TEAM", "YEAR"])
    
    # Compute and display R-squared value
    X = filtered_data_players[x_axis_val]
    y = filtered_data_players[y_axis_val]
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
    r_squared = r_value ** 2
    st.write(f"Scatter plot R-squared value: {r_squared:.2f}")
    # Add prediction for next season
    if x_axis_val == 'YEAR' and y_axis_val != 'YEAR':
        X_train = filtered_data_players[filtered_data_players.YEAR < 2022][[x_axis_val]]
        y_train = filtered_data_players[filtered_data_players.YEAR < 2022][y_axis_val]
        X_test = np.array([2022]).reshape(-1, 1)
        # Hyperparameter tuning for linear regression model
        lr_param_grid = {'fit_intercept': [True, False]}
        lr = LinearRegression()
        n_splits = min(5, len(X_train))  # set maximum number of splits to the number of samples in X_train
        lr_grid = GridSearchCV(lr, lr_param_grid, cv=n_splits, scoring='r2')
        lr_grid.fit(X_train, y_train)
        lr_best = lr_grid.best_estimator_
        # Evaluate linear regression model
        y_pred_lr = lr_best.predict(X_train)
        r2_lr = r2_score(y_train, y_pred_lr)
        
        next_stat = lr_best.predict(X_test)
        st.write(f"Predicted {y_axis_val} for 2022: {next_stat[0]:.2f}")
        plot.add_trace(
            go.Scatter(
                x=[2022],
                y=[next_stat[0]],
                mode='markers',
                name='Next season prediction',
                marker=dict(
                    color='red',
                    size=10,
                    symbol='circle'
                )
            )
        )
            # Evaluation metrics
        mse_lr = mean_squared_error(y_train, y_pred_lr)
        st.write(f"Linear Regression Model Training set mean squared error: {mse_lr:.2f}")
        st.write(f"Linear Regression Model Training set R-squared: {r2_lr:.2f}")
        
            # Display scatter plot
        st.plotly_chart(plot, use_container_width=True)


    
    



# Add a title and intro text
st.title('NBA Data Explorer')
st.text('This is a web app to allow exploration of NBA Data')

# Sidebar setup
st.sidebar.title('Sidebar')
upload_file1 = st.sidebar.file_uploader('Upload a file containing NBA data', key="1")
upload_file2 = st.sidebar.file_uploader('Upload a file containing NBA data', key ="2")
#Sidebar navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select what you want to display:', ['Home', 'Data Summary', 'Interactive Plots', 'Predictive Modeling'])

# Check if file has been uploaded
try:
    if upload_file1 is not None:
        df1 = pd.read_csv(upload_file1)
    if upload_file2 is not None:
        df2 = pd.read_csv(upload_file2)
except:
    print("No file was uploaded.")
    
# Navigation options
if options == 'Home':
    home()
elif options == 'Data Summary':
    data_summary(df1,df2)
elif options == 'Predictive Modeling':
    predictive_team_data(df1)
    predictive_player_data(df2)
elif options == 'Interactive Plots':
    team_data(df1)
    player_data(df2)