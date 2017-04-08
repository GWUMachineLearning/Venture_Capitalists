from linkedin import linkedin
import pandas as pd
API_KEY = '77ilenc46q6sa0'
API_SECRET = 'DbApo9A1zzJaMzFy'
RETURN_URL = 'https://gwmachinelearning.com/auth/callback'
token = 'AQXuICLybNeUQCLte2lfB5UkA0UwXmHcC3BsAIhZvtZNIxJzqiMBG-89QJ9rTwcz81eyzOR6wmo7pOrB5fnl6qo8Zh8Ob76e5ozfF0lvLtn7BdVdB1vNIVQKJnQHCRw2JSz_sJLumGpx27oFeVPQOjv8l79cxK0BGs8udFODHXXjKiwwd-Y'
expire = '5183999'

#authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
#print(authentication.authorization_url)  # open this url on your browser
application = linkedin.LinkedInApplication(None,token)

#authentication.authorization_code = 'AQQtHwVdZnFoZcRDUgMT2RIvMUQrGgGwq6x1nOW0X3Fbfa9nlfviaEAdHU10ECfOTLfKy_FfKikRSdfZivGcrAU9shH-nzIA6Mc9qgs7FsdL1FGgelc'
#authentication.get_access_token()

application.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'distance', 'num-connections', 'skills', 'educations'])
{'distance': 0,
 'firstName': 'Li Hsin',
 'id': '0nTRmPbBnB',
 'lastName': 'Chen',
 'location': {'country': {'code': 'tw'}, 'name': 'Taichung City, Taiwan'},
 'numConnections': 24}

#KEY = 'wFNJekVpDCJtRPFX812pQsJee-gt0zO4X5XmG6wcfSOSlLocxodAXNMbl0_hw3Vl'
#SECRET = 'daJDa6_8UcnGMw1yuq9TjoO_PMKukXMo8vEMo7Qv5J-G3SPgrAV0FqFCd0TNjQyG'

#from linkedin import server
#application = server.quick_api(KEY, SECRET)

application.search_profile(selectors=[{'people': ['Li Hsin', 'Chen']}])

#application.get_connections()
#application.get_connections(selectors=['headline', 'first-name', 'last-name'], params={'start':10, 'count':5})
#application.search_profile(selectors=[{'people': ['id']}], params={'keywords': 'bill gates'})
application.search_company(selectors=[{'companies': ['name', 'employee-count-range','num-followers']}], params={'keywords': 'Benchmark Capital','count': 1})
#application.get_companies(company_ids=[107745], universal_names=['apple'], selectors=['name'], params={'is-company-admin': 'true'})
#application.get_companies(company_ids=[], universal_names= 'apple', selectors = ['name'])
application.search_company(selectors=[{'companies': ['name','universal-name','num-followers','industry','founded-year','employee-count-range','twitter-id']}], params={'keywords': 'Benchmark Capital', 'count': 1})

#==============================================================================
# import data
#==============================================================================
import xlrd
file_location = "C:\\Users\\nishi\\OneDrive\\gwmachinglearning\\Crunshbase.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
sheet.cell_value(0,7)

data = [sheet.cell_value(r,7) for r in range(1,sheet.nrows)]
person = [sheet.cell_value(r,2) for r in range(1,sheet.nrows)]
#data = ['Union Square Ventures','Benchmark','']


#==============================================================================
# search companies
#==============================================================================
application.search_company(selectors=[{'companies': ['universal-name','name','industry']}], params={'keywords': 'Baseline Ventures'})
univname = []
vc_yes_or_no = []
nfollowers = []
univeralname = []
industry = []
NUM_employee = []
for org in data:
    if org == '':
        univname.append('NA')
        vc_yes_or_no.append('NA')
        nfollowers.append('NA')
        univeralname.append('NA')
        industry.append('NA')
        NUM_employee.append('NA')
        continue
    
    vc_check = application.search_company(selectors=[{'companies': ['universal-name','name','industry']}], params={'keywords': org})
    
    for comp in vc_check['companies']['values']:
        if 'industry' not in comp:
            continue
        elif ('industry' in comp) and (comp['industry'] == 'Venture Capital'):
            univname.append(comp['universalName'])
            vc_yes_or_no.append(1)
            nfollowers.append(comp['numFollowers'])
            univeralname.append(comp['universalName'])
            industry.append(comp['industry'])
            NUM_employee.append(comp['employeeCountRange']['code'])
            break
        else:
            univname.append('NA')
            vc_yes_or_no.append(0)
        


nfollowers = []
univeralname = []
industry = []
NUM_employee = []


for org in univname:
    if org == 'NA':
        nfollowers.append('NA')
        univeralname.append('NA')
        industry.append('NA')
        NUM_employee.append('NA')
        continue
    compdat = application.search_company(selectors=[{'companies': ['name','universal-name','num-followers','industry','founded-year','employee-count-range','twitter-id']}], params={'keywords': org, 'count': 1})
    nfollowers.append(compdat['companies']['values'][0]['numFollowers'])
    univeralname.append(compdat['companies']['values'][0]['universalName'])
    industry.append(compdat['companies']['values'][0]['industry'])
    NUM_employee.append(compdat['companies']['values'][0]['employeeCountRange']['code'])
    

#nfollowers = [application.search_company(selectors=[{'companies': ['num-followers']}], params={'keywords': 'Benchmark', 'count': 1})]
#print(nfollowers[0]['companies']['values'][0]['numFollowers'])

#compdat = application.search_company(selectors=[{'companies': ['num-followers']}], params={'keywords': '', 'count': 1})
#nfollowers = nfollowers.append(compdat[0]['companies']['values'][0]['numFollowers'])


pd.Series(univname)
pd.DataFrame(univname)
dat = [data,univname,nfollowers,industry,NUM_employee]
final_data = pd.DataFrame(dat,columns = ['Name','Universal Name', 'Number of followers', 'Industry', 'Number of employees'], index = person)








