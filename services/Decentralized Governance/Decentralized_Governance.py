import datetime
import json
import os
import random
import string
import time

class DecentralizedGovernance:
    def __init__(self, name, threshold=0.5, quorum=0.1):
        self.name = name
        self.threshold = threshold
        self.quorum = quorum
        self.proposals = []
        self.voters = set()
        self.votes = {}

    def new_proposal(self, description):
        proposal_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        proposal = {
            'id': proposal_id,
            'description': description,
            'status': 'open',
            'yes': 0,
            'no': 0,
            'abstain': 0,
            'timestamp': int(time.time()),
        }
        self.proposals.append(proposal)
        return proposal_id

    def vote(self, proposal_id, vote):
        proposal = next((p for p in self.proposals if p['id'] == proposal_id), None)
        if proposal is None:
            raise ValueError('Invalid proposal ID')
        if self.is_voter(vote['voter']):
            self.votes[vote['voter']] = vote['vote']

    def is_voter(self, voter):
        return voter in self.voters

    def add_voter(self, voter):
        self.voters.add(voter)

    def remove_voter(self, voter):
        self.voters.remove(voter)

    def close_proposal(self, proposal_id):
        proposal = next((p for p in self.proposals if p['id'] == proposal_id), None)
        if proposal is None:
            raise ValueError('Invalid proposal ID')
        if proposal['status'] != 'open':
            raise ValueError('Proposal is not open')
        proposal['status'] = 'closed'
        proposal['yes'] = sum(1 for v in self.votes.values() if v == 'yes')
        proposal['no'] = sum(1 for v in self.votes.values() if v == 'no')
        proposal['abstain'] = sum(1 for v in self.votes.values() if v == 'abstain')
        self.votes = {}

    def result(self, proposal_id):
        proposal = next((p for p in self.proposals if p['id'] == proposal_id), None)
        if proposal is None:
            raise ValueError('Invalid proposal ID')
        if proposal['status'] != 'closed':
            raise ValueError('Proposal is not closed')
        total_votes = proposal['yes'] + proposal['no'] + proposal['abstain']
        quorum_met = total_votes >= self.quorum * len(self.voters)
        if quorum_met:
            if proposal['yes'] > proposal['no']:
                return 'passed'
            else:
                return 'failed'
        else:
            return 'quorum_not_met'

    def get_proposals(self):
        return self.proposals

    def save(self, filename):
        data = {
            'name': self.name,
            'threshold': self.threshold,
            'quorum': self.quorum,
            'voters': list(self.voters),
            'proposals': self.proposals,
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.name = data['name']
        self.threshold = data['threshold']
        self.quorum = data['quorum']
        self.voters = set(data['voters'])
        self.proposals = data['proposals']
