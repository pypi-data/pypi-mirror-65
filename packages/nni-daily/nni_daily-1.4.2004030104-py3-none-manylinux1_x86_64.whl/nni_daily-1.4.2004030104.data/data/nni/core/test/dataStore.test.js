'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai_1 = require("chai");
const typescript_ioc_1 = require("typescript-ioc");
const component = require("../../common/component");
const datastore_1 = require("../../common/datastore");
const utils_1 = require("../../common/utils");
const nniDataStore_1 = require("../nniDataStore");
const sqlDatabase_1 = require("../sqlDatabase");
describe('Unit test for dataStore', () => {
    let ds;
    before(async () => {
        utils_1.prepareUnitTest();
        typescript_ioc_1.Container.bind(datastore_1.Database).to(sqlDatabase_1.SqlDB).scope(typescript_ioc_1.Scope.Singleton);
        typescript_ioc_1.Container.bind(datastore_1.DataStore).to(nniDataStore_1.NNIDataStore).scope(typescript_ioc_1.Scope.Singleton);
        ds = component.get(datastore_1.DataStore);
        await ds.init();
    });
    after(() => {
        ds.close();
        utils_1.cleanupUnitTest();
    });
    it('test emtpy experiment profile', async () => {
        const result = await ds.getExperimentProfile('abc');
        chai_1.expect(result).to.equal(undefined, 'Should not get any profile');
    });
    it('test experiment profiles CRUD', async () => {
        const profile = {
            params: {
                authorName: 'test1',
                experimentName: 'exp1',
                trialConcurrency: 2,
                maxExecDuration: 10,
                maxTrialNum: 5,
                trainingServicePlatform: 'local',
                searchSpace: `{
                    "dropout_rate": {
                        "_type": "uniform",
                        "_value": [0.1, 0.5]
                    },
                    "batch_size": {
                        "_type": "choice",
                        "_value": [50, 250, 500]
                    }
                }`,
                tuner: {
                    className: 'testTuner',
                    checkpointDir: '/tmp/cp'
                }
            },
            id: 'exp123',
            execDuration: 0,
            startTime: Date.now(),
            endTime: Date.now(),
            nextSequenceId: 0,
            revision: 0
        };
        const id = profile.id;
        for (let i = 0; i < 5; i++) {
            await ds.storeExperimentProfile(profile);
            profile.revision += 1;
        }
        const result = await ds.getExperimentProfile(id);
        chai_1.expect(result.revision).to.equal(4);
    });
    const testEventRecords = [
        {
            event: 'WAITING',
            jobId: '111'
        },
        {
            event: 'WAITING',
            jobId: '222'
        },
        {
            event: 'RUNNING',
            jobId: '111'
        },
        {
            event: 'RUNNING',
            jobId: '222'
        },
        {
            event: 'SUCCEEDED',
            jobId: '111',
            data: 'lr: 0.001'
        },
        {
            event: 'FAILED',
            jobId: '222'
        }
    ];
    const metricsData = [
        {
            trial_job_id: '111',
            parameter_id: 'abc',
            type: 'PERIODICAL',
            value: 'acc: 0.88',
            timestamp: Date.now()
        },
        {
            trial_job_id: '111',
            parameter_id: 'abc',
            type: 'FINAL',
            value: 'acc: 0.88',
            timestamp: Date.now()
        }
    ];
    it('test trial job events store /query', async () => {
        for (const event of testEventRecords) {
            await ds.storeTrialJobEvent(event.event, event.jobId, event.data);
        }
        for (const metrics of metricsData) {
            await ds.storeMetricData(metrics.trial_job_id, JSON.stringify(metrics));
        }
        const jobs = await ds.listTrialJobs();
        chai_1.expect(jobs.length).to.equals(2, 'There should be 2 jobs');
        const statistics = await ds.getTrialJobStatistics();
        chai_1.expect(statistics.length).to.equals(2, 'There should be 2 statistics');
    });
});
