import sys
import os
import datetime
import ast
from yahoo_finance import Share

import sys
import datetime
import ast
from yahoo_finance import Share

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def pull_historical_data():

    symbols = get_symbols()

    stock_list = []
    for symb in symbols:
        print symb

        if os.path.exists('data/%s.txt' %symb):
            continue

        try:
            stock_list.append(Share(symb))
            print 'Got Info'
            stock = stock_list[-1]
            hist_data= stock.get_historical('2006-02-01','2017-03-27')
            print 'Got Hist'
        except Exception as e:
            print 'Error pulling %s: %s' %(stock.symbol,e)
            continue
        outfile = 'data/%s.txt' %stock.symbol
        with open(outfile,'w') as w:
            w.write(str(hist_data))

#pull_historical_data()
def get_symbols():
    symbols=[]
    with open('SP500.txt','r') as f:
        symbols = [line.strip() for line in f]
    symbols.append('^GSPC')
    return symbols


def load_historical_data(symbols=get_symbols()):

    stock_list={}
    for symb in symbols:
        print symb
        filename = 'data/%s.txt' %symb
        try:
            with open(filename,'r') as r:
                raw = r.read() 
                hist_data = ast.literal_eval(raw)
            stock_list[symb]=hist_data
        except Exception as e:
            print 'Error pulling %s: %s' %(symb,e)
            continue

    return stock_list


def index_by_date(dt,symb = ['AMZN']):
    stock_list = load_historical_data(symb)
    stock = stock_list.get(symb[0])

    for i in range(0,len(stock)):
        tmp = datetime.datetime.strptime(stock[i]['Date'],'%Y-%m-%d')
        if tmp==dt:
            break
    return i

#{'High': '850.0', 'Symbol': 'AMZN', 
#   'Adj_Close': '846.8', 'Volume': '2754200', 
#   'Low': '833.50', 'Date': '2017-03-27', 
#   'Close': '846.82', 'Open': '838.07'}

#pull_historical_data()

##########
# stock_data = load_historical_data()

# amazon = stock_data['AMZN']
# print amazon[0]

# p = []
# time = []
# for day in amazon:
#     p.append(day['Close'])
#     time.append(day['Date'])

# x = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in time]

# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator())
# plt.plot(x,p)
# plt.gcf().autofmt_xdate()
# plt.show()

# dt = datetime.datetime.strptime('2017-03-09', '%Y-%m-%d')
# index_by_date(dt)

# #print stock_data['AMZN'][0]
##########







print '\n++++++++ GET RICH NIGGA ++++++++++\n'












# if __name__ == '__main__':


#Look at documentation about getting fresh tokens for web apps




# {'contest_mode': False, '_comments_by_id': {}, 'banned_by': None, 
# 'comment_sort': 'best', 'media_embed': {}, 
# 'subreddit': Subreddit(display_name='wallstreetbets'), 

# 'likes': None, 'suggested_sort': None, 'user_reports': [], 
# 'secure_media': None, 'link_flair_text': u'BioTrump tech', 
# 'id': u'60w2s3', 'gilded': 0, 'secure_media_embed': {}, 
# 'clicked': False, 'score': 161, 'report_reasons': None, 
# 'author': Redditor(name='hibernating_brain'), 'saved': False, 
# 'mod_reports': [], 'name': u't3_60w2s3', 'comment_limit': 2048, 
# 'subreddit_name_prefixed': u'r/wallstreetbets', 'approved_by': None, 
# 'over_18': False, 'domain': u'self.wallstreetbets', 'hidden': False,
#  'thumbnail': u'', 'subreddit_id': u't5_2th52', 'edited': 1490384142.0, 
#  'link_flair_css_class': u'biotech', 'author_flair_css_class': None, 
#  'downs': 0, 'brand_safe': False, 'archived': False, 'removal_reason': None,
#   '_reddit': <praw.reddit.Reddit object at 0x101869390>, 'is_self': True, 
#   '_mod': None, 'hide_score': False, 'spoiler': False,
#    'permalink': u'/r/wallstreetbets/comments/60w2s3/dd_and_speculation_thread_american_health_care_act/',
#     'num_reports': None, 'locked': False, 'stickied': True, 'created': 1490232861.0, 

#     'url': u'https://www.reddit.com/r/wallstreetbets/comments/60w2s3/dd_and_speculation_thread_american_health_care_act/', 
#     'author_flair_text': u'Likes Hitler dick and Masterbotting', 'quarantine': False,
#      'title': u'[DD and Speculation thread] American Health Care Act', 
#      'created_utc': 1490204061.0, 'distinguished': None, '_flair': None, 'media': None, 
# 'num_comments': 260, 'visited': False, 'subreddit_type': u'public', 'ups': 161, '_fetched': False}



