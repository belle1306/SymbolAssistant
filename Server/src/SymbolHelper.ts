import fetch from 'node-fetch'
import { 
  Account, Address, RepositoryFactoryHttp, Transaction, TransferTransaction, TransactionGroup, 
  Order, TransactionType, Deadline, PlainMessage, UInt64 
} from 'symbol-sdk'
import Config from './config'
import Friend from 'types/Friend'

class SymbolHelper {
  private repositoryFactory: RepositoryFactoryHttp;
  private address: any;
  private transactions: any[];

  constructor() {
    this.repositoryFactory = new RepositoryFactoryHttp(Config.NODE_URL);
    this.address = Address.createFromRawAddress(Config.ACCOUNT_RAW_ADDRESS);
  }

  // check if transaction confirmed
  public async isTransactionConfirmed(hash: string): Promise<boolean> {
    const transactionHttp = this.repositoryFactory.createTransactionRepository();
    
    try {
      const transaction = await transactionHttp.getTransactionsById([hash], TransactionGroup.Confirmed).toPromise();

      if (transaction && transaction.length > 0) {
        return true;
      }
    } catch(ex) {
      console.log(ex);
      return false;
    }

    return false;
  }

  // get transactions
  private async getTransactions() {
    const transactionHttp = this.repositoryFactory.createTransactionRepository();
    const searchCriteria = {
      group: TransactionGroup.Confirmed,
      type: [TransactionType.TRANSFER],
      order: Order.Desc,
      address: this.address,
      pageNumber: 1,
      pageSize: 50
    };

    try {
      const transactions = await transactionHttp.search(searchCriteria).toPromise();
      this.transactions = transactions.data;
    } catch(ex) {
      this.transactions = null;
    }
  }

  // get XYM price (USD)
  private async getXymPrice(): Promise<number> {
    try {
      const priceResponse = await fetch('https://min-api.cryptocompare.com/data/price?fsym=XYM&tsyms=USD,BTC');
      const price = await priceResponse.json();

      return Number(price.USD);
    } catch(ex) {
      return null;
    }
  }

  // get account balance
  public async getAccountBalance(): Promise<Object> {
    const accountHttp = this.repositoryFactory.createAccountRepository();

    try {
      let accountInfo = await accountHttp.getAccountInfo(this.address).toPromise();
      this.getXymPrice();

      // check USD price
      const balanceXYM = Number(accountInfo.mosaics[0].amount) / 1000000;
      const xymPrice: number = await this.getXymPrice();
      const balanceUSD = balanceXYM * Number(xymPrice);
      
      return {
        "balance_xym": balanceXYM.toFixed(1),
        "balance_usd": balanceUSD.toFixed(1)
      };
    } catch (ex) {
      return null;
    }
  }

  // get last transaction
  public async getLastTransaction(): Promise<Object> {
    try {
      await this.getTransactions();

      if (!this.transactions || this.transactions.length === 0) {
        return null;
      }

      // get last transaction
      // @ts-ignore
      const lastTransaction = this.transactions[0];

      // get xym price in usd
      const xymPrice: number = await this.getXymPrice();

      // find friend address
      const friend: Friend = Config.FRIENDS_ADDRESSESS.find(el => el.address === lastTransaction.signer.address.address);

      // create transaction info obj
      const lastTransactionInfo = {
        // @ts-ignore
        amount_xym: lastTransaction.mosaics[0].amount.lower / 1000000,
        // @ts-ignore
        amount_usd: ((lastTransaction.mosaics[0].amount.lower / 1000000) * xymPrice).toFixed(1),
        // @ts-ignore
        recipient_address: lastTransaction.recipientAddress.address,
        // @ts-ignore
        signer_address: lastTransaction.signer.address.address,
        signer_name: friend ? friend.name : 'Unknown',
        // @ts-ignore
        message: lastTransaction.message.payload ? lastTransaction.message.payload : 'No message'
      }

      return lastTransactionInfo;
    } catch(ex) {
      return null;
    }
  }

  // get last message
  public async getLastMessage(): Promise<Object> {
    try {
      await this.getTransactions();

      if (!this.transactions || this.transactions.length === 0) {
        return null;
      }

      const messages = this.transactions.filter((tx) => {
        return Object.keys(tx).length !== 0 && (tx.message.type === 0 || tx.message.type === 1);
      });

      if (messages && messages.length > 1) {
        // get last message
        const lastMessage = messages[0]; 

        // get xym price in usd
        const xymPrice: number = await this.getXymPrice();

        // find friend address
        const friend: Friend = Config.FRIENDS_ADDRESSESS.find(el => el.address === lastMessage.signer.address.address);

        const lastMessageInfo = {
          // @ts-ignore
          amount_xym: lastMessage.mosaics[0].amount.lower / 1000000,
          // @ts-ignore
          amount_usd: ((lastMessage.mosaics[0].amount.lower / 1000000) * xymPrice).toFixed(1),
          // @ts-ignore
          recipient_address: lastMessage.recipientAddress.address,
          // @ts-ignore
          signer_address: lastMessage.signer.address.address,
          signer_name: friend ? friend.name : 'Unknown',
          // @ts-ignore
          message: lastMessage.message.payload       
        }

        return lastMessageInfo;
      }
    } catch(ex) {
      return null;
    }
  }

  // send transaction
  public async sendTransaction(recipientName: string, amount: number, message: string): Promise<string> {
    // https://docs.symbolplatform.com/guides/transfer/sending-a-transfer-transaction.html

    try {
      const epochAdjustment = await this.repositoryFactory.getEpochAdjustment().toPromise();
      const networkType = await this.repositoryFactory.getNetworkType().toPromise();
      const networkGenerationHash = await this.repositoryFactory.getGenerationHash().toPromise();
      const { currency } = await this.repositoryFactory.getCurrencies().toPromise();

      // read address

      // find friend address
      const friend: Friend = Config.FRIENDS_ADDRESSESS.find(el => el.name === recipientName);

      if (!friend) {
        return null;
      }

      const rawAddress = friend.address;
      const recipientAddress = Address.createFromRawAddress(rawAddress);

      const transferTransaction = TransferTransaction.create(
        Deadline.create(epochAdjustment),
        recipientAddress,
        [currency.createRelative(amount)],
        PlainMessage.create(message),
        networkType,
        UInt64.fromUint(2000000),
      );

      const privateKey = Config.ACCOUNT_PRIVATE_KEY;
      const account = Account.createFromPrivateKey(privateKey, networkType);
      const signedTransaction = account.sign(
        transferTransaction,
        networkGenerationHash,
      );
      
      console.log('Payload:', signedTransaction.payload);
      console.log('Transaction Hash:', signedTransaction.hash);

      const transactionRepository = this.repositoryFactory.createTransactionRepository();
      const response = await transactionRepository.announce(signedTransaction).toPromise();
      console.log(response);

      return signedTransaction.hash;
    } catch(ex) {
      console.log(ex);
      return null;
    }
  }
}

export default SymbolHelper