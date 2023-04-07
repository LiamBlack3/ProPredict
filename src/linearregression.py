# code for linear regression only

# # Add linear regression prediction for next season
#     if x_axis_val == 'YEAR' and y_axis_val != 'YEAR':
#         X = df_selected_teams[df_selected_teams.YEAR < 2022][[x_axis_val]]
#         y = df_selected_teams[df_selected_teams.YEAR < 2022][[y_axis_val]]
        
#         # Hyperparameter tuning for linear regression model
#         param_grid = {'fit_intercept': [True, False], 'normalize': [True, False]}
#         lr = LinearRegression()
#         grid = GridSearchCV(lr, param_grid, cv=5, scoring='r2')
#         grid.fit(X, y)
#         lr_best = grid.best_estimator_
        
#         next_season = 2022
#         next_year = np.array([next_season]).reshape(-1, 1)
#         next_stat = lr_best.predict(next_year)
#         st.write(f"Predicted {y_axis_val} for {next_season}: {next_stat[0][0]:.2f}")
#         plot.add_trace(
#             go.Scatter(
#                 x=[next_season],
#                 y=next_stat[0],
#                 mode='markers',
#                 name='Next season prediction',
#                 marker=dict(
#                     color='red',
#                     size=10,
#                     symbol='circle'
#                 )
#             )
#         )
        
# 		# Evaluation metrics
#         y_pred = lr_best.predict(X)
#         mse = mean_squared_error(y, y_pred)
#         r2 = r2_score(y, y_pred)
#         st.write(f"Mean squared error: {mse:.2f}")
#         st.write(f"R-squared: {r2:.2f}")

#     # Display scatter plot
#     st.plotly_chart(plot, use_container_width=True)