[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/liakakos/drachma/blob/master/LICENSE)

# Drachma: DAML Library + Python App for Dwolla Integration

Welcome to Drachma! [Drachma](https://en.wikipedia.org/wiki/Greek_drachma) is a set of [DAML](https://daml.com/) Modules for interfacing between the [Dwolla](https://www.dwolla.com/) ACH Payment Platform and the DAML Ledger. It also includes a reference application which drives the DAML Templates. The App is implemented in Python using the rich Ledger API bindings by [dazl](https://pypi.org/project/dazl/), the [DwollaV2](https://github.com/Dwolla/dwolla-v2-python) Python client for calling the Dwolla APIs and the [Flask](http://flask.pocoo.org/) microframework for listening to Dwolla's [Webhooks](https://docs.dwolla.com/#webhook-subscriptions).

## The DAML Dwolla Library

The [DAML Dwolla Library](https://github.com/liakakos/drachma/tree/master/src/daml/Dwolla) assumes a single operator party and multiple user parties. Users send requests to the operator in order to create [Customers](#customers), attach and verify [Funding Sources](#fundingsources) and eventually issue ACH [Transfers](#transfers) between them. The library is organized in a set of modules with distinct functionality that loosely mimics the Dwolla API resources. I *strongly recommend* that you become familiar with the [Dwolla API](https://docs.dwolla.com/) before using this library. The modules are the following:

### Onboarding

The Onboarding module is used for bootstrapping the DAML Ledger. The party which assumes the operator role creates an instance of the `Operator` template and invites users by exercising the `Operator_InviteUser` choice. The `UserInvitation` contract is accepted by the user party through the `UserInvitation_Accept` choice and the `User` role contract is created. The user can now request the creation of Verified or Unverified Dwolla API Customers.

### Customers

The Customers module contains all the DAML templates necessary for the Customer creation workflows as well as the `Customer` template itself. Via the `Customer` contract, a party can exercise the `Customer_UnverifiedFundingSourceRequest` choice to create a Funding Source (which they can later verify), as well as send an ACH transfer to another customer through the `Customer_SendFunds` choice.
Currently Drachma supports the creation of an Unverified Customer (by creating an `UnverifiedCustomerRequest` contract) and that of a Personal verified Customer (`VerifiedCustomerRequest` contract). The type of information required for each customer type as well as the different state transitions of the creation workflow are dictated by the Dwolla API. You can refer to Dwolla's [Customer types](https://developers.dwolla.com/resources/account-types.html#customer-types) for more information.

### FundingSources

A Dwolla funding source is used to hold ACH bank account information. Currently Drachma supports the creation of the `bank` funding source type which can be attached to a customer resource. The Funding Sources module includes the `UnverifiedFundingSourceRequest` template which asks the operator to create and attach a `FundingSource` to the requesting customer.
Upon creation, the `FundingSource` is _unverified_ but can be verified through Dwolla's [Micro-deposit verification](https://developers.dwolla.com/resources/funding-source-verification/micro-deposit-verification.html) workflow. To execute this workflow, the user initiates two micro deposits by exercising the `FundingSource_InitiateMicroDeposits` on the `FundingSource` contract. This will instruct Dwolla to transfer two random deposits of less than $0.10 to the bank account associated with the funding source. Once the micro deposits post to the customer's bank account, the user can verify the amounts by exercising the `MicroDeposits_Verify` choice on the `MicroDeposits` contract and create a `FundingSourceVerificationRequest`. The operator will finally process the request and if the amounts match the ones posted, a `FundingSourceVerification` contract will be created and provided as proof to verify the funding source.

### Transfers

For transferring funds between customer bank accounts, the `Transfers` module is used. A user who wants to send funds exercises the non-consuming `Customer_SendFunds` choice on the `Customer` contract and creates a `ReceiveFundsRequest` addressed to the receiver party. The sender specifies the source of the funds, the amount that they want to remit and optionally any clearing instructions for their bank as well as any metadata that will be present in the transfer. The receiver party can exercise `ReceiveFundsRequest_AcceptFunds` and specify their preferred bank account that will accept the funds along with any optional receiving-side clearing instructions. This [Initiate and Accept](https://docs.daml.com/daml/patterns/initaccept.html#initiate-and-accept) DAML pattern leads to the creation of a `TransferAgreement` result contract which is subsequently validated for correct information through the `TransferAgreement_Validate` choice. Successful validation of the agreement creates a `TransferRequest` which in turn instructs the operator to call the Dwolla API and initiate a transfer. Finally a `Transfer` contract is created which holds the details of the fund transfer. This contract bears the signatures of all three parties (sender, receiver and operator) and its status gets updated by the operator via Dwolla's webhooks.

### Utils

This is a helper module specifying the various data types and statuses allowed in the Dwolla resources as well as the functions that validate them.


## Getting Started

### 1. Environment

To run Drachma, the DAML SDK must be installed on your system. Click [here](https://docs.daml.com/getting-started/installation.html) for the official installation instructions. You must also have [Python](https://www.python.org/downloads/) 3.6 or higher and [PIP](https://pypi.org/project/pip/).


### 2. Clone this repository

```
git clone git@github.com:liakakos/drachma.git
cd drachma
```

### 3. Install the required python packages

```
pip install -r src/python/requirements.txt
```

### 4. Get a Dwolla App Key and Secret

If you don't have access to the Dwolla API you can sign up [here](https://www.dwolla.com/get-started/) and use their [Sandbox](https://dashboard-sandbox.dwolla.com) environment before you decide to go to production.

### 5. Run the DAML Sandbox

For the DAML sandbox to run, you first need to compile the DAML Dwolla Library to a dar. To do this run
```
daml build -o target/daml/drachma.dar
```
from the parent drachma directory. After the dar is built, run the sandbox by issuing
```
daml sandbox target/daml/drachma.dar
```

### 6. Run the Operator App

At a minimum the Operator needs the Dwolla *App Key*, *App Secret* and the *Operator party name*. Open another terminal window and run `src/python/operator.py`. Use `--help` for more information on its configuration.

### 7. Run the Navigator

The navigator is a web app shipped with the DAML SDK. It allows you to view DAML contracts and exercise choices acting as any party you choose. On yet another terminal tab, navigate to the parent drachma directory and run:
```
daml navigator server
```
You are now ready to create the Operator role contract invite users and start using the Dwolla ACH Payment Platform!

## Disclaimer

As the [License](https://github.com/liakakos/drachma/blob/master/LICENSE#L153) states I assume no liability for any damages or losses arising from the use of this Work. Please proceed at your own risk!
