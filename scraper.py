import requests
from bs4 import BeautifulSoup
from time import sleep

def get_agreeance_text(ratio):
    if ratio > 3: return "absolutely agrees"
    elif 2 < ratio <= 3: return "strongly agrees"
    elif 1.5 < ratio <= 2: return "agrees"
    elif 1 < ratio <= 1.5: return "somewhat agrees"
    elif ratio == 1: return "neutral"
    elif 0.67 < ratio < 1: return "somewhat disagrees"
    elif 0.5 < ratio <= 0.67: return "disagrees"
    elif 0.33 < ratio <= 0.5: return "strongly disagrees"
    elif ratio <= 0.33: return "absolutely disagrees"
    else: return None

def find_ratio(agree, disagree):
    if (agree == 0 and disagree == 0):
        return 1
    elif(agree == 0 and disagree > 0):
        return 0
    elif (agree > 0 and disagree == 0):
        return 4
    else:
        return agree / disagree
    
def print_data_to_files(data):
    data = sorted(data, key=lambda d: d['name'])
    f = open('sorted_name.txt', 'w')
    for d in data:
        f.write(f"{d['name']}: BIAS RATING = {d['bias']}  COMMUNITY: AGREE = {d['agree']} DISAGRE = {d['disagree']} RATIO = {d['agree_ratio']} TEXT = {d['agreeance_text']}  LINK: {d['allsides_page']}\n")
    f.close()
    f = open('sorted_bias.txt', 'w')
    data = sorted(data, key=lambda d: d['bias'])
    for d in data:
        f.write(f"{d['name']}: BIAS RATING = {d['bias']}  COMMUNITY: AGREE = {d['agree']} DISAGRE = {d['disagree']} RATIO = {d['agree_ratio']} TEXT = {d['agreeance_text']}  LINK: {d['allsides_page']}\n")
    f.close()
    f = open('sorted_ratio.txt', 'w')
    data = sorted(data, key=lambda d: d['agree_ratio'], reverse=True)
    for d in data:
        f.write(f"{d['name']}: BIAS RATING = {d['bias']}  COMMUNITY: AGREE = {d['agree']} DISAGRE = {d['disagree']} RATIO = {d['agree_ratio']} TEXT = {d['agreeance_text']}  LINK: {d['allsides_page']}\n")
    f.close()
    
url = 'https://www.allsides.com/media-bias/ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B%5D=2&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&title='

r = requests.get(url)

#print(r.content[:100])

soup = BeautifulSoup(r.content, 'html.parser')

rows = soup.select('tbody tr')

data = []
for row in rows:
    d = dict()
    
    
    d['name'] = row.select_one('.source-title').text.strip()
    d['allsides_page'] = 'https://www.allsides.com' + row.select_one('.source-title a')['href']
    d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
    d['agree'] = int(row.select_one('.agree').text)
    d['disagree'] = int(row.select_one('.disagree').text)
    d['agree_ratio'] = find_ratio(d['agree'], d['disagree'])
    d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])
    
    data.append(d)



print_data_to_files(data)