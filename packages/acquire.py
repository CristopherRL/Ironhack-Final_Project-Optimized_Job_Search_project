######################################### IMPORTING LIBRARIES #################################################
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as windowsclosed
import os
import time
import re
import pandas as pd
from datetime import datetime, timedelta
import getpass
import platform

######################################### IMPORTING DATA #################################################
def getting_data():

    # STARTING
    print("""
    *******************  OPTIMIZED JOB SEARCH ON LINKEDIN *******************

    Welcome!

    This search has been created initially to find job posts on LinkedIn related with: 
    Data Analyst - Data Scientist - Data Engineer

    Please tell me what would you like to do >>>
    1: Start a new search in LinkedIn
    2: Load a recorded search""")

    option_selected = input("   > ")

    if option_selected == '1':
        df_profile, df_job = new_search()
    elif option_selected == '2':
        df_profile, df_job = recorded_search()
    else:
        raise ValueError("Sorry! The option selected is not allowed. Exit and try again")

    input()
    #os.system("pause")

    return df_profile, df_job

def new_search():

    ### SEARCH INFORMATION
    print("""\n\n   *********** NEW SEARCH :
    Please enter your information to sign in on LINKEDIN and begin the search >>>
    """)
    SECRET_USER = input("   EMAIL: ")
    SECRET_PASS = getpass.getpass(" PASSWORD: ")

    # location
    location_input = input("\n  Please enter the location (CITY) where you'd like to search: ")
    location = location_input.capitalize()

    ### SELENIUM DRIVER
    # LINUX
    if platform.system() == 'Linux':
        os.environ['PATH'] = f'{os.environ["PATH"]}:/home/cristopherrl/Documents/program/selenium/drivers/'

    elif platform.system() == 'Windows':
        os.environ['PATH'] = f'{os.environ["PATH"]};C:\\Users\\x385645\\Documents\\Selenium'


    ### SIGN IN - URL
    browser = webdriver.Chrome()
    URL = 'https://www.linkedin.com/login'
    browser.get(URL)
    time.sleep(0.5)

    try:
        # user box
        user = browser.find_element_by_xpath('/html/body/div/main/div/form/div[1]/input')
        user.send_keys(SECRET_USER)
        time.sleep(1)

        # password box
        password = browser.find_element_by_xpath('/html/body/div/main/div/form/div[2]/input')
        password.send_keys(SECRET_PASS)
        time.sleep(1)

        # sign in button
        sign_in = browser.find_element_by_class_name('login__form_action_container')
        sign_in.click()
        time.sleep(1)

    except:
        raise ValueError("  WRONG INFORMATION GIVEN!!! Please close and try again ... ")



    ################################## LINKEDIN PROFILE ######################################

    ### MAIN PAGE
    # Click on profile button (up-rigth)
    profile = browser.find_element_by_id('profile-nav-item')
    # profile = browser.find_element_by_xpath('/html/body/header/div/nav/ul/li[6]/div/artdeco-dropdown/artdeco-dropdown-trigger/div')
    profile.click()
    # Click on View profile button
    # link_profile = browser.find_element_by_xpath('/html/body/header/div/nav/ul/li[6]/div/artdeco-dropdown/artdeco-dropdown-content/div/ul/li[1]/a/div[2]/span')
    link_profile = browser.find_element_by_xpath("//span[@class='artdeco-button artdeco-button--tertiary artdeco-button--fluid']")
    link_profile.click()


    ### PROFILE
    browser.maximize_window()
    html_body = browser.find_element_by_xpath('/html/body')
    html_body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    linkedin_profile = browser.current_url.split('/')[4]

    print(f"""  > LINKEDIN PROFILE: {linkedin_profile}
    """)

    ### HEADLINE
    profile_headline = browser.find_element_by_xpath("//h2[@class='mt1 t-18 t-black t-normal']")
    headline = profile_headline.text.lower()
    print(' Loading PROFILE > OK')

    ### OPEN STATUS
    profile_open = browser.find_element_by_xpath("//artdeco-carousel-content[@class='artdeco-carousel__content']")
    if profile_open.text.split(" ")[0] == 'Open':
        open_status = True
    else:
        open_status = False
    print(' Loading OPEN STATUS > OK')

    ### ABOUT
    # show MORE > button "see more "
    profile_show_about = browser.find_element_by_xpath("//span[@class='lt-line-clamp__line lt-line-clamp__line--last']")
    ActionChains(browser).move_to_element(profile_show_about).perform()
    profile_show_about.click()
    print(' Loading ABOUT > OK')

    ### HEADLINE
    profile_about = browser.find_element_by_xpath("//p[@class='pv-about__summary-text mt4 t-14 ember-view']")
    about = profile_about.text.lower()
    print(' Loading HEADLINE >')

    ### JOB EXPERIENCE
    html_body.send_keys(Keys.PAGE_DOWN * 5)
    time.sleep(0.2)
    html_body.send_keys(Keys.PAGE_DOWN * 5)
    time.sleep(0.2)
    # show MORE experiences > button "show more experience"
    profile_show_experience = browser.find_element_by_xpath \
        ("//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']")
    ActionChains(browser).move_to_element(profile_show_experience).perform()
    profile_show_experience.click()
    html_body.send_keys(Keys.PAGE_UP)
    profile_experience = browser.find_element_by_id('experience-section')
    # getting info: time experience
    pattern_t1 = 'Employment Duration\n(.*)\nLocation'
    time_experience = list(re.findall(pattern_t1, profile_experience.text))
    # getting info: name experience
    pattern_n1 = '\n(.*)\ncompany name'
    name_experience1 = list(re.findall(pattern_n1, profile_experience.text.lower()))
    pattern_n2 = 'title\n(.*)\n'
    name_experience2 = list(re.findall(pattern_n2, profile_experience.text.lower()))
    name_experience = name_experience1 + name_experience2
    name_experience.remove('see more')
    # Calculating years of experience
    y, m = 0, 0
    for t in time_experience:
        if re.findall('[0-9] yr', t):
            year = re.findall('[0-9] yr', t)[0].split(" ")[0]
            y += int(year)
        if re.findall('[0-9] mo', t):
            month = re.findall('[0-9] mo', t)[0].split(" ")[0]
            m += int(month)
    m_nuevo = m // 12
    y_nuevo = y + m % 12
    print(' Loading JOB EXPERIENCE >')

    ### EDUCATION
    profile_education = browser.find_element_by_id('education-section')
    # getting info: degrees
    pattern_e1 = 'degree name\n(.*)\n'
    degrees = re.findall(pattern_e1, profile_education.text.lower())
    # getting info: grades
    pattern_e2 = 'field of study\n(.*)\n'
    fields = re.findall(pattern_e2, profile_education.text.lower())
    print(' Loading EDUCATION > OK')

    ### SKILLS

    # show MORE skills > > button "show more..."
    profile_more_skills = browser.find_element_by_xpath("//button[@data-control-name='skill_details']")
    ActionChains(browser).move_to_element(profile_more_skills).perform()
    profile_more_skills.click()
    html_body.send_keys(Keys.PAGE_UP)
    # skill table> text
    profile_skills_details = browser.find_element_by_xpath \
        ("//section[@class='pv-profile-section pv-skill-categories-section artdeco-container-card ember-view']")
    # Extracting skills
    skills = profile_skills_details.text.split("\n")
    not_needed_words = ['Skills & Endorsements',
                        'Add a new skill',
                        'Take skill quiz',
                        'Passed: LinkedIn Assessments',
                        'Tools & Technologies',
                        'Interpersonal Skills',
                        'Languages',
                        'Other Skills',
                        'Show less',
                        ]
    # Getting just necesary skills
    skills_delete = []
    for s in skills:
        if (s in not_needed_words) or re.search('ndorse', s) or re.search('Show only', s) or re.search('[0-9]', s):
            skills_delete.append(s)
    skills_clean = list(set(skills) - set(skills_delete))
    skills_clean = [x.lower().split(' (')[0] for x in skills_clean]
    skills_clean.sort()
    print(' Loading SKILLS >')

    ### LANGUAGES
    languages = browser.find_element_by_id('languages-expandable-content').text.split(' ')
    languages = [x.lower() for x in languages]
    print(' Loading LANGUAGES >')

    ### TOTAL SKILLS
    total_skills = sorted(list(set(degrees + fields + skills_clean + languages)))

    ### RAW PROFILE
    profile_raw = browser.find_element_by_xpath("//main[@class='core-rail']").text.replace("\n", " ")

    ### DF PROFILE (1ST RESULT)
    # Creating df_profile
    profile = [linkedin_profile, headline, open_status, about, name_experience, time_experience,
               y_nuevo, degrees, fields, skills_clean, languages, total_skills, profile_raw]

    df_profile = pd.DataFrame(profile,
                              index=['profile',
                                     'headline',
                                     'open new jobs',
                                     'about',
                                     'experiences',
                                     'years of experiences',
                                     'total years',
                                     'degrees',
                                     'fields',
                                     'skills',
                                     'languages',
                                     'total skills',
                                     'profile raw'

                                     ],
                              columns=['info']
                              )
    print(" >>> PROFILE LOADED!!!\n")

    ################################## LINKEDIN JOB SEARCH ######################################
    ### PARAMETERS

    # Jobs search
    jobs_list = ['data analyst', 'data scientist', 'data engineer']

    # Defining current date time
    now = datetime.now()
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    ### FUNCTIONS >

    # number of pages with job posts considering job title given to thi
    def n_pages_linkedin(browser, job_title_s, location):

        JOB_URL = f'https://www.linkedin.com/jobs/search/?keywords={job_title_s}&location={location}'
        browser.get(JOB_URL)
        time.sleep(1)

        # Total results
        results = browser.find_element_by_xpath("//small[@class='display-flex t-12 t-black--light t-normal']").text
        print(f'TOTAL RESULTS:{results}')
        results = int(results.split(" ")[0])

        if results > 25:
            pages = browser.find_element_by_xpath(
                "//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']")
            n_pages = int(pages.text.split('\n')[-1])
            return n_pages  # ,results

        else:
            n_pages = 1
            return n_pages  # ,results

    # Iterator of JOB POSTS > the only way is considering XPATH with an iteration
    def j_post(browser, i):
        if browser.find_element_by_xpath \
            (f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a'):
            job_post = browser.find_element_by_xpath \
            (f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a')
        elif browser.find_element_by_xpath \
            (f'/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a'):
            job_post = browser.find_element_by_xpath \
            ('/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a')

        elif browser.find_element_by_xpath \
            (f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a'):
            job_post = browser.find_element_by_xpath \
            (f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a')

        elif browser.find_element_by_xpath \
            (f'/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a'):
            job_post = browser.find_element_by_xpath \
            (f'/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3/a')

        return job_post

    print(f"""  > LINKEDIN JOB SEARCH: {jobs_list} \n""")

    # Creating empty df
    df_jobs = pd.DataFrame(columns=['JOB TITLE',
                                    'LOCATION',
                                    'SEARCH DATETIME',
                                    'Current Job Id',
                                    'Job html',
                                    'Job name',
                                    'Company name',
                                    'Company location',
                                    'Posted date',
                                    'Estimated post date',
                                    'Easy apply',
                                    'Job Description',
                                    'Skills match',
                                    'Seniority Level',
                                    'Industry',
                                    'Employment Type',
                                    'Job Functions',
                                    'Job info'
                                    ])

    ### ITERATOR OF JOB PAGES
    try:

        for j in jobs_list:
            count = 0

            # Getting each job for the search
            print(f'++++++++++++++++  {j} +++++++++++++++++++')
            job_title_df = j
            job_title_s = j.replace(' ', '%20')

            # Getting number of pages for each search
            n_pages = n_pages_linkedin(browser, job_title_s, location)
            # total_results +=results
            last_job_page = n_pages * 25

            # *************************************************************************
            # iterator of JOB PAGES
            for p in range(0, last_job_page, 25):

                # Exploring each page with maximum 25 job posts
                JOB_URL = f'https://www.linkedin.com/jobs/search/?keywords={job_title_s}&location={location}&start={p}'
                browser.get(JOB_URL)

                if p == 0:
                    time.sleep(2)
                else:
                    time.sleep(0.5)

                # Taking table of job posts
                tabla_izq = browser.find_element_by_xpath \
                    ("//div[@class='jobs-search-results jobs-search-results--is-two-pane']")

                # iterator of JOB LIST - jobs posts
                i = 1
                error = False
                while i <= 25 and error == False:

                    try:

                        # Selecting job post in order to click on it
                        job_post = j_post(browser, i)

                        job_post.click()
                        time.sleep(0.1)

                        # Getting current job ID
                        currentJobId = browser.current_url.split('currentJobId=')[1].split('&')[0]  # col1_pd
                        # if you wanna watch the job page
                        job_html = f'https://www.linkedin.com/jobs/view/{currentJobId}/'

                        # Extracting job information on the right side
                        job_post_right = browser.find_element_by_xpath(
                            "//div[@class='jobs-search-two-pane__details pt4 ph3 jobs-search-two-pane__details ember-view']")

                        ##################################################################################################
                        # Job name
                        job_post_name = job_post_right.text.split('\n', 1)[0]

                        # Company name > Sometimes there is no info here
                        if job_post_right.text.split('Company Name\n', 1)[1].split('\n')[0] == 'Company Location':
                            job_post_company_name = ""
                        else:
                            job_post_company_name = job_post_right.text.split('Company Name\n', 1)[1].split('\n')[0]

                        # Location
                        job_post_company_location = job_post_right.text.split('Company Location\n', 1)[1].split('\n')[0]

                        # Posted date
                        job_post_posted_date = job_post_right.text.split(' ago', 1)[0].split('Posted Date\nPosted ')[1]
                        if job_post_posted_date.split(" ")[1] in ['hour', 'hours']:
                            job_post_estimated_date = now - timedelta(hours=int(job_post_posted_date.split(" ")[0]))
                        elif job_post_posted_date.split(" ")[1] in ['day', 'days']:
                            job_post_estimated_date = now - timedelta(days=int(job_post_posted_date.split(" ")[0]))
                        elif job_post_posted_date.split(" ")[1] in ['week', 'weeks']:
                            job_post_estimated_date = now - timedelta(weeks=int(job_post_posted_date.split(" ")[0]))
                        elif job_post_posted_date.split(" ")[1] in ['month', 'months']:
                            job_post_estimated_date = now - timedelta(weeks=4 * int(job_post_posted_date.split(" ")[0]))
                        elif job_post_posted_date.split(" ")[1] in ['year', 'years']:
                            job_post_estimated_date = now - timedelta(
                                weeks=365 * int(job_post_posted_date.split(" ")[0]))

                        # Easy apply: T/F
                        try:
                            if job_post_right.text.split('Save\n', 1)[1].split('\n', 2)[1] == 'Easy Apply':
                                job_post_easy_apply = True
                            else:
                                job_post_easy_apply = False
                        except:
                            if job_post_right.text.split('Unsave\n', 1)[1].split('\n', 2)[1] == 'Easy Apply':
                                job_post_easy_apply = True
                            else:
                                job_post_easy_apply = False

                        # Skills match
                        if re.search('\nHow you match', job_post_right.text):
                            # if '\nHow you match' in job_post_right.text:
                            y = 'Match\n(.*)\n'
                            n = 'No match\n(.*)\n'
                            job_post_skills_match = re.findall(y, job_post_right.text)
                            job_post_skills_nomatch = re.findall(n, job_post_right.text)
                            job_post_skills = {'yes': job_post_skills_match,
                                               'no': job_post_skills_nomatch,
                                               'all': job_post_skills_match + job_post_skills_nomatch
                                               }
                        else:
                            job_post_skills_match = {}

                        ####
                        # Extracting job information on the right side
                        job_post_right_description = \
                            browser.find_element_by_xpath(
                                "//div[@class='jobs-box jobs-box--fadein jobs-box--full-width jobs-box--with-cta-large jobs-description jobs-description--reformatted ember-view']").text

                        # Seniority Level
                        try:
                            job_post_seniority_level = job_post_right.text.split('Seniority Level\n', 1)[1].split('\n')[
                                0]
                        except:
                            job_post_seniority_level = ""

                        # Industry
                        try:
                            job_post_industry = job_post_right.text.split('Industry\n', 1)[1].split('\n')[0]
                        except:
                            job_post_industry = ""

                        # Employment Type
                        try:
                            job_post_employment_type = job_post_right.text.split('Employment Type\n', 1)[1].split('\n')[
                                0]
                        except:
                            job_post_employment_type = ""

                        # Job Functions > maybe this is the last
                        try:
                            job_post_job_functions = job_post_right.text.split('Job Functions\n', 1)[1].split('\n')[0]
                        except:
                            job_post_job_functions = ""

                        # job info
                        job_post_info = job_post_right.text.split('\n', 5)[5]

                        # Dataframe
                        df_jobs = df_jobs.append({
                            'JOB TITLE': job_title_df,
                            'LOCATION': location,
                            'SEARCH DATETIME': now_str,
                            'Current Job Id': currentJobId,
                            'Job html': job_html,
                            'Job name': job_post_name,
                            'Company name': job_post_company_name,
                            'Company location': job_post_company_location,
                            'Posted date': job_post_posted_date,
                            'Estimated post date': job_post_estimated_date.strftime('%Y-%m-%d %H:%M'),
                            'Easy apply': job_post_easy_apply,

                            'Skills match': job_post_skills,
                            'Job Description': job_post_right_description,
                            'Seniority Level': job_post_seniority_level,
                            'Industry': job_post_industry,
                            'Employment Type': job_post_employment_type,
                            'Job Functions': job_post_job_functions,
                            'Job info': job_post_info,
                        }, ignore_index=True)

                        if i % 5 == 0:  # each 5 job post, one execution of 2 pages down
                            tabla_izq.send_keys(Keys.PAGE_DOWN * 2)
                            time.sleep(0.1)
                        count+=1
                        print(f'\rSEARCH RESULTS: {count} RESULTS')

                    except:
                        error = True  # if an error ocurred when the algorith tried to get a post, this loop finishs and goes to the next page
                    finally:
                        i += 1  # next one >>>>>>>>>>>>>>>>

        end = datetime.now()
        dif = end - now

        print(f"""\n WEB SCRAPPING FINISHED IN {dif.total_seconds()/60} MINUTES!!!
        - {df_jobs.shape[0]} job posts have been loaded""")
        #browser.close()

    except windowsclosed:
        print(f"""\n WEB SCRAPPING FINISHED IN {dif.total_seconds()/60} MINUTES!!!
        - {df_jobs.shape[0]} job posts have been loaded""")
        #browser.close()
        pass

    # LINUX
    if platform.system() == 'Linux':
        df_jobs.to_csv(f'../data/raw/df_jobs_{location}_.csv',
                       sep=';',
                       encoding='utf8',
                       index=False,
                       )
    # WINDOWS
    elif platform.system() == 'Windows':
        df_jobs.to_csv(f'..\\data\\raw\\df_jobs_{location}_.csv',
                       sep=';',
                       encoding='utf8',
                       index=False,
                       )

    return df_profile , df_jobs

def recorded_search():

    return