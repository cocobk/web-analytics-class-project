import csv
import re
import json
import requests
import time


# Theses are the headers we have identified as required for each API call
headers = {
    'X-Airbnb-GraphQL-Platform': 'web',
    'X-Airbnb-API-Key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    'X-Airbnb-GraphQL-Platform-Client': 'apollo-niobe'
}

def formatPdpReviewsVariables(listingId, limit, offset):
     return {
        'request': {
            'listingId': listingId, # Listing ID, check browsers address bar, ex: https://www.airbnb.com/rooms/205043
            'limit': limit,
            'offset': offset
        }
    }
    
with open('data/listings.tsv', newline = '', encoding = 'utf-8') as listingsFile:
    listingsReader = csv.DictReader(listingsFile, delimiter = '\t')
    
    with open('data/reviews.tsv', mode = 'w', encoding = 'utf-8') as reviewsFile:
        reviewsFile.write('ID\tQuery\tReview\n')
    
        # API URL we use to get review details
        reviewsUrl = 'https://www.airbnb.com/api/v3/PdpReviews';
    
        for listing in listingsReader:
    
            variables = formatPdpReviewsVariables(listing['ID'], 100, 0)
    
            extensions = {
                'persistedQuery': {
                'version': 1,
                'sha256Hash': 'a6ecae1e52d14869af66a3a1214bb44397c6f8788e308bea63a503fd32000fc4'
                }
            }

            # Query parameters that we need to send to API. variables and extensions dictionaries need to be sent as strings
            params = {
                'operationName': 'PdpReviews',
                'locale': 'en',
                'currency': 'USD',
                'variables': json.dumps(variables, ensure_ascii=False),
                'extensions': json.dumps(extensions, ensure_ascii=False)
            }

            # We use the request library to call the API. We use the "get" method here.
            response = requests.get(reviewsUrl, params = params, headers = headers)

            responseContent = json.loads(response.text)

            reviews = responseContent['data']['merlin']['pdpReviews']['reviews']

            for review in reviews:
                comment = re.sub('[\n]*', '', review['comments']);
                reviewsFile.write(listing['ID'] + '\t' + listing['Query'] + '\t' + comment + '\n')
                
            print('Finished Reviews for: ', listing['ID'], listing['Query'])
            time.sleep(2)

print('Done Reviews')