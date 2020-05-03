
### OPTJOBS: Optimazed Job Search

### **Status**
This is my Ironhack Data Analytics Final Project

###**One-liner**
This project consist in recognize the main features of a specific job search in order to apply to job offers that fit better to our profile

### **Technology stack**
Python / Pandas / Regex / OS / Matplotlib / Web Scrapping: Selenium / NLP: Spacy / Wordcloud / Collections

### **Core technical concepts and inspiration**
This project was born considering the need of job searching. There was a gap identified when a key word is used to find a job, because sometimes offers have descriptions which don't match with the normal description we know about some data profile (for example, Data Analyst), and there aren't coincidences neither with our profiles.
So, this project evaluate the main words in the total job offers and also compare every job post with our profile and recognize the best matches.

### **Configuration**
Requeriments: It was developed for Linux. For Windows it's necessary to do some tests. The basis of searching is having a LinkedIn profile (not necessary a Premium one)

### **Usage**
Return values: When a Web Scrapping or a recorded search is loaded, then we'll have as results: a html table with best matches, json files with most common words, a word cloud for every profile in different languages.

### **Folder structure**
```
└── project
    ├── .gitignore
    ├── requeriments.txt
    ├── README.md
    ├── main.py
    ├── notebooks
    │   ├── 1_Acquire.ipynb
    │   └── 2. Analyze.ipynb
    ├── packages
    │   ├── acquire.py
    │   └── analyze.py
    └── data
        ├── raw
        └── results
```

### **ToDo**
Next steps, features planned, known bugs (shortlist).

### **Contact info**
if you need some help or you want to give some feedback, please write to this email: cristopher.rojas.lepe@gmail.com
 
