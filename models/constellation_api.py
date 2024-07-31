import requests
import logging
import time

_logger = logging.getLogger(__name__)

class ConstellationAPI:
    def __init__(self, base_url, faucet_url, check_status_url):
        self.base_url = base_url
        self.faucet_url = faucet_url
        self.check_status_url = check_status_url

    def _make_request(self, method, url, retries=3, **kwargs):
        for attempt in range(retries):
            try:
                response = requests.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                _logger.error(f"Attempt {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)
        return None

    def get_metagraph_status(self, transaction_hash):
        _logger.info(f"Getting metagraph status for transaction hash: {transaction_hash}")
        url = f"{self.check_status_url}/transactions/{transaction_hash}"
        response = self._make_request('GET', url)
        if response:
            _logger.info(f"Response Status Code: {response.status_code}")
            _logger.info(f"Response Content: {response.content}")
            try:
                return response.json()
            except ValueError:
                _logger.error(f"Failed to parse JSON response: {response.content}")
        return {}

    def get_testnet_dag(self, wallet_address):
        _logger.info(f"Requesting TestNet DAG for wallet address: {wallet_address}")
        url = f"{self.faucet_url}/{wallet_address}"
        response = self._make_request('GET', url)
        if response:
            _logger.info(f"Response Status Code: {response.status_code}")
            _logger.info(f"Response Content: {response.content}")
            try:
                return response.json()
            except ValueError:
                _logger.error(f"Failed to parse JSON response: {response.content}")
        return {}

    def send_payment(self, source_wallet, destination_wallet, amount, fee=0):
        payment_data = {
            "source": source_wallet,
            "destination": destination_wallet,
            "amount": amount,
            "fee": fee
        }
        _logger.info(f"Sending payment: {payment_data}")
        url = f"{self.base_url}/payments"
        response = self._make_request('POST', url, json=payment_data)
        if response:
            _logger.info(f"Response Status Code: {response.status_code}")
            _logger.info(f"Response Content: {response.content}")
            try:
                return response.json()
            except ValueError:
                _logger.error(f"Failed to parse JSON response: {response.content}")
        return {}
