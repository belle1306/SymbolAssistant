import * as express from 'express';
import Config from './src/config'

const app = express()
const port = 3000
import SymbolHelper from './src/SymbolHelper'


// get account balance
app.get('/account', async (req, res) => {
  const symbolHelper = new SymbolHelper();

  try {
    const balance = await symbolHelper.getAccountBalance();
    res.send(JSON.stringify(balance));

    return JSON.stringify(balance);
  } catch(ex) {
    return null;
  }
})

// get last transaction
app.get('/transaction/last', async (req, res) => {
  const symbolHelper = new SymbolHelper();

  try {
    const lastTransactionInfo = await symbolHelper.getLastTransaction();
    res.send(JSON.stringify(lastTransactionInfo));

    return JSON.stringify(lastTransactionInfo);
  } catch(ex) {
    return null;
  }
})

// get last message
app.get('/message/last', async (req, res) => {
  const symbolHelper = new SymbolHelper();

  try {
    const lastMessageInfo = await symbolHelper.getLastMessage();
    res.send(JSON.stringify(lastMessageInfo));
    return JSON.stringify(lastMessageInfo);
  } catch(ex) {
    return null;
  }
})

// send message
app.get('/transaction/send/:address/:amount/:message?', async (req, res) => {
  const symbolHelper = new SymbolHelper();

  try {
    const txHash: string = await symbolHelper.sendTransaction(req.params.address, Number(req.params.amount), req.params.message);

    // wait x sec and check confirmation
    setTimeout(async () => {
      const txConfirmed = await symbolHelper.isTransactionConfirmed(txHash);

      // tx is confirmed
      if (txConfirmed) {
        const accountBalanceInfo = await symbolHelper.getAccountBalance();
        res.send(JSON.stringify(accountBalanceInfo));

        return JSON.stringify(accountBalanceInfo);
      } else {
        return null;
      }
    }, Config.MAX_TX_CONFIRM_TIME * 1000) 
  } catch(ex) {
    console.log(ex);
    return null;
  }
})

// start server
app.listen(Config.SERVER_PORT, () => {
  console.log(`Symbol Assistant server listening at http://localhost:${Config.SERVER_PORT}`)
})

