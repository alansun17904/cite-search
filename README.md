# Cite Search
Cite search is a research tool that makes research easier, faster, hassle-less. By displaying a citation web using d3.js researchers can quickly
pinpoint papers of interest one, two, three, ... up to five layers deep. Researchers can also use cite search to quickly generate BibTeX citations
which can be exported. 

## Brief Overview
This project was built for the DALI Lab Spring 2022 developer challenge. Herein, I will briefly describe some technical highlights of the project 
as well as the parts that I struggled with.

**Highlights**
- I implemented a breadth-first search that would traverse the citation graph.  
- Since any given paper may have up 50^5 citations, I had to limit the number of citations per layer. The web application
would also be making tons of API calls for any given paper. Therefore, I implemented a multi-threaded program that would
get sources quickly and efficiently. 
- This was my first time working with D3.js, I've seen it being used in Distill articles and the potential that it offers. 
Therefore, one of my goals for this challenge was to get familiar with it. I feel that I successfully built a chart that
was captivating. 

**Struggles**
- The API that I was working with had no way of getting the number of citations on a given paper a priori, without getting
all the data associated with that paper. Therefore, I could not sort the entries based on importance. If I had more time, 
I would also implement a keyword search, which would search through the title of the papers, finding and displaying only 
relevant ones.
- I did not have time to deploy the app. Given more time, I would definitely try to deploy it on Heroku. 

## Interface and Functionality
This section briefly demonstrates the interface and functionality of the platform. 

**Home Page**
![homepage](https://user-images.githubusercontent.com/37106254/153897773-80a1d8a6-70d4-4348-b6cf-1034f54e3e8f.png)

**Cite Search Picture**
![search-pic](https://user-images.githubusercontent.com/37106254/153897811-b6d0a1d2-1e36-4f92-9f43-1ee6beceaa5a.png)

**Cite Search Video**


https://user-images.githubusercontent.com/37106254/153898161-32d72023-a4a8-4c90-9edf-128924304d23.mov











## Installation
Cite search is built with Django and D3.js, it also uses the OpenCitations API to get papers of interest. To start 
clone the repositroy:
```bash
git clone git@github.com:alansun17904/cite-search.git
``` 
Then, install all dependencies using a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Now, Django, can be started using the following:
```
python manage.py runserver
```

