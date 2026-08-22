# Python_URL_Shortener

> git clone https://github.com/sunaina156/Python_URL_Shortener.git

# create virtual environment
> python --version
> python -m venv venv  
# means python run the venv module and create an evironment named "venv" 
> .\venv\Scripts\Activate.ps1 
we will see (venv) in terminal means our virtual environment is active.


# create directory structure
Python_URL_Shortener/
│
├── venv/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md

# create .gitignore 
venv/

# create requirements.txt

> git status
> git add . 
> git commit -m "message"
> git push 


# CLI-based URL Shortener:

User enters Long URL
        ↓
Python generates Short Code
        ↓
Long URL + Short Code stored
        ↓
User enters Short Code
        ↓
Python returns Original URL

# * Created `main.py` and implemented the URL Shortener logic using Python.
* Created a function to generate random 6-character short codes.
* Stored short codes and original URLs using a Python dictionary.
* Added URL retrieval and a menu-driven CLI with invalid-code handling.


