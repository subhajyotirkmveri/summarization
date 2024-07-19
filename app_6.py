import streamlit as st 
import requests
import bs4 as bs
import base64
from PIL import Image
import PyPDF2
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompts for Gemini Pro API
base_text_prompt = """You are a document summarizer. You will take the text and summarize it, providing the important summary in points within {} to {} words. Please provide the summary of the text given here: """
base_youtube_prompt = """You are a YouTube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within {} to {} words. Please provide the summary of the text given here: """

# Function to Read .txt File and return its Text
def file_text(filepath):
    with open(filepath) as f:
        text = f.read().replace("\n", '')
        print("number of characters in this txt file =", len(text))
        return text, len(text)

# Function to preprocess and extract text from PDF
def pdf_file_preprocessing(pdf_path):
    with open(pdf_path, 'rb') as pdfFileObject:
        pdfReader = PyPDF2.PdfReader(pdfFileObject)
        count = len(pdfReader.pages)
        print("\nTotal Pages in pdf =", count)
        
        c = input("Do you want to read the entire pdf? [Y]/N: ").strip().lower()
        start_page = 1
        end_page = count 
        
        if c == 'n':
            start_page = int(input("Enter start page number (Indexing start from 1): ").strip())
            end_page = int(input(f"Enter end page number (Less than or equal to {count}): ").strip())
            
            if start_page < 1 or start_page > count:
                print("\nInvalid Start page given")
                sys.exit()
                
            if end_page < 1 or end_page > count:
                print("\nInvalid End page given")
                sys.exit()
                
        text = ""
        for i in range(start_page, end_page + 1):
            page = pdfReader.pages[i-1]
            text += page.extract_text()
        print("number of characters in this document =", len(text))   
        return text, len(text)

# Function to retrieve text from Wikipedia URL
def wiki_text(url):
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    
    # Removing all unwanted characters
    article_text = re.sub(r'\[[0-9]*\]', '', article_text)
    return article_text

# Function to generate summary using Gemini Pro API
def generate_gemini_content(text, prompt, min_words, max_words):
    full_prompt = prompt.format(min_words, max_words) + text
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(full_prompt)
    return response.text

# Function to display PDF
@st.cache_data
def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e

# Streamlit code 
st.set_page_config(page_title='Summarize Chatbot', layout="wide", page_icon="📃", initial_sidebar_state="expanded")

def main():
    st.title("Summarize Chatbot")
    image = Image.open('summary.png')
    st.image(image, width=200)

    choice = st.sidebar.selectbox("Select your choice", ["YouTube Video Transcript", "Load from .pdf file", "Load from .txt file", "From Wikipedia Page URL", "Type your Text (or Copy-Paste)"])

    min_words = st.sidebar.number_input("Minimum Words for Summary", min_value=1, value=50)
    max_words = st.sidebar.number_input("Maximum Words for Summary", min_value=1, value=250)

    if choice == "YouTube Video Transcript":
        st.title("YouTube Video Summarization")
        youtube_link = st.text_input("Enter YouTube Video Link:")
        
        if youtube_link:
            video_id = youtube_link.split("=")[1]
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        
        if st.button("Get Detailed Notes"):
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                summary = generate_gemini_content(transcript_text, base_youtube_prompt, min_words, max_words)
                st.markdown("## Detailed Notes:")
                st.write(summary)

    elif choice == "Load from .pdf file":
        st.subheader("Summarize Document")
        uploaded_file = st.file_uploader("Upload your document here", type=['pdf'])

        if uploaded_file:
            if not os.path.exists("uploaded_pdfs/"):
                os.makedirs("uploaded_pdfs/")
                print("uploaded_pdfs Folder created successfully")
            else:
                print("uploaded_pdfs Folder already exists")   
                      
            filepath = "uploaded_pdfs/" + uploaded_file.name
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("PDF file uploaded successfully!")
            
            if st.button("Summarize Document"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.info("Display document")
                    pdf_view = displayPDF(filepath)
                    st.info("Navigate to the terminal to select the number of pages you'd like to summarize")

                with col2:
                    input_text, input_length = pdf_file_preprocessing(filepath)                
                    summary = generate_gemini_content(input_text, base_text_prompt, min_words, max_words)
                    st.info("Summarization")
                    st.success(summary)
                    
            # Option to delete all uploaded files
            if st.button("Delete Uploaded Files"):
                folder = "uploaded_pdfs/"
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        st.error(f"Error: {e}")                      

    elif choice == "Load from .txt file":
        st.subheader("Summarize text Document")
        uploaded_file = st.file_uploader("Upload your .txt file here", type=['txt'])
        if uploaded_file is not None:
            if st.button("Summarize text Document"):
                col1, col2 = st.columns([1, 1])
                if not os.path.exists("uploaded_txts/"):
                    os.makedirs("uploaded_txts/")
                    print("uploaded_txts Folder created successfully")
                else:
                    print("uploaded_txts Folder already exists")
                    
                filepath = "uploaded_txts/" + uploaded_file.name

                with open(filepath, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())

                with col1:
                    st.info(" Text file uploaded successfully")
                    with open(filepath, "r") as file:
                        file_contents = file.read()
                        st.text_area("Text File Contents", value=file_contents, height=400)

                with col2:
                    input_text, input_length = file_text(filepath)                
                    summary = generate_gemini_content(input_text, base_text_prompt, min_words, max_words)
                    st.info("Summarization")
                    st.success(summary) 
                    
            # Option to delete all uploaded txt files 
            if st.button("Delete Uploaded Files"):
                folder = "uploaded_txts/"
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        st.error(f"Error: {e}")                  
      
    elif choice == "From Wikipedia Page URL":
        app_heading_html =  f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open("logo.png", "rb").read()).decode()}" width=70 height=70>
            <p class="logo-text">{"Wikipedia summarization"}</p>
        </div>
        """

        st.markdown(app_heading_html, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            wiki_URL = st.text_input('Enter the URL of the Wikipedia article to analyze.', value="", placeholder='https://en.wikipedia.org/wiki/')
            if wiki_URL:
                st.components.v1.iframe(src=wiki_URL, width=None, height=550, scrolling=True)

        with col2:
            if wiki_URL:
                if st.button("Summarize"):
                    summary = generate_gemini_content(wiki_text(wiki_URL), base_text_prompt, min_words, max_words)
                    st.success(summary)

    elif choice == "Type your Text (or Copy-Paste)":
        st.subheader("Summarize Text")
        input_text = st.text_area("Enter your text here")
        if input_text is not None:
            if st.button("Summarize Text"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("**Your Input Text**")
                    st.info(input_text)
                with col2:
                    st.markdown("**Summary Result**")
                    result = generate_gemini_content(input_text, base_text_prompt, min_words, max_words)
                    st.success(result)

# Initializing the app
if __name__ == "__main__":
    main()

