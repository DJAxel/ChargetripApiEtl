from python_graphql_client import GraphqlClient

API_KEY = '5f8fbc2aa23e93716e7c621b'
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
variables = {"page": 1}
result = client.execute(query=query, variables=variables, verify=False)

print(result)