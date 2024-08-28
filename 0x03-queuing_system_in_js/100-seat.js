const express = require('express');
const kue = require('kue');
const queue = kue.createQueue();
const { createClient } = require('redis');
const { promisify } = require('util');

const client = createClient();
const INITIAL_AVAILABLE_SEATS = 50;
let reservationEnabled = true;

const app = express();
const port = 1245;

app.listen(port, () => {
  client.set('available_seats', INITIAL_AVAILABLE_SEATS);
  console.log(`app listening at http://localhost:${port}`);
});

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservations are blocked' });
    return;
  }
  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
    } else {
      res.json({ status: 'Reservation failed' });
    }
  });
  job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
  job.on('failed', (error) => console.log(`Seat reservation job ${job.id} failed: ${error.message}`));
});

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats > 0) {
      reserveSeat(availableSeats - 1);
      const newAvailableSeats = await getCurrentAvailableSeats();
      if (newAvailableSeats === 0) {
        reservationEnabled = false;
      }
      if (newAvailableSeats >= 0) {
        done();
      } else {
        done(new Error('Not enough seats available'));
      }
    } else {
      done(new Error('Not enough seats available'));
    }
  });
  res.json({ status: 'Queue processing' });
});

function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const getAsync = promisify(client.get).bind(client);
  const availableSeats = await getAsync('available_seats');
  return parseInt(availableSeats, 10);
}

export default app;
