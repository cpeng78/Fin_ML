# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_data.ipynb.

# %% auto 0
__all__ = ['get_cv_token', 'get_cv_data', 'get_cv_data_df']

# %% ../nbs/00_data.ipynb 4
def get_cv_token(id='', secret=''):
    conn = http.client.HTTPSConnection("api.citivelocity.com")
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        "Accept": "application/json",
        }
    payload = "client_id="+id+"&client_secret="+secret+"&grant_type=client_credentials&scope=/api"
    conn.request("POST", "/markets/cv/api/oauth2/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


# %% ../nbs/00_data.ipynb 5
def get_cv_data(id, token, payload):
    conn = http.client.HTTPSConnection("api.citivelocity.com")
    token = ast.literal_eval(token)
    payload = json.dumps(payload)
    headers = {
        'authorization': "Bearer "+token['access_token'],
        'accept': "application/json",
        'content-type': "application/json"
        }
    conn.request("POST", "/markets/analytics/chartingbe/rest/external/authed/data?client_id=" + id, payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# %% ../nbs/00_data.ipynb 6
def get_cv_data_df(id, token, payload):
    data = get_cv_data(id, token, payload)
    data = ast.literal_eval(data)

    # Extract the required data from the dictionary
    indicator_data = data['body']
    indicators = list(indicator_data.keys())

    # Create a DataFrame with the required columns and index
    df = pd.DataFrame(index=indicator_data[indicators[0]]['x'])

    # Add indicator columns to the DataFrame
    for indicator in indicators:
        df[indicator] = indicator_data[indicator]['c']

    # Rename the index column to 'Date'
    df.index.name = 'Date'
    df.index = pd.to_datetime(df.index, format='%Y%m%d')

    return df

