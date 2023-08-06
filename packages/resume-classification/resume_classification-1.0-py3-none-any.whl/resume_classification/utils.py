from nltk.corpus import stopwords

keywords = ['email','phone','mobile','no','mailto','info','pin','india','profile','resume','objective','key','summary'
           ,'company','project','snapshot','kinetix', 'trading', 'solutions', 'inc', 'www', 'kinetixtt', 'com','name','mail'
            ,'linkedin', 'github', 'url','english','hindi', 'oriya', 'personal', 'details', 'father', 'marital', 'status', 'unmarried'
            ,'birthday', 'gender', 'male', 'female', 'nationality', 'indian', 'declaration','contact', 'college', 'academic',
            'qualification', 'university', 'school', 'icse', 'cbse', 'ssc', 'hsc']
stop = list(stopwords.words('english'))
stop.extend(keywords)
STOP = set(stop)

PREPROCESS_STRING = r"[\w\.\+\-]+\@[\w\.]+\w{2,3}\b|http[s]?://?(www\.)?[\w\./-_\?=]+|((\\n)|(\\xa0)|(\\u200b))+|_+|[^\w\s ]+|\d+|\b\w{1,2}\b"
SPACE_STRING = r"\s{2,}"



