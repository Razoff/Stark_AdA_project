# Media Framing
The bias in international news coverage

# Abstract
With the development of new technologies, people have access to tremendous amounts of sources to keep up with the events of the world. This increase of sources made it nearly impossible for people to get a sense of how biased the media are in transferring the facts and events. With an increasing number of sources, there is increasing risks of misinformation. 
The goal of our project is to raise awareness of the potential bias of news sources in each country and develop a visual representation to demonstrate it. To that aim, we used the dataset provided by the GDELT project which contains the key information needed to investigate international news coverage. 
The idea is to offer textual analysis and graphical content to present the results. We will include node graphs linking sources to one another and maps that will indicate the different characteristics of media coverage in different countries. 

# Research questions
- How differently are international news covered depending on the country or the media? 

- Which category of news tends to be framed or less covered depending on the country or the media?

- How do media try to keep their credibility as a source of information, while introduce bias the news?

- How can we use the graph visualization to demonstrate the bias in the news sources?

- What conclusions can we draw about systematic bias in different countries by studying its media coverage?



# Dataset
<a href="https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/"><b>GDELT v2.0</b></a>: The targeted dataset for this project is GDELT 2.0. Its exhaustive description of events around the globe provides tools to investigate the news coverage in different country. 
All articles and citations comes with multiple indexes (confidence, tone, Goldstein scale) that provides great insights to get an idea of the polarity of the media or even the country.


# A list of internal milestones up until project milestone 2
- Data Cleaning: deal with empty cells, drop irrelevant columns, find interesting metrics.
- Extracting relevant features that are useful for analyzing the degree of bias for each media.
- Checking the project hypothesis by sampling the data from one country and for the events with worldwide coverage.
- Look at the graph algorithms to classify the news media into ones with high bias and low bias and visualize them.
- Doing a case study on a few news media by looking into different categories of news and investigate any patterns of how they try to hide their bias and keep their credibility.
- Discuss the narrative of the story that we try to tell at the end of the project, and provide relevant visualizations to support that narrative.


# Questions for TAa
- How can we get a general overview of the data that is on the cluster? and What is the period of time of the extracted data?
- How can we extract relevant features from the naive features in the data set to measure the bias?
- What graph algorithms and libraries can we use for extracting insightful information and visualizing them?
