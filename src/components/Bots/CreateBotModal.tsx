const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();

  const newBot: Omit<TradingBot, 'id'> = {
    name: formData.name,
    status: 'stopped',
    exchange: formData.exchange,
    pair: formData.pair,
    strategy: formData.strategy,
    pnl: 0,
    pnlPercent: 0,
    trades: 0,
    winRate: 0,
    createdAt: new Date().toISOString().split('T')[0]
  };

  // 1. Send new bot data to Firebase backend
  fetch("https://us-central1-hybridbot-fe281.cloudfunctions.net/api/bots", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: newBot.name,
      exchange: newBot.exchange,
      pair: newBot.pair,
      strategy: newBot.strategy,
      riskLevel: formData.riskLevel,
      user: "emaddev" // optional, can swap with actual user auth later
    }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to save bot to backend");
      return res.text();
    })
    .then((msg) => console.log("✅ Backend says:", msg))
    .catch((err) => console.error("❌ Error creating bot:", err));

  // 2. Update local state/UI
  onCreateBot(newBot);
};
