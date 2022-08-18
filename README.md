# Udacity-Capstone-Project-Starbucks
Capstone project for Udacity's nanodegree course in data science

**Starbucks Capstone Challenge**

Medium Article Link of results and procedure: https://medium.com/@deepanshupandey195/starbucks-capstone-project-udacity-data-science-nanodegree-a67acae6d37a

**Introduction**

This data set contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks.

Not all users receive the same offer, and that is the challenge to solve with this data set.

**File Descriptions**

This repo contains 4 files.There is a notebook available here to showcase work related to the above questions and wrangling process. There are 3 data files used to address the above qustions

- portfolio.json - containing offer ids and meta data about each offer (duration, type, etc.)
- profile.json - demographic data for each customer
- transcript.json - records for transactions, offers received, offers viewed, and offers completed

**Problem Statement**

- Analyse the data and perform EDA to find if any particular customer demographic group is responding/completing more offers
- Predict whether a user will complete an offer or not based on their transactions and offer viewing behaviour

**Analysis**

Since it was an open project and it had been mentioned that the student are free to create their own questions and answer it using the data, I went ahead and analysed the data for the above mentioned questions.
All the results and finding are there in the jupyter notebook and medium article which is mentioned at top of this document.
Final Model: Random Forest with 0.72 F1-score

**Licensing, Acknowledgements, etc.**
Data for project was provided by Udacity. Thank you to Udacity for setting up such a challenging and exciting problem.
