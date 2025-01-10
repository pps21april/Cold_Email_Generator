import streamlit as st
from chains import Chain
from portfolio import Portfolio
from langchain_community.document_loaders import WebBaseLoader
import bs4


def GetStreamlitApp(llm,portfolio):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-48491?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    if submit_button:
        loader = WebBaseLoader([url_input])
        page_data = loader.load().pop().page_content
        portfolio.load_portfolio()
        jobs = llm.get_jobs(page_data)

        for job in jobs:
            links = portfolio.links_list(job)
            email = llm.generate_email(job,links)
            st.code(email,language = "markdown")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    GetStreamlitApp(chain, portfolio)

