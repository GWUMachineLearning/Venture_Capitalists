from linkedin import linkedin
import pandas as pd

#==============================================================================
# get token
#==============================================================================
API_KEY = '77ilenc46q6sa0'
API_SECRET = 'DbApo9A1zzJaMzFy'
RETURN_URL = 'https://gwmachinelearning.com/auth/callback'
token = 'AQXuICLybNeUQCLte2lfB5UkA0UwXmHcC3BsAIhZvtZNIxJzqiMBG-89QJ9rTwcz81eyzOR6wmo7pOrB5fnl6qo8Zh8Ob76e5ozfF0lvLtn7BdVdB1vNIVQKJnQHCRw2JSz_sJLumGpx27oFeVPQOjv8l79cxK0BGs8udFODHXXjKiwwd-Y'
expire = '5183999'
#authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
#print(authentication.authorization_url)  # open this url on your browser
#authentication.authorization_code = 'AQQtHwVdZnFoZcRDUgMT2RIvMUQrGgGwq6x1nOW0X3Fbfa9nlfviaEAdHU10ECfOTLfKy_FfKikRSdfZivGcrAU9shH-nzIA6Mc9qgs7FsdL1FGgelc'
#authentication.get_access_token()

#==============================================================================
# use token to get application
#==============================================================================
application = linkedin.LinkedInApplication(None,token)
application.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'distance', 'num-connections', 'skills', 'educations'])

#==============================================================================
#test for searching company 
#==============================================================================
application.search_company(selectors=[{'companies': ['name', 'employee-count-range','num-followers']}], params={'keywords': 'Benchmark Capital','count': 1})
application.search_company(selectors=[{'companies': ['name','universal-name','num-followers','industry','founded-year','employee-count-range','twitter-id']}], params={'keywords': 'Benchmark Capital', 'count': 1})

#==============================================================================
# import vc companies' data
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
industry = []
NUM_employee = []
for org in data:
    if org == '':
        univname.append('NA')
        vc_yes_or_no.append(0)
        nfollowers.append('NA')
        industry.append('NA')
        NUM_employee.append('NA')
        continue
    
    vc_check = application.search_company(selectors=[{'companies': ['universal-name','name','industry','num-followers','employee-count-range']}], params={'keywords': org})
    
    for comp in vc_check['companies']['values']:
        if 'industry' not in comp:
            continue
        elif ('industry' in comp) and (comp['industry'] == 'Venture Capital'):
            univname.append(comp['universalName'])
            vc_yes_or_no.append(1)
            nfollowers.append(comp['numFollowers'])
            industry.append(comp['industry'])
            NUM_employee.append(comp['employeeCountRange']['code'])
            break
    else:
        univname.append('NA')
        vc_yes_or_no.append(0)
        nfollowers.append('NA')
        industry.append('NA')
        NUM_employee.append('NA')
        

#==============================================================================
# find out NA in universal name
#==============================================================================
uni_NA = []
for i,j in enumerate(univname):
    if j=='NA':
        uni_NA.append(i)
data_NA = []
for i, j in enumerate(data):
    if j =='':
        data_NA.append(i)
for i in uni_NA:
    if i not in data_NA:
        print(i)

#==============================================================================
# make data frame
#==============================================================================
df1 = pd.DataFrame(data,columns = ['Company Name'],index=person)
df1['Universal Name'] = univname
df1['Number of followers'] = nfollowers
df1['Number of employees'] = NUM_employee


#==============================================================================
# export to excel
#==============================================================================
df1.to_excel('C:\\Users\\nishi\\OneDrive\\gwmachinglearning\\linkedin_data.xlsx',sheet_name = 'sheet1',index = True)
