import re, sys, json, requests, html
BASE='https://abstracts.societyforscience.org/'
def search(cat='Any Category', country='', years=(), winners=True, kw=''):
    s=requests.Session(); s.headers['User-Agent']='Mozilla/5.0 (research)'
    h=s.get(BASE,timeout=30).text
    tok=re.search(r'name="__RequestVerificationToken" type="hidden" value="([^"]+)"',h).group(1)
    data=[('KeywordOrPhrase',kw),('FinalistLastName',''),('Category',cat),('FairCountry',country),('FairState','')]
    for y in years: data.append(('SelectedIsefYears',str(y)))
    data+= [('IsGetAllAbstracts','False' if winners else 'True'),('__RequestVerificationToken',tok)]
    r=s.post(BASE,data=data,timeout=60)
    return r.text
if __name__=='__main__':
    t=search(country=sys.argv[1] if len(sys.argv)>1 else '', years=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else [], winners=True, cat=sys.argv[3] if len(sys.argv)>3 else 'Any Category')
    open(sys.argv[4] if len(sys.argv)>4 else 'isef_out.html','w').write(t)
    print(len(t))
