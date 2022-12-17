import streamlit as stl
import preprocessor
import stats
import matplotlib.pyplot as plt
import seaborn as sns

stl.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = stl.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    users = df['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0, "All")

    selection = stl.sidebar.selectbox("Filter Group Member", users)

    if stl.sidebar.button("Generate Report"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = stats.stats(selection, df)
        stl.title("Statistical Report")
        col1, col2, col3, col4 = stl.columns(4)

        with col1:
            stl.header("Messages Sent")
            stl.title(num_messages)
        with col2:
            stl.header("Words Typed")
            stl.title(words)
        with col3:
            stl.header("Media Shared")
            stl.title(num_media_messages)
        with col4:
            stl.header("Links Shared")
            stl.title(num_links)

        stl.title("Monthly Timeline")
        timeline = stats.monthly_timeline(selection, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        stl.pyplot(fig)


        stl.title("Daily Timeline")
        daily_timeline = stats.daily_timeline(selection, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        stl.pyplot(fig)


        stl.title('Activity Timeline')
        col1, col2 = stl.columns(2)

        with col1:
            stl.header("Most busy day")
            busy_day = stats.week_activity_map(selection, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            stl.pyplot(fig)

        with col2:
            stl.header("Most busy month")
            busy_month = stats.month_activity_map(selection, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            stl.pyplot(fig)

        stl.title("Weekly Activity Map")
        user_heatmap = stats.activity_heatmap(selection, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        stl.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selection == 'All':
            stl.title('Most Active User')
            x, new_df = stats.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = stl.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                stl.pyplot(fig)
            with col2:
                stl.dataframe(new_df)

        # WordCloud
        stl.title("Wordcloud")
        df_wc = stats.create_wordcloud(selection, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        stl.pyplot(fig)

        # most common words
        most_common_df = stats.most_common_words(selection, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        stl.title('Frequently Used words')
        stl.pyplot(fig)

        # emoji analysis
        emoji_df = stats.emoji_helper(selection, df)
        stl.title("Emoji Analysis")

        col1, col2 = stl.columns(2)

        with col1:
            stl.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            stl.pyplot(fig)

        x,y,z = stats.senti_analyzer(selection, df)
        total=x+y+z
        stl.title("Sentimental Analysis Report")
        col1, col2, col3 = stl.columns(3)

        with col1:
            stl.header("Positive Conversations")
            stl.title(str(round((x/total)*100))+"%")
        with col2:
            stl.header("Neutral  Conversations")
            stl.title(str(round((z/total)*100))+"%")
        with col3:
            stl.header("Negative Conversations")
            stl.title(str(round((y/total)*100))+"%")


