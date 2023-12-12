This Repository contains all code to obtain the results in my CSC2552 Final Project. The only part missing is the raw Reddit Pushshift data itself.

**Step 1 - Cleaning Data:**

In the "clean_subreddit_data" folder, first run "part1_get_2022_data.py", to strip out all interactions except the ones that were made in 2022 from a given Pushshift file. Then run "part2_remove_users.py" to remove all interactions from bot/spammer users in the files.

**Step 2 - Perparing General Files:**

run the following python scripts to generate files that will be accessed by the regression code.

Calc_Stress.py - uses the subway data to write the amount of stress for each day of 2022 into the file sterss.csv.

get_Toronto_users.py - Goes through the Pushshift files for Toronto subreddits and writes them into the file toronto_users

get_polarized_users.py - partitions the Toronto Users into Right-Wing, Left-Wing, and Center, and write them to the files toronto_right_users, toronto_left_users, toronto_center_users

get_world_biases.py - calculates the average non-Toronto user bias score for each day in 2022, and writes them to the file world_bias_scores.csv

get_world_infos.py - calculates the average non-Toronto user misinformation score for each day in 2022, and writes them to the file world_info_scores.csv

get_domain_rankings/domain_scrape.py + get_domain_rankings/generate_full_domain_list.py - use these files to scape mediabiasfactchack.com to get the trustworthiness and bias ratings for each domain in the dataset.

**To generate a regression result:**

Go to the "generate_figures" and go to the regression you would like to generate. Run the "toronto_domain_list.py" file, this will generate a file containing all interactions of each Toronto user for each day for the user bias group relevent to the regression. The run "generate_regression.py" in order to generate the regression CSV file, which can then be put into R or some other software to run the regression. In the folder for each regression, the final regression csv has already been generated, so you can go in and see all the rows. A full report on each regression is also included in regression_results.txt.
