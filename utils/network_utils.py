# utils/network_utils.py

import requests
import json

def get_node_status(node_url: str) -> Dict:
    """Get the status of a Pi Network node"""
    response = requests.get(f'{node_url}/status')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting node status: {response.status_code}'}

def get_blockchain_info(node_url: str) -> Dict:
    """Get the information of the Pi Network blockchain"""
    response = requests.get(f'{node_url}/blockchain/info')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting blockchain info: {response.status_code}'}

def get_block_by_height(node_url: str, height: int) -> Dict:
    """Get the block by height from the Pi Network blockchain"""
    response = requests.get(f'{node_url}/blockchain/block/{height}')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting block by height: {response.status_code}'}

def get_transaction_by_hash(node_url: str, hash: str) -> Dict:
    """Get the transaction by hash from the Pi Network blockchain"""
    response = requests.get(f'{node_url}/blockchain/transaction/{hash}')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting transaction by hash: {response.status_code}'}

def get_unconfirmed_transactions(node_url: str) -> Dict:
    """Get the unconfirmed transactions from the Pi Network blockchain"""
    response = requests.get(f'{node_url}/blockchain/unconfirmed_transactions')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting unconfirmed transactions: {response.status_code}'}

def get_pending_transactions(node_url: str) -> Dict:
    """Get the pending transactions from the Pi Network blockchain"""
    response = requests.get(f'{node_url}/blockchain/pending_transactions')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting pending transactions: {response.status_code}'}

def get_mempool_info(node_url: str) -> Dict:
    """Get the information of the Pi Network mempool"""
    response = requests.get(f'{node_url}/mempool/info')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mempool info: {response.status_code}'}

def get_mempool_transactions(node_url: str) -> Dict:
    """Get the transactions from the Pi Network mempool"""
    response = requests.get(f'{node_url}/mempool/transactions')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mempool transactions: {response.status_code}'}

def get_mempool_transaction_by_hash(node_url: str, hash: str) -> Dict:
    """Get the transaction by hash from the Pi Network mempool"""
    response = requests.get(f'{node_url}/mempool/transaction/{hash}')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mempool transaction by hash: {response.status_code}'}

def get_peers(node_url: str) -> Dict:
    """Get the peers of the Pi Network node"""
    response = requests.get(f'{node_url}/peers')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting peers: {response.status_code}'}

def get_mining_info(node_url: str) -> Dict:
    """Get the mining information of the Pi Network node"""
    response = requests.get(f'{node_url}/mining/info')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining info: {response.status_code}'}

def get_mining_stats(node_url: str) -> Dict:
    """Get the mining statistics of the Pi Network node"""
    response = requests.get(f'{node_url}/mining/stats')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining stats: {response.status_code}'}

def get_mining_blocks(node_url: str) -> Dict:
    """Get the mining blocks of the Pi Network node"""
    response = requests.get(f'{node_url}/mining/blocks')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining blocks: {response.status_code}'}

def get_mining_block_by_hash(node_url: str, hash: str) -> Dict:
    """Get the mining block by hash from the Pi Network node"""
    response = requests.get(f'{node_url}/mining/block/{hash}')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining block by hash: {response.status_code}'}

def get_mining_block_by_height(node_url: str, height: int) -> Dict:
    """Get the mining block by height from the Pi Network node"""
    response = requests.get(f'{node_url}/mining/block/{height}')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining block by height: {response.status_code}'}

def get_mining_transactions(node_url: str) -> Dict:
    """Get the mining transactions from the Pi Network node"""
    response = requests.get(f'{node_url}/mining/transactions')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining transactions: {response.status_code}'}

def get_mining_transaction_by_hash(node_url: str, hash: str) -> Dict:
    """Get the mining transaction by hash from the Pi Network node"""
    response = requests.get(f'{node_url}/mining/transaction/{hash}')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining transaction by hash: {response.status_code}'}

def get_mining_unconfirmed_transactions(node_url: str) -> Dict:
    """Get the mining unconfirmed transactions from the Pi Network node"""
    response = requests.get(f'{node_url}/mining/unconfirmed_transactions')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining unconfirmed transactions: {response.status_code}'}

def get_mining_pending_transactions(node_url: str) -> Dict:
    """Get the mining pending transactions from the Pi Network node"""
    response = requests.get(f'{node_url}/mining/pending_transactions')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error getting mining pending transactions: {response.status_code}'}
