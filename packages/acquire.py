######################################### IMPORTING LIBRARIES #################################################
from selenium import webdriver
import os
from dotenv import load_dotenv
import time

######################################### IMPORTING DATA #################################################
def getting_data():

    # job_title
    #job_title_input = input("PLEASE ENTER THE JOB THAT YOU'D LIKE TO SEARCH: ")
    job_title_input = 'data analyst'
    job_title = job_title_input.lower().replace(' ', '%20')

    # location
    #location_input = input("PLEASE ENTER THE LOCATION WHERE YOU'D LIKE TO SEARCH: ")
    location_input = 'Berlin'
    location = location_input.capitalize()

    # Driver PATH
    os.environ['PATH'] = f'{os.environ["PATH"]}:/home/cristopherrl/Documents/program/selenium/drivers/'

    # .env path
    #load_dotenv(dotenv_path='../.env')
    load_dotenv(dotenv_path='.env')

    # Sign In - URL
    browser = webdriver.Chrome()
    URL = 'https://www.linkedin.com/login'
    browser.get(URL)
    time.sleep(0.5)

    # Sign In - parameters
    SECRET_USER = os.getenv("SESSION_KEY")
    SECRET_PASS = os.getenv("SESSION_PASSWORD")

    user = browser.find_element_by_xpath('/html/body/div/main/div/form/div[1]/input')
    user.send_keys(SECRET_USER)
    time.sleep(0.1)

    password = browser.find_element_by_xpath('/html/body/div/main/div/form/div[2]/input')
    password.send_keys(SECRET_PASS)
    time.sleep(0.1)

    sign_in = browser.find_element_by_class_name('login__form_action_container')
    sign_in.click()
    time.sleep(1)

    # First job search URL
    JOB_URL = f'https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}&start=0'
    browser.get(JOB_URL)
    print(JOB_URL)

    # number of pages with job posts
    try:
        pages = \
            browser.find_element_by_xpath \
                ('/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/section/artdeco-pagination/ul')
    except:
        pages = \
            browser.find_element_by_xpath \
                ('/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/section/artdeco-pagination/ul')

    n_pages = int(pages.text.split('\n')[-1])
    print(n_pages)

    ########################
    # Extracting info
    last_job_page = n_pages * 25
    print(last_job_page)

    for p in range(0, last_job_page, 25):
    #for p in range(0,n_pages*25,25):
    #for p in range(0, 1):

        print(p)

        # Exploring each page with maximum 25 job posts
        JOB_URL = f'https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}&start={p}'
        browser.get(JOB_URL)

        # Taking table of job posts
        try:
            tabla_izq = \
                browser.find_element_by_xpath("/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]")
        except:
            tabla_izq = \
                browser.find_element_by_xpath("/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]")
        time.sleep(0.1)


        # Getting quantity of job posts (i) to explore on this page >
        if p < (last_job_page-25):
            job_list = tabla_izq.text.split('Manage alerts\n')[1].split('Close\n')[0].split('ago')
        # >> for last page there is another logic ( not 'Close')
        else:
            job_list = \
                tabla_izq.text.split('Manage alerts\n')[1].split('Close\n')[0].split('Create alert for this search\n')[
                    0].split('ago')
        n_job_list = len(job_list) - 1
        print(n_job_list)


        #for i in range(1, 26):
        for i in range(1,n_job_list+1):

            # Selecting job post in order
            try:
                job_post = browser.find_element_by_xpath\
                (f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a')
            except:
                job_post = browser.find_element_by_xpath\
                (f'/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a')
            print(job_post.text)
            time.sleep(0.1)
            job_post.click()
            time.sleep(0.1)

            # Getting job post ID
            print(browser.current_url)
            currentJobId = browser.current_url.split('currentJobId=')[1].split('&')[0]
            print(f'{currentJobId}')

            # Extracting job information
            try:
                job_post_right = browser.find_element_by_xpath\
                    ('/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[2]')
            except:
                job_post_right = browser.find_element_by_xpath\
                    ('/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[2]')
            job_post_right_content = job_post_right.text.split('\n', 15)
            print(len(job_post_right_content))
            print(f'{job_post_right_content}\n')


print("fin")

