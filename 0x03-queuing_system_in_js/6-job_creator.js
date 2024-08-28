const kue = require('kue');
const queue = kue.createQueue();

const jobData = {
    phoneNumber: '07123456789',
    message: 'This is the code to verify your account',
}

let job = queue.create('push_notification_code', jobData).save((err) => {
    if (!err) console.log(`Notification job created: ${job.id}`);
});
job.on('complete', () => console.log('Notification job completed'));
job.on('failed', () => console.log('Notification job failed'));
