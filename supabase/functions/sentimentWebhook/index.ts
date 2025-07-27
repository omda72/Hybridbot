import { serve } from "https://deno.land/std/http/server.ts";

serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }

  const body = await req.json();
  const { coin, sentiment, recommendation, confidence, timestamp } = body;

  console.log("📩 Received sentiment:", body);

  // 👉 Insert trading logic or routing here
  if (coin === "SOL") {
    console.log(`🛠️ Routing to Solana trader: ${recommendation}`);
  } else if (coin === "ETH") {
    console.log(`🛠️ Routing to Ethereum trader: ${recommendation}`);
  } else {
    console.log(`🔍 Coin not recognized: ${coin}`);
  }

  return new Response(
    JSON.stringify({ status: "success", coin, sentiment, timestamp }),
    { status: 200, headers: { "Content-Type": "application/json" } }
  );
});