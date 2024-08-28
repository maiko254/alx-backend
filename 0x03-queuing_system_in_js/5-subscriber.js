import { createClient } from "redis";

const client = createClient()
  .on("error", (error) => console.log(`Redis client not connected to the server: ${error.message}`))
  .on("connect", () => console.log('Redis client connected to the server'))
  .on("message", (channel, message) => {
    console.log(message);
    if (message === 'KILL_SERVER') {
      client.unsubscribe();
      client.quit();
    }
  });

client.subscribe('holberton school channel');