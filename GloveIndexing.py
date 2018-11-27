
import simplejson as json
import timeit
import requests

start = timeit.default_timer()

# ******* Change this path according to Glove txt File *********
glovePath = "/home/ashwin/Study/NLP/glove.6B/glove.6B.100d.txt"

def update_solr_field(payload):
    # Updates a single field in a document with id 'doc_id'.
    # Updates only the 'field_update_name' field to the 'field_update_value', leaving other fields intact

    base_url = 'http://localhost:8983/'
    solr_url = 'solr/glove/'
    update_url = 'update?commit=true'
    full_url = base_url + solr_url + update_url
    headers = {'content-type': "application/json"}

    response = requests.post(full_url, data=json.dumps(payload), headers=headers)

    return response


try:
    count=0;
    unidata = []

    with open(glovePath) as corpusFile:
        for tweet in corpusFile:
            tweet=tweet.strip()
            varr=tweet.split(' ',1)
            unidata.append({"id": varr[0], "value": varr[1]})
            count+=1
            if count%10000 ==0:
                response=update_solr_field(unidata)
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    # Whoops it wasn't a 200
                    print "Error: " + str(e)
                unidata=[]
                print "{0} tweets processed...".format(count)

except Exception as e:
    print(e)

stop = timeit.default_timer()
print 'Runtime : '
print stop - start
