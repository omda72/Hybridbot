const { id, keccak256, toUtf8Bytes, parseUnits } = require('ethers');
const { BigNumber } = require('ethers');

// Solana parser
function parseTokenTransfer(logs) {
  if (!Array.isArray(logs)) return null;

  let result = {
    type: null,
    amount: null,
    source: null,
    destination: null,
    authority: null
  };

  for (const line of logs) {
    if (line.includes('Instruction: Transfer')) result.type = 'Transfer';
    if (line.includes('amount:')) result.amount = line.split('amount:')[1].trim();
    if (line.includes('source:')) result.source = line.split('source:')[1].trim();
    if (line.includes('destination:')) result.destination = line.split('destination:')[1].trim();
    if (line.includes('authority:')) result.authority = line.split('authority:')[1].trim();
  }

  if (result.type && result.destination) {
    return result;
  }

  return null;
}

// Ethereum ERC20 Transfer topic
const TRANSFER_TOPIC = keccak256(toUtf8Bytes('Transfer(address,address,uint256)'));

// Ethereum parser
function parseTokenTransferEth(log) {
  if (!log || !log.topics || log.topics[0] !== TRANSFER_TOPIC) return null;

  try {
    const from = '0x' + log.topics[1].slice(-40);
    const to = '0x' + log.topics[2].slice(-40);
    const value = BigNumber.from(log.data).toString();

    return {
      type: 'ERC20_TRANSFER',
      amount: value,
      source: from,
      destination: to,
      tokenAddress: log.address,
      txHash: log.transactionHash || 'N/A',
    };
  } catch (err) {
    console.error('⚠️ Failed to parse ETH transfer log:', err.message);
    return null;
  }
}

module.exports = {
  parseTokenTransfer,
  parseTokenTransferEth,
};
