import { createClient } from "redis";
import redis from "redis";

const client = createClient()
  .on("error", (error) => console.log(`Redis client not connected to the server: ${error.message}`))
  .on("connect", () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
    client.set(schoolName, value, (error, reply) => {
        if (error) console.log(`Error setting value: ${error.message}`);
        redis.print(`Reply: ${reply}`);
    });
}

function displaySchoolValue(schoolName) {
    client.get(schoolName, (error, reply) => {
        if (error) console.log(`Error getting value: ${error.message}`);
        console.log(reply);
    });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');