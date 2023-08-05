# Python client for Velo
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![npm version](https://badge.fury.io/py/velo-python.svg)](https://badge.fury.io/py/velo-python) [![CircleCI](https://circleci.com/gh/velopaymentsapi/velo-python.svg?style=svg)](https://circleci.com/gh/velopaymentsapi/velo-python)
This library provides a Python client that simplifies interactions with the Velo Payments API. For full details covering the API visit our docs at [Velo Payments APIs](https://apidocs.velopayments.com). Note: some of the Velo API calls which require authorization via an access token, see the full docs on how to configure.
Throughout this document and the Velo platform the following terms are used:

* **Payor.** An entity (typically a corporation) which wishes to pay funds to one or more payees via a payout.
* **Payee.** The recipient of funds paid out by a payor.
* **Payment.** A single transfer of funds from a payor to a payee.
* **Payout.** A batch of Payments, typically used by a payor to logically group payments (e.g. by business day). Technically there need be no relationship between the payments in a payout - a single payout can contain payments to multiple payees and/or multiple payments to a single payee.
* **Sandbox.** An integration environment provided by Velo Payments which offers a similar API experience to the production environment, but all funding and payment events are simulated, along with many other services such as OFAC sanctions list checking.

## Overview

The Velo Payments API allows a payor to perform a number of operations. The following is a list of the main capabilities in a natural order of execution:

* Authenticate with the Velo platform
* Maintain a collection of payees
* Query the payor’s current balance of funds within the platform and perform additional funding
* Issue payments to payees
* Query the platform for a history of those payments

This document describes the main concepts and APIs required to get up and running with the Velo Payments platform. It is not an exhaustive API reference. For that, please see the separate Velo Payments API Reference.

## API Considerations

The Velo Payments API is REST based and uses the JSON format for requests and responses.

Most calls are secured using OAuth 2 security and require a valid authentication access token for successful operation. See the Authentication section for details.

Where a dynamic value is required in the examples below, the {token} format is used, suggesting that the caller needs to supply the appropriate value of the token in question (without including the { or } characters).

Where curl examples are given, the –d @filename.json approach is used, indicating that the request body should be placed into a file named filename.json in the current directory. Each of the curl examples in this document should be considered a single line on the command-line, regardless of how they appear in print.

## Authenticating with the Velo Platform

Once Velo backoffice staff have added your organization as a payor within the Velo platform sandbox, they will create you a payor Id, an API key and an API secret and share these with you in a secure manner.

You will need to use these values to authenticate with the Velo platform in order to gain access to the APIs. The steps to take are explained in the following:

create a string comprising the API key (e.g. 44a9537d-d55d-4b47-8082-14061c2bcdd8) and API secret (e.g. c396b26b-137a-44fd-87f5-34631f8fd529) with a colon between them. E.g. 44a9537d-d55d-4b47-8082-14061c2bcdd8:c396b26b-137a-44fd-87f5-34631f8fd529

base64 encode this string. E.g.: NDRhOTUzN2QtZDU1ZC00YjQ3LTgwODItMTQwNjFjMmJjZGQ4OmMzOTZiMjZiLTEzN2EtNDRmZC04N2Y1LTM0NjMxZjhmZDUyOQ==

create an HTTP **Authorization** header with the value set to e.g. Basic NDRhOTUzN2QtZDU1ZC00YjQ3LTgwODItMTQwNjFjMmJjZGQ4OmMzOTZiMjZiLTEzN2EtNDRmZC04N2Y1LTM0NjMxZjhmZDUyOQ==

perform the Velo authentication REST call using the HTTP header created above e.g. via curl:

```
  curl -X POST \\
  -H \"Content-Type: application/json\" \\
  -H \"Authorization: Basic NDRhOTUzN2QtZDU1ZC00YjQ3LTgwODItMTQwNjFjMmJjZGQ4OmMzOTZiMjZiLTEzN2EtNDRmZC04N2Y1LTM0NjMxZjhmZDUyOQ==\" \\
  'https://api.sandbox.velopayments.com/v1/authenticate?grant_type=client_credentials'
```

If successful, this call will result in a **200** HTTP status code and a response body such as:

```
  {
    \"access_token\":\"19f6bafd-93fd-4747-b229-00507bbc991f\",
    \"token_type\":\"bearer\",
    \"expires_in\":1799,
    \"scope\":\"...\"
  }
```
## API access following authentication
Following successful authentication, the value of the access_token field in the response (indicated in green above) should then be presented with all subsequent API calls to allow the Velo platform to validate that the caller is authenticated.

This is achieved by setting the HTTP Authorization header with the value set to e.g. Bearer 19f6bafd-93fd-4747-b229-00507bbc991f such as the curl example below:

```
  -H \"Authorization: Bearer 19f6bafd-93fd-4747-b229-00507bbc991f \"
```

If you make other Velo API calls which require authorization but the Authorization header is missing or invalid then you will get a **401** HTTP status response.


This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 2.20.118
- Package version: 2.20.118
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import velo_payments
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import velo_payments
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import velo_payments
from velo_payments.rest import ApiException
from pprint import pprint


# Defining host is optional and default to https://api.sandbox.velopayments.com
configuration.host = "https://api.sandbox.velopayments.com"
# Enter a context with an instance of the API client
with velo_payments.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = velo_payments.CountriesApi(api_client)
    
    try:
        # List Supported Countries
        api_response = api_instance.list_supported_countries()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CountriesApi->list_supported_countries: %s\n" % e)
    
```

## Documentation for API Endpoints

All URIs are relative to *https://api.sandbox.velopayments.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*CountriesApi* | [**list_supported_countries**](docs/CountriesApi.md#list_supported_countries) | **GET** /v2/supportedCountries | List Supported Countries
*CountriesApi* | [**list_supported_countries_v1**](docs/CountriesApi.md#list_supported_countries_v1) | **GET** /v1/supportedCountries | List Supported Countries
*CountriesApi* | [**v1_payment_channel_rules_get**](docs/CountriesApi.md#v1_payment_channel_rules_get) | **GET** /v1/paymentChannelRules | List Payment Channel Country Rules
*CurrenciesApi* | [**list_supported_currencies**](docs/CurrenciesApi.md#list_supported_currencies) | **GET** /v2/currencies | List Supported Currencies
*FundingManagerApi* | [**create_ach_funding_request**](docs/FundingManagerApi.md#create_ach_funding_request) | **POST** /v1/sourceAccounts/{sourceAccountId}/achFundingRequest | Create Funding Request
*FundingManagerApi* | [**create_funding_request**](docs/FundingManagerApi.md#create_funding_request) | **POST** /v2/sourceAccounts/{sourceAccountId}/fundingRequest | Create Funding Request
*FundingManagerApi* | [**get_funding_account**](docs/FundingManagerApi.md#get_funding_account) | **GET** /v1/fundingAccounts/{fundingAccountId} | Get Funding Account
*FundingManagerApi* | [**get_funding_accounts**](docs/FundingManagerApi.md#get_funding_accounts) | **GET** /v1/fundingAccounts | Get Funding Accounts
*FundingManagerApi* | [**get_fundings_v1**](docs/FundingManagerApi.md#get_fundings_v1) | **GET** /v1/paymentaudit/fundings | Get Fundings for Payor
*FundingManagerApi* | [**get_source_account**](docs/FundingManagerApi.md#get_source_account) | **GET** /v1/sourceAccounts/{sourceAccountId} | Get details about given source account.
*FundingManagerApi* | [**get_source_account_v2**](docs/FundingManagerApi.md#get_source_account_v2) | **GET** /v2/sourceAccounts/{sourceAccountId} | Get details about given source account.
*FundingManagerApi* | [**get_source_accounts**](docs/FundingManagerApi.md#get_source_accounts) | **GET** /v1/sourceAccounts | Get list of source accounts
*FundingManagerApi* | [**get_source_accounts_v2**](docs/FundingManagerApi.md#get_source_accounts_v2) | **GET** /v2/sourceAccounts | Get list of source accounts
*FundingManagerApi* | [**list_funding_audit_deltas**](docs/FundingManagerApi.md#list_funding_audit_deltas) | **GET** /v1/deltas/fundings | Get Funding Audit Delta
*FundingManagerApi* | [**set_notifications_request**](docs/FundingManagerApi.md#set_notifications_request) | **POST** /v1/sourceAccounts/{sourceAccountId}/notifications | Set notifications
*FundingManagerApi* | [**transfer_funds**](docs/FundingManagerApi.md#transfer_funds) | **POST** /v2/sourceAccounts/{sourceAccountId}/transfers | Transfer Funds between source accounts
*FundingManagerPrivateApi* | [**create_funding_account**](docs/FundingManagerPrivateApi.md#create_funding_account) | **POST** /v1/fundingAccounts | Create Funding Account
*GetPayoutApi* | [**v3_payouts_payout_id_get**](docs/GetPayoutApi.md#v3_payouts_payout_id_get) | **GET** /v3/payouts/{payoutId} | Get Payout Summary
*InstructPayoutApi* | [**v3_payouts_payout_id_post**](docs/InstructPayoutApi.md#v3_payouts_payout_id_post) | **POST** /v3/payouts/{payoutId} | Instruct Payout
*LoginApi* | [**logout**](docs/LoginApi.md#logout) | **POST** /v1/logout | Logout
*LoginApi* | [**reset_password**](docs/LoginApi.md#reset_password) | **POST** /v1/password/reset | Reset password
*LoginApi* | [**validate_access_token**](docs/LoginApi.md#validate_access_token) | **POST** /v1/validate | validate
*LoginApi* | [**velo_auth**](docs/LoginApi.md#velo_auth) | **POST** /v1/authenticate | Authentication endpoint
*PayeeInvitationApi* | [**get_payees_invitation_status_v1**](docs/PayeeInvitationApi.md#get_payees_invitation_status_v1) | **GET** /v1/payees/payors/{payorId}/invitationStatus | Get Payee Invitation Status
*PayeeInvitationApi* | [**get_payees_invitation_status_v2**](docs/PayeeInvitationApi.md#get_payees_invitation_status_v2) | **GET** /v2/payees/payors/{payorId}/invitationStatus | Get Payee Invitation Status
*PayeeInvitationApi* | [**get_payees_invitation_status_v3**](docs/PayeeInvitationApi.md#get_payees_invitation_status_v3) | **GET** /v3/payees/payors/{payorId}/invitationStatus | Get Payee Invitation Status
*PayeeInvitationApi* | [**query_batch_status_v2**](docs/PayeeInvitationApi.md#query_batch_status_v2) | **GET** /v2/payees/batch/{batchId} | Query Batch Status
*PayeeInvitationApi* | [**query_batch_status_v3**](docs/PayeeInvitationApi.md#query_batch_status_v3) | **GET** /v3/payees/batch/{batchId} | Query Batch Status
*PayeeInvitationApi* | [**resend_payee_invite_v1**](docs/PayeeInvitationApi.md#resend_payee_invite_v1) | **POST** /v1/payees/{payeeId}/invite | Resend Payee Invite
*PayeeInvitationApi* | [**resend_payee_invite_v3**](docs/PayeeInvitationApi.md#resend_payee_invite_v3) | **POST** /v3/payees/{payeeId}/invite | Resend Payee Invite
*PayeeInvitationApi* | [**v2_create_payee**](docs/PayeeInvitationApi.md#v2_create_payee) | **POST** /v2/payees | Initiate Payee Creation
*PayeeInvitationApi* | [**v3_create_payee**](docs/PayeeInvitationApi.md#v3_create_payee) | **POST** /v3/payees | Initiate Payee Creation
*PayeesApi* | [**delete_payee_by_id_v1**](docs/PayeesApi.md#delete_payee_by_id_v1) | **DELETE** /v1/payees/{payeeId} | Delete Payee by Id
*PayeesApi* | [**delete_payee_by_id_v3**](docs/PayeesApi.md#delete_payee_by_id_v3) | **DELETE** /v3/payees/{payeeId} | Delete Payee by Id
*PayeesApi* | [**get_payee_by_id_v1**](docs/PayeesApi.md#get_payee_by_id_v1) | **GET** /v1/payees/{payeeId} | Get Payee by Id
*PayeesApi* | [**get_payee_by_id_v2**](docs/PayeesApi.md#get_payee_by_id_v2) | **GET** /v2/payees/{payeeId} | Get Payee by Id
*PayeesApi* | [**get_payee_by_id_v3**](docs/PayeesApi.md#get_payee_by_id_v3) | **GET** /v3/payees/{payeeId} | Get Payee by Id
*PayeesApi* | [**list_payee_changes**](docs/PayeesApi.md#list_payee_changes) | **GET** /v1/deltas/payees | List Payee Changes
*PayeesApi* | [**list_payee_changes_v3**](docs/PayeesApi.md#list_payee_changes_v3) | **GET** /v3/payees/deltas | List Payee Changes
*PayeesApi* | [**list_payees_v1**](docs/PayeesApi.md#list_payees_v1) | **GET** /v1/payees | List Payees V1
*PayeesApi* | [**list_payees_v3**](docs/PayeesApi.md#list_payees_v3) | **GET** /v3/payees | List Payees
*PayeesApi* | [**v1_payees_payee_id_remote_id_update_post**](docs/PayeesApi.md#v1_payees_payee_id_remote_id_update_post) | **POST** /v1/payees/{payeeId}/remoteIdUpdate | Update Payee Remote Id
*PayeesApi* | [**v3_payees_payee_id_remote_id_update_post**](docs/PayeesApi.md#v3_payees_payee_id_remote_id_update_post) | **POST** /v3/payees/{payeeId}/remoteIdUpdate | Update Payee Remote Id
*PaymentAuditServiceApi* | [**export_transactions_csvv3**](docs/PaymentAuditServiceApi.md#export_transactions_csvv3) | **GET** /v3/paymentaudit/transactions | Export Transactions
*PaymentAuditServiceApi* | [**export_transactions_csvv4**](docs/PaymentAuditServiceApi.md#export_transactions_csvv4) | **GET** /v4/paymentaudit/transactions | Export Transactions
*PaymentAuditServiceApi* | [**get_fundings_v1**](docs/PaymentAuditServiceApi.md#get_fundings_v1) | **GET** /v1/paymentaudit/fundings | Get Fundings for Payor
*PaymentAuditServiceApi* | [**get_payment_details**](docs/PaymentAuditServiceApi.md#get_payment_details) | **GET** /v3/paymentaudit/payments/{paymentId} | Get Payment
*PaymentAuditServiceApi* | [**get_payment_details_v4**](docs/PaymentAuditServiceApi.md#get_payment_details_v4) | **GET** /v4/paymentaudit/payments/{paymentId} | Get Payment
*PaymentAuditServiceApi* | [**get_payments_for_payout**](docs/PaymentAuditServiceApi.md#get_payments_for_payout) | **GET** /v3/paymentaudit/payouts/{payoutId} | Get Payments for Payout
*PaymentAuditServiceApi* | [**get_payments_for_payout_v4**](docs/PaymentAuditServiceApi.md#get_payments_for_payout_v4) | **GET** /v4/paymentaudit/payouts/{payoutId} | Get Payments for Payout
*PaymentAuditServiceApi* | [**get_payouts_for_payor_v3**](docs/PaymentAuditServiceApi.md#get_payouts_for_payor_v3) | **GET** /v3/paymentaudit/payouts | Get Payouts for Payor
*PaymentAuditServiceApi* | [**get_payouts_for_payor_v4**](docs/PaymentAuditServiceApi.md#get_payouts_for_payor_v4) | **GET** /v4/paymentaudit/payouts | Get Payouts for Payor
*PaymentAuditServiceApi* | [**list_payment_changes**](docs/PaymentAuditServiceApi.md#list_payment_changes) | **GET** /v1/deltas/payments | List Payment Changes
*PaymentAuditServiceApi* | [**list_payments_audit**](docs/PaymentAuditServiceApi.md#list_payments_audit) | **GET** /v3/paymentaudit/payments | Get List of Payments
*PaymentAuditServiceApi* | [**list_payments_audit_v4**](docs/PaymentAuditServiceApi.md#list_payments_audit_v4) | **GET** /v4/paymentaudit/payments | Get List of Payments
*PayorsApi* | [**get_payor_by_id**](docs/PayorsApi.md#get_payor_by_id) | **GET** /v1/payors/{payorId} | Get Payor
*PayorsApi* | [**get_payor_by_id_v2**](docs/PayorsApi.md#get_payor_by_id_v2) | **GET** /v2/payors/{payorId} | Get Payor
*PayorsApi* | [**payor_add_payor_logo**](docs/PayorsApi.md#payor_add_payor_logo) | **POST** /v1/payors/{payorId}/branding/logos | Add Logo
*PayorsApi* | [**payor_create_api_key_request**](docs/PayorsApi.md#payor_create_api_key_request) | **POST** /v1/payors/{payorId}/applications/{applicationId}/keys | Create API Key
*PayorsApi* | [**payor_create_application_request**](docs/PayorsApi.md#payor_create_application_request) | **POST** /v1/payors/{payorId}/applications | Create Application
*PayorsApi* | [**payor_email_opt_out**](docs/PayorsApi.md#payor_email_opt_out) | **POST** /v1/payors/{payorId}/reminderEmailsUpdate | Reminder Email Opt-Out
*PayorsApi* | [**payor_get_branding**](docs/PayorsApi.md#payor_get_branding) | **GET** /v1/payors/{payorId}/branding | Get Branding
*PayorsApi* | [**payor_links**](docs/PayorsApi.md#payor_links) | **GET** /v1/payorLinks | List Payor Links
*PayorsPrivateApi* | [**create_payor_links**](docs/PayorsPrivateApi.md#create_payor_links) | **POST** /v1/payorLinks | Create a Payor Link
*PayoutHistoryApi* | [**get_payments_for_payout**](docs/PayoutHistoryApi.md#get_payments_for_payout) | **GET** /v3/paymentaudit/payouts/{payoutId} | Get Payments for Payout
*PayoutHistoryApi* | [**get_payments_for_payout_v4**](docs/PayoutHistoryApi.md#get_payments_for_payout_v4) | **GET** /v4/paymentaudit/payouts/{payoutId} | Get Payments for Payout
*PayoutHistoryApi* | [**get_payout_stats_v1**](docs/PayoutHistoryApi.md#get_payout_stats_v1) | **GET** /v1/paymentaudit/payoutStatistics | Get Payout Statistics
*QuotePayoutApi* | [**v3_payouts_payout_id_quote_post**](docs/QuotePayoutApi.md#v3_payouts_payout_id_quote_post) | **POST** /v3/payouts/{payoutId}/quote | Create a quote for the payout
*SubmitPayoutApi* | [**submit_payout**](docs/SubmitPayoutApi.md#submit_payout) | **POST** /v3/payouts | Submit Payout
*TokensApi* | [**resend_token**](docs/TokensApi.md#resend_token) | **POST** /v2/users/{userId}/tokens | Resend a token
*UsersApi* | [**delete_user_by_id_v2**](docs/UsersApi.md#delete_user_by_id_v2) | **DELETE** /v2/users/{userId} | Delete a User
*UsersApi* | [**disable_user_v2**](docs/UsersApi.md#disable_user_v2) | **POST** /v2/users/{userId}/disable | Disable a User
*UsersApi* | [**enable_user_v2**](docs/UsersApi.md#enable_user_v2) | **POST** /v2/users/{userId}/enable | Enable a User
*UsersApi* | [**get_self**](docs/UsersApi.md#get_self) | **GET** /v2/users/self | Get Self
*UsersApi* | [**get_user_by_id_v2**](docs/UsersApi.md#get_user_by_id_v2) | **GET** /v2/users/{userId} | Get User
*UsersApi* | [**invite_user**](docs/UsersApi.md#invite_user) | **POST** /v2/users/invite | Invite a User
*UsersApi* | [**list_users**](docs/UsersApi.md#list_users) | **GET** /v2/users | List Users
*UsersApi* | [**register_sms**](docs/UsersApi.md#register_sms) | **POST** /v2/users/registration/sms | Register SMS Number
*UsersApi* | [**resend_token**](docs/UsersApi.md#resend_token) | **POST** /v2/users/{userId}/tokens | Resend a token
*UsersApi* | [**role_update**](docs/UsersApi.md#role_update) | **POST** /v2/users/{userId}/roleUpdate | Update User Role
*UsersApi* | [**unlock_user_v2**](docs/UsersApi.md#unlock_user_v2) | **POST** /v2/users/{userId}/unlock | Unlock a User
*UsersApi* | [**unregister_mfa**](docs/UsersApi.md#unregister_mfa) | **POST** /v2/users/{userId}/mfa/unregister | Unregister MFA for the user
*UsersApi* | [**unregister_mfa_for_self**](docs/UsersApi.md#unregister_mfa_for_self) | **POST** /v2/users/self/mfa/unregister | Unregister MFA for Self
*UsersApi* | [**update_password_self**](docs/UsersApi.md#update_password_self) | **POST** /v2/users/self/password | Update Password for self
*UsersApi* | [**user_details_update**](docs/UsersApi.md#user_details_update) | **POST** /v2/users/{userId}/userDetailsUpdate | Update User Details
*UsersApi* | [**validate_password_self**](docs/UsersApi.md#validate_password_self) | **POST** /v2/users/self/password/validate | Validate the proposed password
*WithdrawPayoutApi* | [**v3_payouts_payout_id_delete**](docs/WithdrawPayoutApi.md#v3_payouts_payout_id_delete) | **DELETE** /v3/payouts/{payoutId} | Withdraw Payout


## Documentation For Models

 - [AcceptedPayment](docs/AcceptedPayment.md)
 - [AccessTokenResponse](docs/AccessTokenResponse.md)
 - [AccessTokenValidationRequest](docs/AccessTokenValidationRequest.md)
 - [AuthResponse](docs/AuthResponse.md)
 - [AutoTopUpConfig](docs/AutoTopUpConfig.md)
 - [Challenge](docs/Challenge.md)
 - [Company](docs/Company.md)
 - [Company2](docs/Company2.md)
 - [CompanyResponse](docs/CompanyResponse.md)
 - [CompanyV1](docs/CompanyV1.md)
 - [CreateFundingAccountRequest](docs/CreateFundingAccountRequest.md)
 - [CreateIndividual](docs/CreateIndividual.md)
 - [CreateIndividual2](docs/CreateIndividual2.md)
 - [CreateIndividual2Name](docs/CreateIndividual2Name.md)
 - [CreatePayee](docs/CreatePayee.md)
 - [CreatePayee2](docs/CreatePayee2.md)
 - [CreatePayeeAddress](docs/CreatePayeeAddress.md)
 - [CreatePayeeAddress2](docs/CreatePayeeAddress2.md)
 - [CreatePayeesCSVRequest](docs/CreatePayeesCSVRequest.md)
 - [CreatePayeesCSVRequest2](docs/CreatePayeesCSVRequest2.md)
 - [CreatePayeesCSVResponse](docs/CreatePayeesCSVResponse.md)
 - [CreatePayeesCSVResponse2](docs/CreatePayeesCSVResponse2.md)
 - [CreatePayeesCSVResponseRejectedCsvRows](docs/CreatePayeesCSVResponseRejectedCsvRows.md)
 - [CreatePayeesRequest](docs/CreatePayeesRequest.md)
 - [CreatePayeesRequest2](docs/CreatePayeesRequest2.md)
 - [CreatePaymentChannel](docs/CreatePaymentChannel.md)
 - [CreatePaymentChannel2](docs/CreatePaymentChannel2.md)
 - [CreatePayorLinkRequest](docs/CreatePayorLinkRequest.md)
 - [CreatePayoutRequest](docs/CreatePayoutRequest.md)
 - [CurrencyType](docs/CurrencyType.md)
 - [Error](docs/Error.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [FailedSubmission](docs/FailedSubmission.md)
 - [FailedSubmission2](docs/FailedSubmission2.md)
 - [FundingAccountResponse](docs/FundingAccountResponse.md)
 - [FundingAudit](docs/FundingAudit.md)
 - [FundingEvent](docs/FundingEvent.md)
 - [FundingEventType](docs/FundingEventType.md)
 - [FundingPayorStatusAuditResponse](docs/FundingPayorStatusAuditResponse.md)
 - [FundingRequestV1](docs/FundingRequestV1.md)
 - [FundingRequestV2](docs/FundingRequestV2.md)
 - [FxSummaryV3](docs/FxSummaryV3.md)
 - [FxSummaryV4](docs/FxSummaryV4.md)
 - [GetFundingsResponse](docs/GetFundingsResponse.md)
 - [GetFundingsResponseAllOf](docs/GetFundingsResponseAllOf.md)
 - [GetPaymentsForPayoutResponseV3](docs/GetPaymentsForPayoutResponseV3.md)
 - [GetPaymentsForPayoutResponseV3Page](docs/GetPaymentsForPayoutResponseV3Page.md)
 - [GetPaymentsForPayoutResponseV3Summary](docs/GetPaymentsForPayoutResponseV3Summary.md)
 - [GetPaymentsForPayoutResponseV4](docs/GetPaymentsForPayoutResponseV4.md)
 - [GetPaymentsForPayoutResponseV4Summary](docs/GetPaymentsForPayoutResponseV4Summary.md)
 - [GetPayoutStatistics](docs/GetPayoutStatistics.md)
 - [GetPayoutsResponseV3](docs/GetPayoutsResponseV3.md)
 - [GetPayoutsResponseV3Links](docs/GetPayoutsResponseV3Links.md)
 - [GetPayoutsResponseV3Page](docs/GetPayoutsResponseV3Page.md)
 - [GetPayoutsResponseV4](docs/GetPayoutsResponseV4.md)
 - [Individual](docs/Individual.md)
 - [Individual2](docs/Individual2.md)
 - [IndividualResponse](docs/IndividualResponse.md)
 - [IndividualV1](docs/IndividualV1.md)
 - [IndividualV1Name](docs/IndividualV1Name.md)
 - [InlineResponse400](docs/InlineResponse400.md)
 - [InlineResponse400Errors](docs/InlineResponse400Errors.md)
 - [InlineResponse401](docs/InlineResponse401.md)
 - [InlineResponse401Errors](docs/InlineResponse401Errors.md)
 - [InlineResponse403](docs/InlineResponse403.md)
 - [InlineResponse403Errors](docs/InlineResponse403Errors.md)
 - [InlineResponse409](docs/InlineResponse409.md)
 - [InlineResponse409Errors](docs/InlineResponse409Errors.md)
 - [InvitationStatus](docs/InvitationStatus.md)
 - [InvitationStatusResponse](docs/InvitationStatusResponse.md)
 - [InvitePayeeRequest](docs/InvitePayeeRequest.md)
 - [InvitePayeeRequest2](docs/InvitePayeeRequest2.md)
 - [InviteUserRequest](docs/InviteUserRequest.md)
 - [KycState](docs/KycState.md)
 - [Language](docs/Language.md)
 - [Language2](docs/Language2.md)
 - [LinkForResponse](docs/LinkForResponse.md)
 - [ListFundingAccountsResponse](docs/ListFundingAccountsResponse.md)
 - [ListPaymentsResponse](docs/ListPaymentsResponse.md)
 - [ListPaymentsResponsePage](docs/ListPaymentsResponsePage.md)
 - [ListPaymentsResponseV4](docs/ListPaymentsResponseV4.md)
 - [ListSourceAccountResponse](docs/ListSourceAccountResponse.md)
 - [ListSourceAccountResponseLinks](docs/ListSourceAccountResponseLinks.md)
 - [ListSourceAccountResponsePage](docs/ListSourceAccountResponsePage.md)
 - [ListSourceAccountResponseV2](docs/ListSourceAccountResponseV2.md)
 - [LocationType](docs/LocationType.md)
 - [MFADetails](docs/MFADetails.md)
 - [MFAType](docs/MFAType.md)
 - [MarketingOptIn](docs/MarketingOptIn.md)
 - [Notifications](docs/Notifications.md)
 - [OfacStatus](docs/OfacStatus.md)
 - [OfacStatus2](docs/OfacStatus2.md)
 - [OnboardedStatus](docs/OnboardedStatus.md)
 - [OnboardedStatus2](docs/OnboardedStatus2.md)
 - [PageForResponse](docs/PageForResponse.md)
 - [PageResourceFundingPayorStatusAuditResponseFundingPayorStatusAuditResponse](docs/PageResourceFundingPayorStatusAuditResponseFundingPayorStatusAuditResponse.md)
 - [PagedPayeeInvitationStatusResponse](docs/PagedPayeeInvitationStatusResponse.md)
 - [PagedPayeeInvitationStatusResponse2](docs/PagedPayeeInvitationStatusResponse2.md)
 - [PagedPayeeInvitationStatusResponsePage](docs/PagedPayeeInvitationStatusResponsePage.md)
 - [PagedPayeeResponse](docs/PagedPayeeResponse.md)
 - [PagedPayeeResponse2](docs/PagedPayeeResponse2.md)
 - [PagedPayeeResponse2Summary](docs/PagedPayeeResponse2Summary.md)
 - [PagedPayeeResponseLinks](docs/PagedPayeeResponseLinks.md)
 - [PagedPayeeResponsePage](docs/PagedPayeeResponsePage.md)
 - [PagedPayeeResponseSummary](docs/PagedPayeeResponseSummary.md)
 - [PagedResponse](docs/PagedResponse.md)
 - [PagedResponsePage](docs/PagedResponsePage.md)
 - [PagedUserResponse](docs/PagedUserResponse.md)
 - [PagedUserResponseLinks](docs/PagedUserResponseLinks.md)
 - [PagedUserResponsePage](docs/PagedUserResponsePage.md)
 - [PasswordRequest](docs/PasswordRequest.md)
 - [Payee](docs/Payee.md)
 - [Payee2](docs/Payee2.md)
 - [PayeeAddress](docs/PayeeAddress.md)
 - [PayeeAddress2](docs/PayeeAddress2.md)
 - [PayeeDelta](docs/PayeeDelta.md)
 - [PayeeDelta2](docs/PayeeDelta2.md)
 - [PayeeDeltaResponse](docs/PayeeDeltaResponse.md)
 - [PayeeDeltaResponse2](docs/PayeeDeltaResponse2.md)
 - [PayeeDeltaResponse2Links](docs/PayeeDeltaResponse2Links.md)
 - [PayeeDeltaResponseLinks](docs/PayeeDeltaResponseLinks.md)
 - [PayeeDeltaResponsePage](docs/PayeeDeltaResponsePage.md)
 - [PayeeInvitationStatus](docs/PayeeInvitationStatus.md)
 - [PayeeInvitationStatusResponse](docs/PayeeInvitationStatusResponse.md)
 - [PayeeInvitationStatusResponse2](docs/PayeeInvitationStatusResponse2.md)
 - [PayeePaymentChannel](docs/PayeePaymentChannel.md)
 - [PayeePaymentChannel2](docs/PayeePaymentChannel2.md)
 - [PayeePayorRef](docs/PayeePayorRef.md)
 - [PayeePayorRefV2](docs/PayeePayorRefV2.md)
 - [PayeePayorRefV3](docs/PayeePayorRefV3.md)
 - [PayeeResponse](docs/PayeeResponse.md)
 - [PayeeResponse2](docs/PayeeResponse2.md)
 - [PayeeResponseV2](docs/PayeeResponseV2.md)
 - [PayeeResponseV3](docs/PayeeResponseV3.md)
 - [PayeeType](docs/PayeeType.md)
 - [PaymentAuditCurrencyV3](docs/PaymentAuditCurrencyV3.md)
 - [PaymentAuditCurrencyV4](docs/PaymentAuditCurrencyV4.md)
 - [PaymentChannelCountry](docs/PaymentChannelCountry.md)
 - [PaymentChannelRule](docs/PaymentChannelRule.md)
 - [PaymentChannelRulesResponse](docs/PaymentChannelRulesResponse.md)
 - [PaymentDelta](docs/PaymentDelta.md)
 - [PaymentDeltaResponse](docs/PaymentDeltaResponse.md)
 - [PaymentEventResponseV3](docs/PaymentEventResponseV3.md)
 - [PaymentEventResponseV4](docs/PaymentEventResponseV4.md)
 - [PaymentInstruction](docs/PaymentInstruction.md)
 - [PaymentRails](docs/PaymentRails.md)
 - [PaymentResponseV3](docs/PaymentResponseV3.md)
 - [PaymentResponseV4](docs/PaymentResponseV4.md)
 - [PaymentResponseV4Payout](docs/PaymentResponseV4Payout.md)
 - [PayorAddress](docs/PayorAddress.md)
 - [PayorAddressV2](docs/PayorAddressV2.md)
 - [PayorAmlTransactionV3](docs/PayorAmlTransactionV3.md)
 - [PayorAmlTransactionV4](docs/PayorAmlTransactionV4.md)
 - [PayorBrandingResponse](docs/PayorBrandingResponse.md)
 - [PayorCreateApiKeyRequest](docs/PayorCreateApiKeyRequest.md)
 - [PayorCreateApiKeyResponse](docs/PayorCreateApiKeyResponse.md)
 - [PayorCreateApplicationRequest](docs/PayorCreateApplicationRequest.md)
 - [PayorEmailOptOutRequest](docs/PayorEmailOptOutRequest.md)
 - [PayorLinksResponse](docs/PayorLinksResponse.md)
 - [PayorLinksResponseLinks](docs/PayorLinksResponseLinks.md)
 - [PayorLinksResponsePayors](docs/PayorLinksResponsePayors.md)
 - [PayorLogoRequest](docs/PayorLogoRequest.md)
 - [PayorV1](docs/PayorV1.md)
 - [PayorV2](docs/PayorV2.md)
 - [PayoutPayorV4](docs/PayoutPayorV4.md)
 - [PayoutPrincipalV4](docs/PayoutPrincipalV4.md)
 - [PayoutStatusV3](docs/PayoutStatusV3.md)
 - [PayoutStatusV4](docs/PayoutStatusV4.md)
 - [PayoutSummaryAuditV3](docs/PayoutSummaryAuditV3.md)
 - [PayoutSummaryAuditV4](docs/PayoutSummaryAuditV4.md)
 - [PayoutSummaryResponse](docs/PayoutSummaryResponse.md)
 - [PayoutTypeV4](docs/PayoutTypeV4.md)
 - [QueryBatchResponse](docs/QueryBatchResponse.md)
 - [QueryBatchResponse2](docs/QueryBatchResponse2.md)
 - [QuoteFxSummary](docs/QuoteFxSummary.md)
 - [QuoteResponse](docs/QuoteResponse.md)
 - [Region](docs/Region.md)
 - [RegisterSmsRequest](docs/RegisterSmsRequest.md)
 - [RejectedPayment](docs/RejectedPayment.md)
 - [ResendTokenRequest](docs/ResendTokenRequest.md)
 - [ResetPasswordRequest](docs/ResetPasswordRequest.md)
 - [Role](docs/Role.md)
 - [RoleUpdateRequest](docs/RoleUpdateRequest.md)
 - [SelfMFATypeUnregisterRequest](docs/SelfMFATypeUnregisterRequest.md)
 - [SelfUpdatePasswordRequest](docs/SelfUpdatePasswordRequest.md)
 - [SetNotificationsRequest](docs/SetNotificationsRequest.md)
 - [SourceAccount](docs/SourceAccount.md)
 - [SourceAccountResponse](docs/SourceAccountResponse.md)
 - [SourceAccountResponseV2](docs/SourceAccountResponseV2.md)
 - [SourceAccountSummaryV3](docs/SourceAccountSummaryV3.md)
 - [SourceAccountSummaryV4](docs/SourceAccountSummaryV4.md)
 - [SupportedCountriesResponse](docs/SupportedCountriesResponse.md)
 - [SupportedCountriesResponse2](docs/SupportedCountriesResponse2.md)
 - [SupportedCountry](docs/SupportedCountry.md)
 - [SupportedCountry2](docs/SupportedCountry2.md)
 - [SupportedCurrency](docs/SupportedCurrency.md)
 - [SupportedCurrencyResponse](docs/SupportedCurrencyResponse.md)
 - [TransferRequest](docs/TransferRequest.md)
 - [UnregisterMFARequest](docs/UnregisterMFARequest.md)
 - [UpdateRemoteIdRequest](docs/UpdateRemoteIdRequest.md)
 - [UserDetailsUpdateRequest](docs/UserDetailsUpdateRequest.md)
 - [UserInfo](docs/UserInfo.md)
 - [UserResponse](docs/UserResponse.md)
 - [UserResponse2](docs/UserResponse2.md)
 - [UserResponse2Roles](docs/UserResponse2Roles.md)
 - [UserStatus](docs/UserStatus.md)
 - [UserType](docs/UserType.md)
 - [UserType2](docs/UserType2.md)
 - [ValidatePasswordResponse](docs/ValidatePasswordResponse.md)
 - [WatchlistStatus](docs/WatchlistStatus.md)


## Documentation For Authorization


## OAuth2

- **Type**: OAuth
- **Flow**: application
- **Authorization URL**: 
- **Scopes**: 
 - ** **: Scopes not required


## basicAuth

- **Type**: HTTP basic authentication


## oAuthVeloBackOffice

- **Type**: OAuth
- **Flow**: application
- **Authorization URL**: 
- **Scopes**: 
 - ** **: Scopes not required


## Author




