import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,
               model_name = "llama-3.3-70b-versatile",
               groq_api_key = os.getenv("GROQ_API_KEY"))

    def get_jobs(self,page_data):
        prompt_extract = PromptTemplate.from_template(

            """
            # SCRAPED DATA FROM WEBSITE
            {page_data}
            # INSTRUCTION
            Extract the job postings from the above scraped data and return them in a JASON format having the 
            following keys - skills, experience, role and description
            Only return the valid JASON  
            # VALID JASON (No Preamble)                                          

            """
        )

        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke(input={"page_data": page_data})
        json_parser = JsonOutputParser()
        res = json_parser.parse(res.content)
        return res if isinstance(res, list) else [res]

    def generate_email(self,job,links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Prashant, a Sales Manager at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
            Remember you are Mohan, BDE at AtliQ. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content