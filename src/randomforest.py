from sklearn.model_selection import RandomizedSearchCV

# Add random forest prediction for next season
if x_axis_val == 'YEAR' and y_axis_val != 'YEAR':
    X_train = df_selected_teams[df_selected_teams.YEAR < 2022][[x_axis_val]]
    y_train = df_selected_teams[df_selected_teams.YEAR < 2022][y_axis_val]
    X_test = np.array([2022]).reshape(-1, 1)

    # Hyperparameter tuning for random forest model
    param_distributions = {
        'n_estimators': [10, 50, 100],
        'max_depth': [3, 5, 10],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    rf = RandomForestRegressor(random_state=42)
    randomized = RandomizedSearchCV(rf, param_distributions, cv=5, scoring='r2', n_iter=20, random_state=42)
    randomized.fit(X_train, y_train)
    rf_best = randomized.best_estimator_

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
    y_pred_train = rf_best.predict(X_train)
    mse_train = mean_squared_error(y_train, y_pred_train)
    r2_train = r2_score(y_train, y_pred_train)

    st.write(f"Training set mean squared error: {mse_train:.2f}")
    st.write(f"Training set R-squared: {r2_train:.2f}")

    # Display scatter plot
    st.plotly_chart(plot, use_container_width=True)
