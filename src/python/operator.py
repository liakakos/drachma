import logging
import _thread
from datetime import datetime
from argparse import ArgumentParser

from dazl import Network, exercise
from dwollav2 import Client
from flask import Flask, request, abort

import constants as const


if __name__ == '__main__':
    parser = ArgumentParser(description="Dwolla Operator")
    parser.add_argument('dwolla_app_key', type=str, help="Dwolla App Key")
    parser.add_argument('dwolla_app_secret', type=str, help="Dwolla App Secret")
    parser.add_argument('operator', type=str, help="Operator Name")
    parser.add_argument('-e', '--dwolla_env', type=str, choices=['production', 'sandbox'],
                        help="Dwolla Environment", default='production')
    parser.add_argument('-l', '--ledger_host', type=str, help="Ledger Host URL", default='localhost')
    parser.add_argument('-p', '--ledger_port', type=int, help="Ledger Port", default=6865)
    parser.add_argument('-v', '--log_level', type=str, choices=['ERROR', 'WARNING', 'INFO', 'DEBUG'],
                        help="Log Level", default='WARNING')
    parser.add_argument('-w', '--webhook_url', type=str, help="HTTP Webhook Listener URL",
                        default='http://localhost:5000')

    args = parser.parse_args()

    network = Network()
    network.set_config(url=f'http://{args.ledger_host}:{args.ledger_port}')

    operator = network.simple_party(args.operator)

    client = Client(key=args.dwolla_app_key,
                    secret=args.dwolla_app_secret,
                    environment=args.dwolla_env)

    dwolla_hostname = client.api_url
    app_token = client.Auth.client()

    webhooks = Flask(__name__)

    logging.basicConfig(level=args.log_level)
    LOG = logging.getLogger('operator')


    def flask_thread():
        print("starting flask thread")
        webhooks.run(debug=False, use_reloader=False)


    def delete_webhook_subsriptions():
        webhook_subsriptions_resp = app_token.get('webhook-subscriptions')
        LOG.debug(f"webhook_subsriptions_resp status: {webhook_subsriptions.status}, "
                  f"headers: {webhook_subsriptions.headers}, "
                  f"body: {webhook_subsriptions.body}")
        for webhook in webhook_subsriptions_resp.body['_embedded']['webhook-subscriptions']:
            app_token.delete(webhook['_links']['self']['href'])


    def subscribe_to_webhooks():
        request_body = {
            'url': f'{args.webhook_url}/webhooks',
            'secret': args.dwolla_app_secret
        }
        subscription_resp = app_token.post('webhook-subscriptions', request_body)
        LOG.debug(f"subscription_resp status: {subscription_resp.status}, "
                  f"headers: {subscription_resp.headers}, "
                  f"body: {subscription_resp.body}")


    @webhooks.route('/webhooks', methods=['POST'])
    def on_webhook():
        if request.method == 'POST':
            webhook = request.json
            topic = webhook['topic']
            if topic == 'customer_microdeposits_completed':
                micro_deposits_resp = app_token.get(webhook['_links']['resource']['href'])
                LOG.debug(f"micro_deposits_resp status: {micro_deposits_resp.status}, "
                          f"headers: {micro_deposits_resp.headers}, "
                          f"body: {micro_deposits_resp.body}")

                micro_deposits_cid, micro_deposits_cdata = operator.find_one(const.T_MICRO_DEPOSITS, {
                    'fundingSourceId': webhook['resourceId'],
                    'status': 'pending'
                })

                operator.submit_exercise(micro_deposits_cid, const.C_MICRO_DEPOSITS_UPDATE_STATUS, {
                    'newStatus': 'processed'
                })

            return '', 200
        else:
            abort(400)


    @operator.ledger_created(const.T_UNVERIFIED_CUSTOMER_REQUEST)
    def on_unverified_customer_request(event):
        cdata = event.cdata
        LOG.debug(f"UNVERIFIED_CUSTOMER_REQUEST cdata: {cdata}")
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

        return exercise(event.cid, const.C_UNVERIFIED_CUSTOMER_REQUEST_ACCEPT, {
            'customerId': customer['id'],
            'created': datetime.strptime(customer['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'status': customer['status']
        })


    @operator.ledger_created(const.T_VERIFIED_CUSTOMER_REQUEST)
    def on_verified_customer_request(event):
        cdata = event.cdata
        LOG.debug(f"VERIFIED_CUSTOMER_REQUEST cdata: {cdata}")
        request_body = {
            'firstName': cdata['firstName'],
            'lastName': cdata['lastName'],
            'email': cdata['email'],
            'type': 'personal',
            'address1': cdata['address1'],
            'address2': cdata['optAddress2'] if cdata['optAddress2'] is not None else '',
            'city': cdata['city'],
            'state': cdata['state'],
            'postalCode': cdata['postalCode'],
            'dateOfBirth': datetime.strftime(cdata['dateOfBirth'], "%Y-%m-%d"),
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

        return exercise(event.cid, const.C_VERIFIED_CUSTOMER_REQUEST_ACCEPT, {
            'customerId': customer['id'],
            'created': datetime.strptime(customer['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'status': customer['status']
        })


    @operator.ledger_created(const.T_UNVERIFIED_FUNDING_SOURCE_REQUEST)
    def on_unverified_funding_source_request(event):
        cdata = event.cdata
        LOG.debug(f"UNVERIFIED_FUNDING_SOURCE_REQUEST cdata: {cdata}")
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

        return exercise(event.cid, const.C_UNVERIFIED_FUNDING_SOURCE_REQUEST_ACCEPT, {
            'fundingSourceId': funding_source['id'],
            'created': datetime.strptime(funding_source['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'channels': funding_source['channels'],
            'bankName': funding_source['bankName']
        })


    @operator.ledger_created(const.T_INITIATE_MICRO_DEPOSITS_REQUEST)
    def on_initiate_micro_deposits_request(event):
        funding_source_url = f"{dwolla_hostname}/funding-sources/{event.cdata['fundingSourceId']}"
        new_micro_deposits_resp = app_token.post(f"{funding_source_url}/micro-deposits")
        LOG.debug(f"new_micro_deposits_resp status: {new_micro_deposits_resp.status}, "
                  f"headers: {new_micro_deposits_resp.headers}, "
                  f"body: {new_micro_deposits_resp.body}")

        if new_micro_deposits_resp.status >= 400:
            return exercise(event.cid, const.C_INITIATE_MICRO_DEPOSITS_REQUEST_REJECT, {})

        micro_deposits_resp = app_token.get(f"{funding_source_url}/micro-deposits")
        LOG.debug(f"micro_deposits_resp status: {micro_deposits_resp.status}, "
                  f"headers: {micro_deposits_resp.headers}, "
                  f"body: {micro_deposits_resp.body}")

        micro_deposits = micro_deposits_resp.body

        return exercise(event.cid, const.C_INITIATE_MICRO_DEPOSITS_REQUEST_ACCEPT, {
            'created': datetime.strptime(micro_deposits['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'status': micro_deposits['status'],
            'failure': {
                'code': '',
                'description': ''
            }
        })


    # need hook for changing the status of micro-deposits


    @operator.ledger_created(const.T_FUNDING_SOURCE_VERIFICATION_REQUEST)
    def on_funding_source_verification_request(event):
        cdata = event.cdata
        LOG.debug(f"FUNDING_SOURCE_VERIFICATION_REQUEST cdata: {cdata}")
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
            return exercise(event.cid, const.C_FUNDING_SOURCE_VERIFICATION_REQUEST_REJECT, {})

        return exercise(event.cid, const.C_FUNDING_SOURCE_VERIFICATION_REQUEST_ACCEPT, {})


    @operator.ledger_created(const.T_FUNDING_SOURCE_VERIFICATION)
    def on_funding_source_verification(event):
        verification_cid = event.cid
        cdata = event.cdata
        LOG.debug(f"FUNDING_SOURCE_VERIFICATION cdata: {cdata}")
        funding_source_cid, funding_source_cdata = event.acs_find_one(const.T_FUNDING_SOURCE, {
            'operator': cdata['operator'],
            'user': cdata['user'],
            'fundingSourceId': cdata['fundingSourceId']
        })

        LOG.debug(f"found funding source cid: {funding_source_cid}, cdata: {funding_source_cdata}")

        return exercise(funding_source_cid, const.C_FUNDING_SOURCE_VERIFY, {
            'verificationCid': verification_cid
        })


    @operator.ledger_created(const.T_TRANSFER_AGREEMENT)
    def on_transfer_agreement(event):
        cdata = event.cdata
        LOG.debug(f"TRANSFER_AGREEMENT cdata: {cdata}")
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
            const.T_FUNDING_SOURCE, {
                'operator': cdata['operator'],
                'user': cdata['receiver'],
                'fundingSourceId': cdata['receiverSourceId']
            }
        )
        LOG.debug(f"found receiver funding source cid: {receiver_funding_source_cid}, "
                  f"cdata: {receiver_funding_source_cdata}")

        return exercise(event.cid, const.C_TRANSFER_AGREEMENT_VALIDATE, {
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


    @operator.ledger_created(const.T_TRANSFER_REQUEST)
    def on_transfer_request(event):
        cdata = event.cdata
        LOG.debug(f"TRANSFER_REQUEST cdata: {cdata}")
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

        return exercise(event.cid, const.C_TRANSFER_REQUEST_SENT, {
            'transferId': transfer['id'],
            'status': transfer['status'],
            'created': datetime.strptime(transfer['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'individualAchId': ''
            # 'individualAchId': transfer['individualAchId']
        })


    _thread.start_new_thread(flask_thread, ())

    delete_webhook_subsriptions()
    subscribe_to_webhooks()

    network.run_forever()
