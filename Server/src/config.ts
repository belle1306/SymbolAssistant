import Friend from 'types/Friend'

class Config {
  // server port
  static SERVER_PORT: number = 3000

  // account address
  static ACCOUNT_RAW_ADDRESS: string = ''
  
  // account private key (for sending transactions)
  static ACCOUNT_PRIVATE_KEY: string = ''

  // node url address (mainet / testnet)
  static NODE_URL: string = 'http://api-01.us-east-1.testnet.symboldev.network:3000'

  // wait for transaction confirm (sec)
  static MAX_TX_CONFIRM_TIME: number = 30

  // saved contacts
  static FRIENDS_ADDRESSESS: Friend[] = [
    // John
    { name: 'John', address: 'xxxxxxxxxxxxxxxxxx' }
  ]
}

export default Config