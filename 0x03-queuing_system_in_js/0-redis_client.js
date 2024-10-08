import { createClient } from "redis";

const client = createClient()
  .on("error", (error) => console.log(`Redis client not connected to the server: ${error.message}`))
  .on("connect", () => console.log('Redis client connected to the server'));
