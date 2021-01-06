import sys
import traceback

from python_graphql_client import GraphqlClient
import json

API_KEY = '5e8c22366f9c5f23ab0eff39' # This is the public key, replace with your own to access all data

client = GraphqlClient(endpoint="https://staging-api.chargetrip.io/graphql")
client.headers = {
    'x-client-id': API_KEY
}

query = """
query stationListAll ($page: Int!) {
  stationList(size: 100, page: $page) {
    id
    external_id
    country_code
    party_id
    name
    address
    city
    postal_code
    state
    country
    coordinates {
      latitude
      longitude
    }
    related_locations {
      latitude
      longitude
    }
    parking_type
    evses {
      uid
      evse_id
      status
      status_schedule {
        period_begin
        period_end
        status
      }
      capabilities
      connectors {
        id
        standard
        format
        power_type
        max_voltage
        max_amperage
        max_electric_power
        power
        tariff_ids
        terms_and_conditions
        last_updated
        properties
      }
      floor_level
      coordinates {
        latitude
        longitude
			}
      physical_reference
      parking_restrictions
      images {
        url
        thumbnail
        category
        type
        width
        height
      }
      last_updated
      parking_cost
      properties
    }
    directions  {
      language
      text
    }
    operator {
      id
      external_id
      name
      website
      logo {
        url
        thumbnail
        category
        type
        width
        height
      }
      country
      contact {
        phone
        email
        website
        facebook
        twitter
        properties
      }
    }
    suboperator {
      id
      name
    }
    owner {
      id
      name
    }
    facilities
    time_zone
    opening_times {
      twentyfourseven
      regular_hours {
        weekday
        period_begin
        period_end
      }
      exceptional_openings {
        period_begin
        period_end
      }
      exceptional_closings {
        period_begin
        period_end
      }
    }
    charging_when_closed
    images {
      url
      thumbnail
      category
      type
      width
      height
    }
    last_updated
    location {
      type
      coordinates
    }
    elevation
    chargers {
      standard
      power
      price
      speed
      status {
        free
        busy
        unknown
        error
      }
      total
    }
    physical_address {
      continent
      country
      county
      city
      street
      number
      postalCode
      what3Words
      formattedAddress
    }
    amenities
    properties
    realtime
    power
    speed
    status
    review {
      rating
      count
    }
  }
}
"""
stations = []
startPage = 0
endpage = 2000
lastPageSaved = None
lastPageFetched = None
failedPages = []
numberOfPagesFetched = 0

def attempt(variables, times=3):
    to_raise = None
    for _ in range(times):
        try:
            if _ > 1:
                print("Failed to load, starting attempt "+str(_))
            return client.execute(query=query, variables=variables)
        except Exception as err:
            to_raise = err
    raise to_raise

def fetchPage(pageNumber):
    variables = {"page": pageNumber}
    try:
        result = attempt( variables )
        global lastPageFetched
        lastPageFetched = pageNumber
        return result
    except Exception as err:
        print("An error occured while fetching page "+str(pageNumber))
        print(err)
        traceback.print_exc(file=sys.stdout)
        failedPages.append(pageNumber)
        return None

def saveResults(currentPage):
    global lastPageSaved, stations
    if(lastPageSaved == currentPage):
        return
    firstPage = lastPageSaved + 1 if lastPageSaved else startPage
    lastPage = currentPage
    with open('/home/axel/Documents/electralign-data/stations-page-' + str(firstPage) + '-' + str(lastPage) + '.json', 'w') as f:
        json.dump(stations, f)
    stations = [];
    print("Saved pages "+str(firstPage)+" until "+str(lastPage)+".")
    lastPageSaved = lastPage


for x in range(startPage, endpage+1):
    print("Fetching page "+str(x))
    data = fetchPage(x)
    if data is not None:
        stations = stations + data['data']['stationList']
    print(len(stations))

    if( len(data['data']['stationList']) < 100 ):
        break;

    numberOfPagesFetched += 1
    if(numberOfPagesFetched % 100 == 0):
        saveResults(x)

saveResults(lastPageFetched)
print("The following pages failed to load:")
print(failedPages)