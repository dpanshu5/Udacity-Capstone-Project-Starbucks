#Python File which contains functions which were used to prepare data for modeling


def create_offeranalysis_dataset(profile, portfolio, offer_data, transaction):
    """ Creates an analytic dataset from the following Starbucks challenge 
    datasets:

    * portfolio.json - Contains offer ids and meta data (duration, type,
                       etc.)

    * profile.json - demographic data for each customer

    * transcript.json - records for transactions, offers received, offers
                        viewed, and offers completed
                        
    INPUT:
        profile: DataFrame that contains demographic data for each 
                 customer

        portfolio: Contains offer ids and meta data (duration, type, etc.)

        offer_data: DataFrame that describes customer offer data

        transaction: DataFrame that describes customer transactions

    OUTPUT:
        clean_data: DataFrame that characterizes the effectiveness of
                    customer offers"""
    clean_data = []
    customerid_list = offer_data['customer_id'].unique()

    for idx in tqdm.tqdm(range(len(customerid_list))):

        clean_data.extend(create_combined_records(customerid_list[idx],
                                                  portfolio,
                                                  profile,
                                                  offer_data,
                                                  transaction))

    clean_data = pd.DataFrame(clean_data)

    # Initialize a list that describes the desired output DataFrame


    clean_data = clean_data.sort_values('time')
    return clean_data.reset_index(drop=True)

def create_combined_records(customer_id, portfolio, profile, offer_data, transaction):
    """ 
    Creates a list of dictionaries that describes the effectiveness of
    offers to a specific customer

    INPUT:
        customer_id: String that refers to a specific customer

        profile: DataFrame that contains demographic data for each 
                 customer
                 
        portfolio: DataFrame containing offer ids and meta data about 
                   each offer (duration, type, etc.)

        offer_data: DataFrame that describes customer offer data

        transaction: DataFrame that describes customer transactions
    
    OUTPUT:
        rows: List of dictionaries that describes the effectiveness of
              offers to a specific customer
    """
    # Select a customer's profile
    cur_customer = profile[profile['customer_id'] == customer_id]

    # Select offer data for a specific customer
    select_offer_data = offer_data['customer_id'] == customer_id
    customer_offer_data = offer_data[select_offer_data]
    customer_offer_data = customer_offer_data.drop(columns='customer_id')
    customer_offer_data = customer_offer_data.reset_index(drop=True)

    # Select transactions for a specific customer
    select_transaction = transaction['customer_id'] == customer_id
    customer_transaction_data = transaction[select_transaction]

    customer_transaction_data =\
        customer_transaction_data.drop(columns='customer_id')

    customer_transaction_data =\
        customer_transaction_data.reset_index(drop=True)

    # Initialize DataFrames that describe when a customer receives,
    # views, and completes an offer
    event_type = ['offer completed',
                  'offer received',
                  'offer viewed']

    offer_received =\
        customer_offer_data[customer_offer_data['offer received'] == 1]

    offer_received = offer_received.drop(columns=event_type)
    offer_received = offer_received.reset_index(drop=True)

    offer_viewed =\
        customer_offer_data[customer_offer_data['offer viewed'] == 1]

    offer_viewed = offer_viewed.drop(columns=event_type)
    offer_viewed = offer_viewed.reset_index(drop=True)

    offer_completed =\
        customer_offer_data[customer_offer_data['offer completed'] == 1]

    offer_completed = offer_completed.drop(columns=event_type)
    offer_completed = offer_completed.reset_index(drop=True)
    
    #print(offer_received.head())
    # Iterate over each offer a customer receives
    rows = []
    for idx in range(offer_received.shape[0]):

        # Initialize the current offer id
        cur_offer_id = offer_received.iloc[idx]['offer id']
        
        # Look-up a description of the current offer
        cur_offer = portfolio[portfolio['offer id'] == cur_offer_id]
        durationdays = cur_offer['duration'].values[0]

        # Initialize the time period when an offer is valid
        cur_offer_startime = offer_received.iloc[idx]['time_days']

        cur_offer_endtime =\
            offer_received.iloc[idx]['time_days'] + durationdays

        # Initialize a boolean array that select customer transcations that
        # fall within the valid offer time window
        select_transaction =\
            np.logical_and(customer_transaction_data['time_days'] >=
                           cur_offer_startime,
                           customer_transaction_data['time_days'] <=
                           cur_offer_endtime)

        # Initialize a boolean array that selects a description of when a
        # customer completes an offer (this array may not contain any True
        # values)
        select_offer_completed =\
            np.logical_and(offer_completed['time_days'] >= cur_offer_startime,
                           offer_completed['time_days'] <= cur_offer_endtime)

        # Initialize a boolean array that selects a description of when a
        # customer views an offer (this array may not contain any True
        # values)
        select_offer_viewed =\
            np.logical_and(offer_viewed['time_days'] >= cur_offer_startime,
                           offer_viewed['time_days'] <= cur_offer_endtime)

        # Determine whether the current offer was successful
        cur_offer_successful =\
            select_offer_completed.sum() > 0 and select_offer_viewed.sum() > 0

        # Select customer transcations that occurred within the current offer
        # valid time window
        cur_offer_transactions = customer_transaction_data[select_transaction]

        # Initialize a dictionary that describes the current customer offer
        cur_row = {'offerid': cur_offer_id,
                   'customerid': customer_id,
                   'time': cur_offer_startime,
                   'offersuccessful': int(cur_offer_successful),
                   'totalamount': cur_offer_transactions['amount'].sum()}

        cur_row.update(cur_offer.iloc[0,1:].to_dict())

        cur_row.update(cur_customer.iloc[0,1:].to_dict())

        # Update a list of dictionaries that describes the effectiveness of 
        # offers to a specific customer
        rows.append(cur_row)

    return rows
