import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title('Sentiment Analysis of tweets about US Airlines!')

st.sidebar.title("Sentiment Analysis of tweets about US Airlines!")

st.markdown(" This application is a streamlit dashboard used to analyze sentiments of the tweets.")
st.sidebar.markdown(" This application is a streamlit dashboard used to analyze sentiments of the tweets.")

@st.cache(persist = True)
def load_data():
    data = pd.read_csv('Tweets.csv')
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.write(data)

st.sidebar.subheader("Show random tweet")

random_tweet = st.sidebar.radio('Sentiment',('positive','neutral','negative'))

st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n = 1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment")

option = st.sidebar.selectbox('Visualization',['Histogram','Pie chart'], key = '1')

sentiment_count = data['airline_sentiment'].value_counts()

sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox("Hide",True):
    st.markdown("### Number of tweets per sentiment")
    if option == "Histogram":
        fig = px.bar(sentiment_count, x = "Sentiment", y = "Tweets", color = "Tweets", height = 500)
        st.plotly_chart(fig)
    elif option == "Pie chart":
        fig = px.pie(
            sentiment_count, values = "Tweets", names = "Sentiment")
        st.plotly_chart(fig)

st.sidebar.subheader("When are users tweeting?")

hour = st.sidebar.slider("Hour of day", 0,23)
# hour = st.sidebar.number_input("Hour of day", 1,24)

modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close", True, key = '1'):
    st.markdown('### Tweets locations based on the time of day')
    st.markdown("%i tweets between %i:00 and %i:00 hours" % (len(modified_data), hour, (hour + 1) % 24))
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiments")

airlines = data['airline'].unique()
choice = st.sidebar.multiselect("Pick airlines", airlines,key = '1')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig = px.histogram(choice_data,x = "airline",y = "airline_sentiment",histfunc = 'count',color = 'airline_sentiment',facet_col = "airline_sentiment",labels = {'airline_sentiment': 'tweets'})
    st.plotly_chart(fig)

st.sidebar.subheader("Word Cloud")

word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?',['positive','neutral','negative'])

if not st.sidebar.checkbox("Close", True, key = "2"):
    st.subheader('word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white',width = 800, height = 640).generate(processed_words)
    plt.imshow(wordcloud)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()

        