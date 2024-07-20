## Purpose :- 

To save time while reading by summarizing a large article in english language or text in english language or youtube video in english language into fewer lines. 

1. # Configuring
First create a virtual environemnt.
```
python -m venv env
```
or go to terminal and create a new environment by typing below cmd
```
conda create -p venv python=3.10 -y
```

2. Activate the new terminal
```
conda activate venv
```
3. Clone this repository:
   
```
 git clone https://github.com/subhajyotirkmveri/summarization.git
 
```
4. Go to the cloning folder
```
cd summarization
```
5. Within this directory create a .env file which contain the below thing
```
GOOGLE_API_KEY = "put your api key here"
```
6. Install all the depenedencies :   
```
pip install -r requirements.txt
```

7. Open terminal and run the following command:
```
streamlit run app_5.py
```
or 
```
streamlit run app_6.py
```
and for youtube video summarization run the following command:
```
streamlit run app.py
```
## Application Preview :
You can select text from your lengthy article in five ways:-
![image](https://github.com/subhajyotirkmveri/summarization/blob/main/asset/asset_21.jpeg)

  - By putting youtube url
  - Reading the text from **.txt file**.
  - Reading the text from **.pdf file**.(You can choose either to get summary of entire pdf or select any page interval).
  
  - Reading the text from **wikipedia page** (All you have to do is to provide the url of that page. Program will automatically scrap the text and summarise it for you).
  - By typing text on your own (or copy-paste).
  

 
## Output :- 
- This is a portion of the summary text returned by the program when selecting "youtube video transcript"
Click the "Summarize" button for summarize the input text:-
![image](https://github.com/subhajyotirkmveri/summarization/blob/main/asset/asset_22.jpeg)


- This is a snippet of the summary text returned by the program if ".txt" is chosen, you can also accordingly choose minimun number of token and maximum number of token and press enter for taking those value and upload any .txt file:-

Click the "Summarize" button for summarize the .txt file:
![image](https://github.com/subhajyotirkmveri/summarization/blob/main/asset/asset_23.jpeg)

- This is a portion of the summary text provided by the program when selecting the ".pdf" option
  upload any .pdf file:-

Click the "Summarize" button and navigate to the terminal. Then, input the page number you wish to summarize by typing an integer value. If you type "Y" then it summarize whole document: one such sample given below
![image](https://github.com/subhajyotirkmveri/summarization/blob/main/asset/asset_24.jpeg)
