# next-merch-backend

API
endpoint
request body
return json

GET /merch
`none`
info of all merch

GET /merch
`{<merch_id>}`
info of one specific merch

GET /merch
`{<seller_id>}`
info of all merch by a seller

POST /merch
`{all fields except for id of merch db}`
create one new merch in merch database 

DELETE /merch
`{<merch_id>}`
delete merch by merch_id

GET /order
`none`
get all orders (not for using but for testing purposes)

GET /order
`{<order_id>}`
get one order by order_id

GET /order
`{<merch_id>}`
get all orders for one merch

GET /order
`{<buyer_id>}`
get all orders for one buyer

POST /order
`{all fields except for id}`
create one new order in order database, if pickedup, if payment received defaulted to be false

POST /order
`{<order_id>, <if pickedup>, <if payment received>}`
This endpoint is used by sellers to update the 2 status of order. If one or both boolean values are missing in the json body, still accept it without raising error.

DELETE /order
`{<order_id>}`
delete order by order_id

POST /user
`{<name>,<password>}`
create a new user and return the json with user_id

GET /user
`{<user_id>}`
return the user name (probably not password)

GET /user
`{<name>,<password>}`
verify if the user exists in the database

