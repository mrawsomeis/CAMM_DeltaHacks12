import { kv } from "@vercel/kv";

export default async function handler(req, res) {
  const auth = req.headers.authorization;
  if (auth !== `Bearer ${process.env.API_KEY}`) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  if (req.method === "POST") {
    await kv.set("latest_state", req.body);
    return res.json({ ok: true });
  }

  if (req.method === "GET") {
    const state = await kv.get("latest_state");
    return res.json({ state });
  }
}
