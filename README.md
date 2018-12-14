# Media Framing
The bias in international news coverage

- Link to the detailed codes for the project: https://github.com/Razoff/Stark_AdA_project/blob/master/Project_Pipeline.ipynb
      
- Link to the latest version on Google Drive (space issues): https://drive.google.com/a/epfl.ch/uc?id=1XUGA7UsE8zoIUoVnnNNHJEgn7IuXwM1A&export=download

# Abstract
With the development of new technologies, people have access to tremendous amounts of sources to keep up with the events of the world. This increase of sources made it nearly impossible for people to get a sense of how biased the media are in transferring the facts and events. With an increasing number of sources, there is increasing risks of misinformation. 
The goal of our project is to raise awareness of the potential bias of news sources in each country and develop a visual representation to demonstrate it. To that aim, we used the dataset provided by the GDELT project which contains the key information needed to investigate international news coverage. 
The idea is to offer textual analysis and graphical content to present the results. We will include node graphs linking sources to one another and maps that will indicate the different characteristics of media coverage in different countries. 

# Research questions

With our work in milestone 2 we think we can answer the question below: 
- How differently are international news covered depending on the country or the media? 

By looking at the gkg dataset and using the themes of the article we will be able to answer the question below:
- Which category of news tends to be framed or less covered depending on the country or the media?

However, we will need some more work to be able to answer the questions below:
- How can we use the graph visualization to demonstrate the bias in the news sources?
- What conclusions can we draw about systematic bias in different countries by studying its media coverage?

Also given the data it will be hard to answer questions such as:
- How do media try to keep their credibility as a source of information, while introduce bias the news?


# Dataset
<a href="https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/"><b>GDELT v2.0</b></a>: The targeted dataset for this project is GDELT 2.0. Its exhaustive description of events around the globe provides tools to investigate the news coverage in different country. 
All articles and citations comes with multiple indexes (confidence, tone, Goldstein scale) that provides great insights to get an idea of the polarity of the media or even the country.
The Records are stored one per line, separated by a newline (\n) and are tab-delimited (although the files have a “.csv” extension, but are actually tab-delimited). The dataset that we will use for the project is a subset of the complete GDELT v2.0 dataset which has been stored on the ADA cluster and contains event records from February 2015 to November 2017.

<a href="https://github.com/datasets/country-codes"><b>Country-codes</b></a>: This dataset holds country code information.
In this project we are going to deal with worldwide coverage and sometimes the format kind be a little bit tricky. The csv file provided by this git repository offers an easy way to deal with different way of representing a country. Its main usage will be in helping the identification of a news sources through a website.

<a href="https://github.com/johan/world.geo.json/tree/master/countries"><b>world.geo.json</b></a>: This git repository offers annotated geo-json geometry files for the world.
The dataset will be used during the display of various event on a map. It works as follows: there is a one to one mapping from an ISO3166-1-Alpha-3 country code to a json file which once provided to good display library (in our case follium) draw any country's border. In our objectif of analysing world coverage of event this will come in very handy.  




# A list of internal milestones up until project milestone 2
- Data Cleaning: deal with empty cells, drop irrelevant columns, find interesting metrics.
- Extracting relevant features that are useful for analyzing the degree of bias for each media coverage.
- Checking the project hypothesis by sampling the data from one country and for the events with worldwide coverage.
- Look at the graph algorithms to classify the news media into ones with high bias and low bias and visualize them.
- Doing a case study on a few news media and investigate any patterns of how they try to hide the bias in the news and keep their credibility.
- Discuss the narrative of the story that we try to tell at the end of the project, and provide relevant visualizations to support that narrative.

# A list of internal milestones up until project milestone 3

- Further study of the features: With milestone 2 we understood how to aggregate the data and its potential by making simple visualizations using a subset of the features. The next step is to make an exhaustive description and a statistical analysis of all of the features contained in the datasets, including the gkg dataset.

- Biais measurement: One issue with our project is to have a way to mesure bias which can be done by using the "Average Tone" or "Goldstein Scale" however this isn't enough. It will be necessary to find a better measurement for bias. For instance we could think of ways to use either supervised or unsupervised machine learning algorithms to group news sources into clusters. This type of study will help us answer some of the questions we couldn't answer yet.

- Visualizations: We will have to come up with news visualizations and choose the best ones to answer our different key questions. Instead of maps, we will also need to have more diversified visualizations such as bar charts and graphs.

- Answer to the key questions: Using the the results of the previous step, we will ned to analyse the results and explain how we can notice biais in internation media coverage.

- Create a website containing the data story: The idea is to aggreagate everyhting that we did in this project in the form a data story. We will create a website to showcase our visualizations and analysis with each key question getting us closer to answering the main reseach question.

- Create a poster for the presentation: We will use everything we have done during the project to synthetize the main results in a poster format. 


# Questions for TAa
- How can we get a general overview of the data that is on the cluster? and What is the period of time of the extracted data?
- How can we extract relevant features from the naive features in the data set to measure the bias?
- What graph algorithms and libraries can we use for extracting insightful information and visualizing them?
