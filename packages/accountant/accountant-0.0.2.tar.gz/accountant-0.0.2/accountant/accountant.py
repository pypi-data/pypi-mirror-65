from ledger.client import LedgerClient

import logging

log = logging.getLogger(__name__)


class Accountant:
    """
    Accountant binds together 2 concepts - BankAccount & Ledger
    Ledger is the source of truth for the Bank
    Ledger ALWAYS reflect the true state of the OutsideWorld
    Accountant MUST manage BankAccount's books inside Ledger properly
    Accountant stores no state
    """
    DEFAULT_CASH_BOOK_ID = {'name': 'cash_book', 'id': '1'}

    def __init__(self, bank_account):
        self.bank_account = bank_account
        self.ledger = LedgerClient(ledger_host="http://ledger-service-dev-1.local-dev:3000")

        log.info("---------Initialising-------------")
        log.info("Bank Account Number: ", self.bank_account['account_id'])
        log.info("Main Account Book: ", self.bank_account['ledger_books']['main_balance'])
        log.info("Block Account Book: ", self.bank_account['ledger_books']['blocked_balance'])
        log.info("Cash Book: ", self.DEFAULT_CASH_BOOK_ID)

    def get_book_balances(self, currency):
        log.info("---------Balance----------")
        blocked_deposit_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={'operation': 'DEPOSIT'})

        blocked_withdraw_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={'operation': 'WITHDRAW'})

        main_balance = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['main_balance']['id'],
                                                     asset_id=currency)

        return {'Blocked_balance_deposit': blocked_deposit_balance,
                'Blocked_balance_withdraw': blocked_withdraw_balance,
                'Main_balance': main_balance}

    def withdraw_block_amount(self, value, currency, memo):
        log.info("---------Block_Amount_Withdraw----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['main_balance']['id'],
            to_book_id=self.bank_account['ledger_books']['blocked_balance']['id'], asset_id=currency, value=value,
            memo=memo, metadata={'operation': 'WITHDRAW'})
        log.info(operation)
        return operation

    def deposit_block_amount(self, value, currency, memo):
        log.info("---------Block_Amount_Deposit----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.DEFAULT_CASH_BOOK_ID['id'],
            to_book_id=self.bank_account['ledger_books']['blocked_balance']['id'], asset_id=currency, value=value,
            memo=memo,
            metadata={'operation': 'DEPOSIT'})
        log.info(operation)
        return operation

    def withdraw_unblock_amount(self, value, currency, memo):
        log.info("---------Unblock_Amount_Withdraw----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.bank_account['ledger_books']['main_balance']['id'], asset_id=currency, value=value,
            memo=memo,
            metadata={'operation': 'WITHDRAW'})
        log.info(operation)
        return operation

    def deposit_unblock_amount(self, value, currency, memo):
        log.info("---------Unblock_Amount_Deposit----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.DEFAULT_CASH_BOOK_ID['id'], asset_id=currency, value=value, memo=memo,
            metadata={'operation': 'DEPOSIT'})
        log.info(operation)
        return operation

    def withdraw_amount(self, value, currency, memo):
        log.info("---------Withdraw_amount----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.DEFAULT_CASH_BOOK_ID['id'],
            asset_id=currency, value=value, memo=memo, metadata={'operation': 'WITHDRAW'})
        log.info(operation)
        return operation

    def deposit_amount(self, value, currency, memo):
        log.info("---------Deposit_amount----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.bank_account['ledger_books'][
                'main_balance']['id'], asset_id=currency, value=value,
            memo=memo, metadata={'operation': 'DEPOSIT'})
        log.info(operation)
        return operation

    def create_book(self):
        log.info("---------New_ledger-------------")
        block_book_id = self.ledger.create_book(name=f"{self.bank_account['account_id']}_block_book",
                                                min_balance="-100")
        main_book_id = self.ledger.create_book(name=f"{self.bank_account['account_id']}_main_book", min_balance="-100")
        new_books = {
            'main_balance': {'name': main_book_id['name'],
                             'id': main_book_id['id']},
            'blocked_balance': {'name': block_book_id['name'],
                                'id': block_book_id['id']}
        }
        log.info(new_books)
        return new_books
