const WebSocket = require('ws');
require('dotenv').config();
const { parseTokenTransfer, parseTokenTransferEth } = require('./parser.cjs');

const HELIUS_WS_URL = process.env.HELIUS_WEBSOCKET;
const INFURA_WS_URL = process.env.INFURA_WEBSOCKET;

const SOLANA_TOKEN_ADDRESSES = [
  'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
  '8JnNWJ46yfdq8sKgT1Lk4G7VWkAA8Rhh7LhqgJ6WY41G',
  'So11111111111111111111111111111111111111112'
];

let solanaWS, ethWS;
let solanaReconnectTimeout = null;
let ethReconnectTimeout = null;
const RECONNECT_DELAY_MS = 5000;

function connectSolana() {
  solanaWS = new WebSocket(HELIUS_WS_URL);

  solanaWS.on('open', () => {
    console.log('✅ Connected to Helius WebSocket (Solana)');

    SOLANA_TOKEN_ADDRESSES.forEach((address, index) => {
      const subscribeMessage = {
        jsonrpc: '2.0',
        id: index + 1,
        method: 'logsSubscribe',
        params: [
          { mentions: [address] },
          { commitment: 'confirmed' }
        ]
      };

      solanaWS.send(JSON.stringify(subscribeMessage));
      console.log(`📡 Subscribed to Solana token: ${address}`);
    });
  });

  solanaWS.on('message', (data) => {
    try {
      const msg = JSON.parse(data);
      if (msg.method === 'logsNotification') {
        const result = msg.params.result;
        const logs = result.value.logs;
        const signature = result.value.signature;

        const parsedEvent = parseTokenTransfer(logs);

        if (parsedEvent) {
          console.log('🧾 Parsed Solana Token Transfer Event:');
          console.log('  Signature:', signature || 'N/A');
          console.log('  Type:', parsedEvent.type);
          console.log('  Amount:', parsedEvent.amount);
          console.log('  Source:', parsedEvent.source);
          console.log('  Destination:', parsedEvent.destination);
          console.log('  Authority:', parsedEvent.authority);
        }
      }
    } catch (err) {
      console.error('⚠️ Error parsing Solana message:', err.message);
    }
  });

  solanaWS.on('close', () => {
    console.warn('❌ Solana WebSocket closed, reconnecting...');
    scheduleSolanaReconnect();
  });

  solanaWS.on('error', (err) => {
    console.error('⚠️ Solana WebSocket error:', err.message);
    solanaWS.close();
  });
}

function scheduleSolanaReconnect() {
  if (solanaReconnectTimeout) return;
  solanaReconnectTimeout = setTimeout(() => {
    solanaReconnectTimeout = null;
    connectSolana();
  }, RECONNECT_DELAY_MS);
}

function connectEthereum() {
  ethWS = new WebSocket(INFURA_WS_URL);

  ethWS.on('open', () => {
    console.log('✅ Connected to Infura WebSocket (Ethereum)');

    const subscribeMessage = {
      jsonrpc: '2.0',
      id: 1,
      method: 'eth_subscribe',
      params: ['logs'] // Or specify tokens here, e.g. ['logs', { address: '0xe0f63a424a4439cbe457d80e4f4b51ad25b2c56c' }]
    };

    ethWS.send(JSON.stringify(subscribeMessage));
    console.log('📡 Subscribed to Ethereum logs');
  });

  ethWS.on('message', (data) => {
    try {
      const msg = JSON.parse(data);

      if (msg.method === 'eth_subscription') {
        const log = msg.params.result;
        const parsed = parseTokenTransferEth(log);
        if (parsed) {
          console.log('🧾 Parsed Ethereum ERC-20 Transfer Event:');
          console.log(`  TxHash: ${parsed.txHash}`);
          console.log(`  Token: ${parsed.tokenAddress}`);
          console.log(`  From: ${parsed.source}`);
          console.log(`  To: ${parsed.destination}`);
          console.log(`  Amount: ${parsed.amount}`);
        }
      }
    } catch (err) {
      console.error('⚠️ Error parsing Ethereum message:', err.message);
    }
  });

  ethWS.on('close', () => {
    console.warn('❌ Ethereum WebSocket closed, reconnecting...');
    scheduleEthereumReconnect();
  });

  ethWS.on('error', (err) => {
    console.error('⚠️ Ethereum WebSocket error:', err.message);
    ethWS.close();
  });
}

function scheduleEthereumReconnect() {
  if (ethReconnectTimeout) return;
  ethReconnectTimeout = setTimeout(() => {
    ethReconnectTimeout = null;
    connectEthereum();
  }, RECONNECT_DELAY_MS);
}

// Start both WebSocket connections
connectSolana();
connectEthereum();
