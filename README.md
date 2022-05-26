# API-users-transactions

A simple API that allows us to register user's transactions and have an overview of how they are using their money. To do so, we want you to implement a REST API that can save users' transactions. Each transaction has: reference (unique), date, amount, type and category.

#### Example 

```json
{
  "reference": "000051",
  "date": "2020-01-13",
  "amount": "-51.13", 
  "type": "outflow",
  "category": "groceries", 
  "user_email": "janedoe@email.com"
}
```

### Constraints
  - A transaction reference is unique.
  - There are only two types of transactions: inflow and outflow.
  - All outflow transactions amounts are negative decimal numbers. 
  - All inflow transactions amounts are positive decimal numbers. 
  - We expect to receive transactions in bulk as well. 
  - The transactions we receive could be already in our system, thus we need to avoid duplicating them in our database
  
### Goals

Give the following example input:

```json
[
  {
    "reference": "000051",
    "date": "2020-01-03",
    "amount": "-51.13",
    "type": "outflow",
    "category": "groceries",
    "user_email": "janedoe@email.com"
  },
  {
    "reference": "000052",
    "date": "2020-01-10",
    "amount": "2500.72",
    "type": "inflow",
    "category": "salary",
    "user_email": "janedoe@email.com"
  },
  {
    "reference": "000053",
    "date": "2020-01-10",
    "amount": "-150.72",
    "type": "outflow",
    "category": "transfer",
    "user_email": "janedoe@email.com"
  },
  {
    "reference": "000054",
    "date": "2020-01-13",
    "amount": "-560.00",
    "type": "outflow",
    "category": "rent",
    "user_email": "janedoe@email.com"
  },
{
  "reference": "000051",
  "date": "2020-01-04",
  "amount": "-51.13",
  "type": "outflow",
  "category": "other",
  "user_email": "johndoe@email.com"
  },
  {
  "reference": "000689",
  "date": "2020-01-10",
  "amount": "150.72",
  "type": "inflow",
  "category": "savings" ,
  "user_email": "janedoe@email.com" 
  }
]
```
1. Be able to see a summary that shows the total inflow and total outflows per user

##### Example:

```json
GET /transactions?group_by=type
[ 
  { 
    "user_email": "janedoe@email.com",
    "total_inflow": "2651.44",
    "total_outflow": "-761.85" 
  },
  { 
    "user_email": "johndoe@email.com", 
    "total_inflow": "0.00", 
    "total_outflow": "-51.13"
  }
]
```


2.  Be able to see a user's summary by category that shows the sum of amounts per transaction category:

```json
GET /transactions/{user_email}/summary 
{ 
  "inflow": {
      "salary": "2500.72",
      "savings": "150.72"
  },
  "outflow": {
      "groceries": "-51.13", 
      "rent": "-560.00", 
      "transfer": "-150.72"
  }
}
```
### Expectations

- Build the app using Python 
- Provide simple and clear instructions for building and running your app
- The endpoints are just examples, feel free to change them according to your needs, we only expect you to follow the response format. 
- Optimize based on your available time, not on app performance 
- Unit tests 
- Dockerized app 
- Deliver as a private git repository, sharing with the GitHub user “belvo-hiring” when complete and indicating your GitHub user to the people team. 
- Good to haves: 
    - Django + DRF as framework
