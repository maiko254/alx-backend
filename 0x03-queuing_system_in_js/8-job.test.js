import { expect } from 'chai';
import sinon from 'sinon';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
    let queue = createQueue({ name: 'push_notification_code_test' });
    const consoleSpy = sinon.spy(console, 'log');

    beforeEach(() => {
        queue.testMode.enter();
    });

    afterEach(() => {
        queue.testMode.clear();
        queue.testMode.exit();
    });

    it('throw an error if jobs is not an array', () => {
        expect(createPushNotificationsJobs.bind(createPushNotificationsJobs, {}, queue)).to.throw(Error, 'Jobs is not an array');
    });
    it('should add two new jobs to the queue', () => {
        const jobData = [
            {
                phoneNumber: '4153518780',
                message: 'This is the code 1234 to verify your account'
            },
            {
                phoneNumber: '4153518781',
                message: 'This is the code 4562 to verify your account'
            }
        ];
        createPushNotificationsJobs(jobData, queue);

        expect(queue.testMode.jobs.length).to.equal(2);
        expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[0].data).to.deep.equal(jobData[0]);
        expect(queue.testMode.jobs[1].data).to.deep.equal(jobData[1]);
    });

    it('should log a message when a job is created', () => {
        queue.process('push_notification_code_3', (job, done) => {
            expect(consoleSpy.calledWith('Notification job create:', queue.testMode.jobData[0].id)).to.be.true;
            done();
        });
    });

    it('registers the progress event', () => {
        const jobData = [
            {
                phoneNumber: '4153518780',
                message: 'This is the code 1234 to verify your account'
            }
        ];
        createPushNotificationsJobs(jobData, queue);

        queue.process('push_notification_code_3', (job, done) => {
            job.progress(25, 100);
            expect(consoleSpy.calledWith('Notification job', job.id, '25% complete')).to.be.true;
            done();
        });
    });

    it('registers the complete event', () => {
        const jobData = [
            {
                phoneNumber: '4153518780',
                message: 'This is the code 1234 to verify your account'
            }
        ];
        createPushNotificationsJobs(jobData, queue);

        queue.process('push_notification_code_3', (job, done) => {
            job.progress(100, 100);
            expect(consoleSpy.calledWith('Notification job', job.id, 'completed')).to.be.true;
            done();
        });
    });
});