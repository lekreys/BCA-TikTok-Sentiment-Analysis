import streamlit as st
import helper
import preprocessing

st.set_page_config(layout="wide")


st.title(":blue[BCA TikTok Comments ( Sentiment Analysis )]")
st.markdown('This application offers in-depth insights into customer feedback on TikTok for BCA, specifically focusing on analyzing user comments to gauge overall sentiment. It identifies both positive and negative feedback, and categorizes complaints into several distinct groups, such as app-related technical issues, customer service challenges, transaction problems, and more. By utilizing sentiment analysis, this app helps provide a clearer understanding of how users perceive the BCA experience, enabling the identification of trends, areas of concern, and potential improvements that can enhance customer satisfaction and service efficiency.')

st.divider()
urls = st.text_input("Paste URLs ( use commas to separate multiple URLs ): " , placeholder="Max 3 urls")

ids = helper.get_id(urls=urls)

st.caption(f"Total number of videos selected for analysis: {len(ids)}")

if st.button("Perform Sentiment Analysis") :

  try : 
    data = helper.scrap_data(ids)
  except : 
    st.error("Failed to scrape data, please try again or reduce the number of URLs.")


  data['preprocessing'] = data.comments.apply(preprocessing.preprocessing)
  data['Sentiment'] = preprocessing.predict_sentiment(data)

  data_disp = data.copy()

  preprocessing.mapping_sentimen(data_disp)

  col1 , col2 = st.columns([1.4,1])

  with col1 : 
    st.dataframe(data_disp[['comments' , "Sentiment"]] , height=500 , width=1000)

  with col2 :

    num_sentiment = helper.metric_sentiment(data=data[['Sentiment']])

    positive = num_sentiment[0]
    negative = num_sentiment[1]

    st.title(f":red[Complaint]        : {round((negative / (negative + positive)) * 100, 2)}% ( {negative} )")
    st.title(f":green[Non-Complaint]  : {round((positive / (negative + positive)) * 100, 2)}% ( {positive} )")
    st.title(f":blue[Total Comments]  : {data.shape[0]}")

  
  st.divider()


  tab1, tab2, tab3 , tab4 = st.tabs(["Application", "Service", "Credit-Card" , "Non-Categorize"])

  data_cat = data[data.Sentiment == 1 ]
  data_cat["Category"] = preprocessing.predict_sentiment_cat(data_cat)

  preprocessing.mapping_cat(data_cat)

  with tab1 : 
    col1 , col2 = st.columns([1,3])

    app_data = data_cat[data_cat.Category == "app"][['comments' , "Category"]]

    with col1 :
     st.header("Total Complaints about the Application :")
     st.header(app_data.shape[0])
    with col2 :
     st.dataframe(app_data , width=1000)

  with tab2 : 
    col1 , col2 = st.columns([1,3])

    service_data = data_cat[data_cat.Category == "Service"][['comments' , "Category"]]

    with col1 :
     st.header(f"Total Complaint about the Service :")
     st.header(service_data.shape[0])
    with col2 :
     st.dataframe(service_data , width=1000)

  with tab3 : 
    col1 , col2 = st.columns([1,3])

    Credit_data = data_cat[data_cat.Category == "Credit"][['comments' , "Category"]]

    with col1 :
     st.header(f"Total Complaint about the Credit-Card :")
     st.header(Credit_data.shape[0])
    with col2 :
     st.dataframe(Credit_data , width=1000)

  with tab4 : 
    col1 , col2 = st.columns([1,3])

    non_category_data = data_cat[data_cat.Category == "Non-Category"][['comments' , "Category"]]

    with col1 :
     st.header(f"Total Complaint about the Non-Category :")
     st.header(non_category_data.shape[0])
    with col2 :
     st.dataframe(non_category_data , width=1000)  
  





  




