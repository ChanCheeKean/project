import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime
import pickle

# path = './data/LN_Amazon_50K.pkl'
# path = './data/LN_amazon_processed_50k.pkl'
# with open(path, 'wb') as pfile:
#     pickle.dump(df, pfile, protocol=3)

# mapping = pd.read_csv('./data/index_term_mapping.csv')
# cat = pd.read_csv('./data/index_term_category.csv')
# mapping = mapping.merge(cat, on='Category', how='inner')
# mapping.to_csv('./data/index_term_mapping.csv', index=False)
# path = './data/LN_amazon_processed_50k.pkl'


# df['url_num'] = df.groupby(['duplicateGroupId', 'title'])['originalUrl'].transform('count')
# df.sort_values(['url_num', 'f_saliency'], ascending=False, inplace=True)
# df = df.head(20000)
# df.drop(columns=['url_num'], inplace=True)

# path = './data/LN_Amazon_50K.pkl'
# da = df[df.originalUrl.str.contains('metabase')].head(1000)
# df[df.licenses.str.contains('LexisNexis Licensed')]
# df[df.licenses.str.contains('LexisNexis Licensed')]

#################
### Data Task ###
#################
def get_counter(s):
    ''''Extract Frequency of all index term'''
    t = '; '.join([x for x in s])
    l = t.split('; ')
    d = dict(Counter(l))
    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
    foo = pd.DataFrame.from_dict(d, orient='index', columns=['Freq'])
    foo = foo[foo['Freq'] > 10]
    return foo[foo.index != '']

def sort_index_term(row):
    l = sorted(eval(row), key = lambda i: i['score'], reverse=True)
    return l

def extract_index_term(row, ind_type='SUB'):
    '''Extract Index Term for Subject and Industry'''
    l = [x['name'] for x in row if x['domains'] == [ind_type]]
    return l

def sigmoid(x, xmid=0, tau=0.05, top=1):
    """Sigmoid with Parameters"""
    return top / (1. + np.exp(-(x-xmid)*tau))

def fetch_data(path, start=None, end=None):
    '''Fetch Data from raw table'''
    # d1 = pd.read_csv('./data/amazon_articles_new.csv')
    # d2 = pd.read_csv('./data/amazon_articles_300k.csv')
    # d3 = pd.read_csv('./data/amazon_articles_1.csv')
    # df = pd.concat([d1, d2, d3], axis=0)    
    df = pd.read_pickle(path)
    try:
        df['publishedDate'] = pd.to_datetime(df['publishedDate']).dt.tz_convert(None)
    except:
        df['publishedDate'] = pd.to_datetime(df['publishedDate'])

    df['publishedDate'] = df['publishedDate'] + (datetime.now() - df['publishedDate'].max()) + pd.Timedelta(days=3)
    # df['publishedDate'] = df['publishedDate'] + pd.Timedelta(days=60)
    
    if start:
        df = df[(df['publishedDate'] >= start) & (df['publishedDate'] <= end)]
    else:
        pass
    return df

def process_data(df, brand):
    '''Data Filtering and Processing''' 
    mapping = pd.read_csv('./data/index_term_mapping.csv')
    
    # filtering    
    df = df.drop_duplicates(['title', 'source', 'publishedDate'])
    df = df[['duplicateGroupId', 'title', 'publishedDate', 'originalUrl', 'indexTerms', 'sentiment', 'locations', 'source']]
    df = df[df['sentiment'].str.contains(brand)]
    df = df[df['indexTerms'].str.len() > 0]
    
    # popularity
    df['coverage_rank'] = df['source'].apply(lambda x: eval(x)['metrics']['mozscape'].get('mozRank', None))
    df = df[df['coverage_rank'].notnull()]

    # topics mapping
    df['indexTerms'] = df['indexTerms'].apply(sort_index_term)
    df['Topics'] = df['indexTerms'].apply(extract_index_term)
    df = df[df['Topics'].notnull()]
    map_dict = mapping.drop_duplicates(subset=['Topics']).set_index('Topics')['Category'].to_dict()
    df['Topics'] = df['Topics'].apply(lambda x: [term for term in x if map_dict.get(term)])   
    df = df[df['Topics'].str.len() > 0]
    df['Topics'] = df['Topics'].apply(lambda x: x[0])
    df = df.merge(mapping, on='Topics', how='inner')
    
    # extract number of org mention
    df['company'] = df['sentiment'].apply(lambda row: [x for x in eval(row)['entities'] if ((x['type'] == 'Company') | (brand in x['value']))])
    df['total_org_mentions'] = df['company'].apply(lambda x: sum([int(ele['mentions']) for ele in x]))
    df['brand_mentions'] = df['company'].apply(lambda x: [int(ele['mentions']) for ele in x if brand in ele['value']][0])
    df['title_mentioned'] = [1 if brand in x else 0 for x in df['title']]
    
    # sentiment
    df['article_sentiment'] = df['sentiment'].apply(lambda x: float(eval(x)['score']))
    df['brand_sentiment'] = df['company'].apply(lambda x: [float(ele['score']) for ele in x if brand in ele['value']][0])    
    df['f_sentiment']  = [1 if x > 1 else (-1 if x < -1 else x) for x in df['brand_sentiment']]   
    
    df.drop(columns=['indexTerms', 'company', 'sentiment', 'source'], inplace=True, errors='ignore')   
    return df

def cal_trust_score(df, start, end, w0=0.8, method='additive', sal_filter=0, up_weight=1.5, senti_filter=0.05, with_rec=True, with_cov=True):
    '''Calculate trust score'''
    
    # filtering of last 7 days
    df = df[(df['publishedDate'] >= start) & (df['publishedDate'] <= end)]
    df = df[df['brand_sentiment'].abs() >= senti_filter]
    
    # saliency score
    df['f_saliency'] = (df['brand_mentions'] / df['total_org_mentions']) * np.power(up_weight, df['title_mentioned'])
    df['f_saliency'] = [1 if x > 1 else x for x in df['f_saliency']]
    
    if sal_filter > 0:
        df = df[df['f_saliency'] > sal_filter]
    
    # trust score calculation
    if method == 'additive':
        df['f_saliency'] = df['f_saliency'] * 2 - 1
        df['trust_score'] = w0 * df['f_sentiment'] + (1 - w0) * df['f_saliency']
    else:
        df['trust_score'] = df['f_saliency'] * df['f_sentiment']
        df['f_saliency'] = df['f_saliency'] * 2 - 1
    
    if with_rec:
        df['time_diff'] = (end - df['publishedDate']).dt.total_seconds() / 3600
        df['f_recency'] = sigmoid(df['time_diff'], xmid=(7 / 2 * 24), tau=.1, top=1)
        df['f_recency'] = df['f_recency'] / df['f_recency'].sum()
        df['trust_score'] =  df['trust_score'] * df['f_recency']
    
    if with_cov:
        df['coverage_rank'] = df['coverage_rank'].astype(float)
        df['url_num'] = df.groupby(['duplicateGroupId', 'title'])['originalUrl'].transform('count')        
        df.sort_values(['duplicateGroupId', 'title', 'coverage_rank'], ascending=False, inplace=True)
        df = df.groupby(['duplicateGroupId', 'title']).first().reset_index()
        df['coverage'] = df['coverage_rank'] / (10 + np.exp(-df['url_num']))
        df['trust_score'] =  df['trust_score'] * df['coverage']
        
    df['trust_score'] = df['trust_score'] * 100
    return df