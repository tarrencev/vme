from dotenv import load_dotenv
load_dotenv()

import plaid
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from flask import Flask, request, jsonify

app = Flask(__name__)

configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

@app.route("/create_link_token", methods=['POST'])
def create_link_token():
    # Get the client_user_id by searching for the current user
    # user = User.find(...)
    # client_user_id = user.id
    # Create a link_token for the given user
    request = LinkTokenCreateRequest(
            products=[Products("auth")],
            client_name="the dude",
            country_codes=[CountryCode('US')],
            redirect_uri='https://domainname.com/oauth-page.html',
            language='en',
            webhook='https://webhook.example.com',
            user=LinkTokenCreateRequestUser(
                client_user_id="dude"
            )
        )
    response = client.link_token_create(request)
    # Send the data to the client
    return jsonify(response.to_dict())

# the public token is received from Plaid Link
# exchange_request = ItemPublicTokenExchangeRequest(
#     public_token=pt_response['public_token']
# )
# exchange_response = client.item_public_token_exchange(exchange_request)
# access_token = exchange_response['access_token']
# print(access_token)

# Calculate the start and end dates for the last month
# end_date = datetime.datetime.now().date()
# start_date = (end_date - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
# end_date = end_date.strftime("%Y-%m-%d")

# request = TransactionsSyncRequest(
#     access_token=access_token,
# )
# response = client.transactions_sync(request)
# transactions = response['added']

# # the transactions in the response are paginated, so make multiple calls while incrementing the cursor to
# # retrieve all transactions
# while (response['has_more']):
#     request = TransactionsSyncRequest(
#         access_token=access_token,
#         cursor=response['next_cursor']
#     )
#     response = client.transactions_sync(request)
#     transactions += response['added']

if __name__ == "__main__":
    app.run(debug=True)