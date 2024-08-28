import { createClient } from "redis";
import redis from "redis";
import { promisify } from "util";

const client = createClient()
  .on("error", (error) => console.log(`Redis client not connected to the server: ${error.message}`))
  .on("connect", () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
    client.set(schoolName, value, (error, reply) => {
        if (error) console.log(`Error setting value: ${error.message}`);
        redis.print(`Reply: ${reply}`);
    });
}

async function displaySchoolValue(schoolName) {
    const getAsync = promisify(client.get).bind(client);
    const reply = await getAsync(schoolName);
    console.log(reply);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');