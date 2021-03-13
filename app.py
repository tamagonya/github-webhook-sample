# -*- coding: utf-8 -*-

#
# Github Webhook & Branch Protection Sample
#
# github_api_headers: Github REST API headers
# github_update_branch_protection: Update branch protection via Github REST API
# github_create_issue: Create issue via Github REST API
# webhook_event: Endpoint for Github Webhook
# hello_world: root Endpoint
#

from flask import Flask, request, Response
import requests
import logging
import sys

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def github_api_headers():
    # https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api
    content_type = 'application/vnd.github.v3+json'
    token = 'YOUR-TOKEN'
    return {
        'Authorization': 'token {:s}'.format(token),
        'Accept': content_type,
    }


def github_update_branch_protection(org, repo_name, branch):
    # https://docs.github.com/en/rest/reference/repos#update-branch-protection
    result = False
    try:
        endpoint = 'repos/{}/{}/branches/{}/protection'.format(org, repo_name, branch)
        payload = {"required_status_checks": {"strict": False, "contexts": []}, "enforce_admins": False,
                   "required_pull_request_reviews": {"dismissal_restrictions": {"users": [], "teams": []}},
                   "restrictions": {"users": [], "teams": [], "apps": []}}

        repo_response = requests.put('https://api.github.com/' + endpoint, json=payload, headers=github_api_headers())
        if repo_response.status_code == 200:
            logging.info('updated branch protection. {}'.format(payload))
            result = True
        else:
            logging.error('updated branch protection received invalid status code. {}'.format(repo_response.status_code))

    except Exception as e:
        logging.error('update branch protection error. {}'.format(e))
    return result


def github_create_issue(org, repo_name, mention):
    # https://docs.github.com/en/rest/reference/issues#create-an-issue
    try:
        endpoint = 'repos/{}/{}/issues'.format(org, repo_name)
        body = 'Main branch protection has been added. - @{}'.format(mention)
        payload = {'title': 'settings notification', 'body': body}
        repo_response = requests.post('https://api.github.com/' + endpoint, json=payload, headers=github_api_headers())
        if repo_response.status_code == 201:
            logging.info('created issue. {}'.format(payload))
        else:
            logging.error('create issue received invalid status code. {}'.format(repo_response.status_code))
    except Exception as e:
        logging.error('create issue error. {}'.format(e))



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/webhook', methods=['POST'])
def webhook_event():
    # https://docs.github.com/en/developers/webhooks-and-events/webhooks
    try:
        webhook_data = request.json
        logging.info(webhook_data)

        # detect webhook event for repository created action
        if webhook_data.get('action') is not None and webhook_data.get('repository') is not None:
            if webhook_data['action'] == 'created':
                repo_name = webhook_data['repository']['name']
                owner_login = webhook_data['repository']['owner']['login']
                org_login = webhook_data['organization']['login']
                sender_login = webhook_data['sender']['login']
                logging.info('create repository event received. {},{},{},{}'.format(org_login, repo_name, owner_login, sender_login))

                # update main branch protection
                update_result = github_update_branch_protection(org_login, repo_name, 'main')

                # create issue if branch protection succeeded
                if update_result:
                    github_create_issue(org_login, repo_name, sender_login)

    except Exception as e:
        logging.error('webhook_event error. {}'.format(e))

    return Response(status=200)


if __name__ == '__main__':
    app.run()
