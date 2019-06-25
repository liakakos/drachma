import constants as const

import argparse
import datetime
import dazl
import dwollav2
import logging


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dwolla Operator")
    parser.add_argument('dwolla_app_key', type=str, help="Dwolla App Key")
    parser.add_argument('dwolla_app_secret', type=str, help="Dwolla App Secret")
    parser.add_argument('operator', type=str, help="Operator Name")
    parser.add_argument('-e', '--dwolla_env', type=str, choices=['production', 'sandbox'],
                        help="Dwolla Environment", default='production')
    parser.add_argument('-l', '--ledger_host', type=str, help="Ledger Host URL", default='localhost')
    parser.add_argument('-p', '--ledger_port', type=int, help="Ledger Port", default=6865)

    args = parser.parse_args()

    network = dazl.Network()
    network.set_config(url=f'http://{args.ledger_host}:{args.ledger_port}')

    operator = network.simple_party(args.operator)

    client = dwollav2.Client(key=args.dwolla_app_key,
                             secret=args.dwolla_app_secret,
                             environment=args.dwolla_env)

    dwolla_hostname = client.api_url
    app_token = client.Auth.client()

    LOG = logging.getLogger('Dwolla Operator')


    @operator.ledger_created(const.T_UNVERIFIED_CUSTOMER_REQUEST)
    def on_unverified_customer_request(event):
        cdata = event.cdata
        request_body = {
            'firstName': cdata['firstName'],
            'lastName': cdata['lastName'],
            'email': cdata['email'],
            'ipAddress': cdata['ipAddress']
        }

        new_customer_resp = app_token.post('customers', request_body)
        LOG.debug(f"new_customer_resp status: {new_customer_resp.status}, "
                  f"headers: {new_customer_resp.headers}, "
                  f"body: {new_customer_resp.body}")

        if new_customer_resp.status >= 400:
            return

        customer_resp = app_token.get(new_customer_resp.headers['location'])
        LOG.debug(f"customer status: {customer_resp.status}, "
                  f"headers: {customer_resp.headers}, "
                  f"body: {customer_resp.body}")

        customer = customer_resp.body

        return dazl.exercise(event.cid, const.C_UNVERIFIED_CUSTOMER_REQUEST_ACCEPT, {
            'customerId': customer['id'],
            'created': datetime.datetime.strptime(customer['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'status': customer['status']
        })


    @operator.ledger_created(const.VERIFIED_CUSTOMER_REQUEST)
    def on_verified_customer_request(event):
        cdata = event.cdata
        request_body = {
            'firstName': cdata['firstName'],
            'lastName': cdata['lastName'],
            'email': cdata['email'],
            'type': 'personal',
            'address1': cdata['address1'],
            'address2': '',  # address2
            'city': cdata['city'],
            'state': cdata['state'],
            'postalCode': cdata['postalCode'],
            'dateOfBirth': cdata['dateOfBirth'],
            'ssn': cdata['ssn']
        }

        new_customer_resp = app_token.post('customers', request_body)
        LOG.debug(f"new_customer_resp status: {new_customer_resp.status}, "
                  f"headers: {new_customer_resp.headers}, "
                  f"body: {new_customer_resp.body}")

        if new_customer_resp.status >= 400:
            return

        customer_resp = app_token.get(new_customer_resp.headers['location'])
        LOG.debug(f"customer status: {customer_resp.status}, "
                  f"headers: {customer_resp.headers}, "
                  f"body: {customer_resp.body}")

        customer = customer_resp.body

        return dazl.exercise(event.cid, const.C_VERIFIED_CUSTOMER_REQUEST_ACCEPT, {
            'customerId': customer['id'],
            'created':datetime.datetime.strptime(customer['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'status': customer['status']
        })


    @operator.ledger_created(const.UNVERIFIED_FUNDING_SOURCE_REQUEST)
    def on_unverified_funding_source_request(event):
        cdata = event.cdata
        request_body = {
            'routingNumber': cdata['routingNumber'],
            'accountNumber': cdata['accountNumber'],
            'bankAccountType': cdata['bankAccountType'],
            'name': cdata['name']
        }

        customer_url = f"{dwolla_hostname}/customers/{cdata['customerId']}"
        new_funding_source_resp = app_token.post(f"{customer_url}/funding-sources", request_body)
        LOG.debug(f"new_funding_source_resp status: {new_funding_source_resp.status}, "
                  f"headers: {new_funding_source_resp.headers}, "
                  f"body: {new_funding_source_resp.body}")

        if new_funding_source_resp.status >= 400:
            return

        funding_source_resp = app_token.get(new_funding_source_resp.headers['location'])
        LOG.debug(f"funding_source_resp status: {funding_source_resp.status}, "
                  f"headers: {funding_source_resp.headers}, "
                  f"body: {funding_source_resp.body}")

        funding_source = funding_source_resp.body

        return dazl.exercise(event.cid, const.C_UNVERIFIED_FUNDING_SOURCE_REQUEST_ACCEPT, {
            'fundingSourceId': funding_source['id'],
            'created': datetime.datetime.strptime(funding_source['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'channels': funding_source['channels'],
            'bankName': funding_source['bankName']
        })


    @operator.ledger_created(const.INITIATE_MICRO_DEPOSITS_REQUEST)
    def on_initiate_micro_deposits_request(event):
        funding_source_url = f"{dwolla_hostname}/funding-sources/{event.cdata['fundingSourceId']}"
        new_micro_deposits_resp = app_token.post(f"{funding_source_url}/micro-deposits")
        LOG.debug(f"new_micro_deposits_resp status: {new_micro_deposits_resp.status}, "
                  f"headers: {new_micro_deposits_resp.headers}, "
                  f"body: {new_micro_deposits_resp.body}")

        if new_micro_deposits_resp.status >= 400:
            return dazl.exercise(event.cid, const.C_INITIATE_MICRO_DEPOSITS_REQUEST_REJECT, {})

        micro_deposits_resp = app_token.get(f"{funding_source_url}/micro-deposits")
        LOG.debug(f"micro_deposits_resp status: {micro_deposits_resp.status}, "
                  f"headers: {micro_deposits_resp.headers}, "
                  f"body: {micro_deposits_resp.body}")

        micro_deposits = micro_deposits_resp.body

        return dazl.exercise(event.cid, const.C_INITIATE_MICRO_DEPOSITS_REQUEST_ACCEPT, {
            'created': datetime.datetime.strptime(micro_deposits['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'status': micro_deposits['status'],
            'failure': {
                'code': '',
                'description': ''
            }
        })


    # need hook for changing the status of micro-deposits


    @operator.ledger_created(const.FUNDING_SOURCE_VERIFICATION_REQUEST)
    def on_funding_source_verification_request(event):
        cdata = event.cdata
        request_body = {
            'amount1': {
                'value': cdata['amount1']['value'],
                'currency': cdata['amount1']['currency']
            },
            'amount2': {
                'value': cdata['amount2']['value'],
                'currency': cdata['amount2']['currency']
            }
        }

        funding_source_url = f"{dwolla_hostname}/funding-sources/{cdata['fundingSourceId']}"
        verify_micro_deposits_resp = app_token.post('%s/micro-deposits' % funding_source_url, request_body)
        LOG.debug(f"verify_micro_deposits_resp status: {verify_micro_deposits_resp.status}, "
                  f"headers: {verify_micro_deposits_resp.headers}, "
                  f"body: {verify_micro_deposits_resp.body}")

        if verify_micro_deposits_resp.status != 200:
            return dazl.exercise(event.cid, const.C_FUNDING_SOURCE_VERIFICATION_REQUEST_REJECT, {})

        return dazl.exercise(event.cid, const.C_FUNDING_SOURCE_VERIFICATION_REQUEST_ACCEPT, {})


    @operator.ledger_created(const.FUNDING_SOURCE_VERIFICATION)
    def on_funding_source_verification(event):
        verification_cid = event.cid
        cdata = event.cdata
        funding_source_cid, funding_source_cdata = event.acs_find_one(const.T_FUNDING_SOURCE, {
            'operator': cdata['operator'],
            'user': cdata['user'],
            'fundingSourceId': cdata['fundingSourceId']
        })

        LOG.debug(f"found funding source cid: {funding_source_cid.status}, cdata: {funding_source_cdata}")

        return dazl.exercise(funding_source_cid, const.C_FUNDING_SOURCE_VERIFY, {
            'verificationCid': verification_cid
        })


    @operator.ledger_created(const.TRANSFER_AGREEMENT)
    def on_transfer_agreement(event):
        cdata = event.cdata
        sender_funding_source_cid, sender_funding_source_cdata = event.acs_find_one(
            const.T_FUNDING_SOURCE, {
                'operator': cdata['operator'],
                'user': cdata['sender'],
                'fundingSourceId': cdata['senderSourceId'],
                'status': 'verified'
            }
        )
        LOG.debug(f"found sender funding source cid: {sender_funding_source_cid}, "
                  f"cdata: {sender_funding_source_cdata}")

        receiver_funding_source_cid, receiver_funding_source_cdata = event.acs_find_one(
            const.FUNDING_SOURCE, {
                'operator': cdata['operator'],
                'user': cdata['receiver'],
                'fundingSourceId': cdata['receiverSourceId']
            }
        )
        LOG.debug(f"found receiver funding source cid: {receiver_funding_source_cid}, "
                  f"cdata: {receiver_funding_source_cdata}")

        return dazl.exercise(event.cid, const.C_TRANSFER_AGREEMENT_VALIDATE, {
            'senderFundingCid': sender_funding_source_cid,
            'receiverFundingCid': receiver_funding_source_cid,
            'optClearing': {
                'optSource': '',
                'optDestination': ''
            },
            'optAchDetails': {
                'source': {
                    'addenda': [''],
                    'traceId': ''
                },
                'destination': {
                    'addenda': [''],
                    'traceId': ''
                }
            },
            'optCorrelationId': "one-two-three"
        })


    @operator.ledger_created(const.TRANSFER_REQUEST)
    def on_transfer_request(event):
        cdata = event.cdata
        funding_source_url = f"{dwolla_hostname}/funding-sources"
        request_body = {
            '_links': {
                'source': {
                    'href': f"{funding_source_url}/{cdata['senderSourceId']}"
                },
                'destination': {
                    'href': f"{funding_source_url}/{cdata['receiverSourceId']}"
                }
            },
            'amount': {
                'currency': cdata['amount']['currency'],
                'value': cdata['amount']['value']
            },
            'correlationId': cdata['correlationId']
        }

        new_transfer_resp = app_token.post('transfers', request_body)
        LOG.debug(f"new_transfer_resp status: {new_transfer_resp.status}, "
                  f"headers: {new_transfer_resp.headers}, "
                  f"body: {new_transfer_resp.body}")

        if new_transfer_resp.status >= 400:
            return  # should exercise a fail choice

        transfer_resp = app_token.get(new_transfer_resp.headers['location'])
        LOG.debug(f"transfer_resp status: {transfer_resp.status}, "
                  f"headers: {transfer_resp.headers}, "
                  f"body: {transfer_resp.body}")

        transfer = transfer_resp.body

        return dazl.exercise(event.cid, const.C_TRANSFER_REQUEST_SENT, {
            'transferId': transfer['id'],
            'status': transfer['status'],
            'created':datetime.datetime.strptime(transfer['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'individualAchId': transfer['individualAchId']
        })


    network.run_forever()
