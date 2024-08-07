import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)


        st.title('Message Count by User')
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='user', ax=ax)
        ax.set_xlabel('User')
        ax.set_ylabel('Message Count')
        plt.xticks(rotation=80)  # Rotate x-axis labels for better readability
        st.pyplot(fig)

        # Percentage of chat contributions by each user
        st.title("Percentage of Chat Contributions by User")
        user_message_counts = df['user'].value_counts(normalize=True) * 100
        percentage_df = pd.DataFrame(
            {'User': user_message_counts.index, 'Percentage of Messages': user_message_counts.values})
        st.write(percentage_df)

        #wordcloud
    text_data = " ".join(df[df['user'] == selected_user]['message'])

    if text_data:
        # Generate the word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

        # Plot the word cloud
        st.title("Wordcloud")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')  # Disable axis
        st.pyplot(fig)
    else:
        st.write("No data available for generating the word cloud.")

        # most common words
        # Load the most common words DataFrame
        # Load the text data for word cloud
        text_data = " ".join(df[df['user'] == selected_user]['message'])

        if text_data:
            # Generate the word cloud
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

            # Plot the word cloud
            st.title("Wordcloud")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')  # Disable axis
            st.pyplot(fig)
        else:
            st.write("No data available for generating the word cloud.")



