'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const ts_deferred_1 = require("ts-deferred");
const errors_1 = require("../../common/errors");
const manager_1 = require("../../common/manager");
exports.testManagerProvider = {
    get: () => { return new MockedNNIManager(); }
};
class MockedNNIManager extends manager_1.Manager {
    getStatus() {
        return {
            status: 'RUNNING',
            errors: []
        };
    }
    updateExperimentProfile(experimentProfile, updateType) {
        return Promise.resolve();
    }
    importData(data) {
        return Promise.resolve();
    }
    async exportData() {
        const ret = '';
        return Promise.resolve(ret);
    }
    getTrialJobStatistics() {
        const deferred = new ts_deferred_1.Deferred();
        deferred.resolve([{
                trialJobStatus: 'RUNNING',
                trialJobNumber: 2
            }, {
                trialJobStatus: 'FAILED',
                trialJobNumber: 1
            }]);
        return deferred.promise;
    }
    addCustomizedTrialJob(hyperParams) {
        return Promise.resolve(99);
    }
    resumeExperiment() {
        return Promise.resolve();
    }
    submitTrialJob(form) {
        const deferred = new ts_deferred_1.Deferred();
        const jobDetail = {
            id: '1234',
            status: 'RUNNING',
            submitTime: Date.now(),
            startTime: Date.now(),
            endTime: Date.now(),
            tags: ['test'],
            url: 'http://test',
            workingDirectory: '/tmp/mocked',
            form: {
                sequenceId: 0,
                hyperParameters: { value: '', index: 0 }
            }
        };
        deferred.resolve(jobDetail);
        return deferred.promise;
    }
    cancelTrialJobByUser(trialJobId) {
        return Promise.resolve();
    }
    getClusterMetadata(key) {
        return Promise.resolve('METAVALUE1');
    }
    startExperiment(experimentParams) {
        return Promise.resolve('id-1234');
    }
    setClusterMetadata(key, value) {
        return Promise.resolve();
    }
    getTrialJob(trialJobId) {
        const deferred = new ts_deferred_1.Deferred();
        const jobInfo = {
            id: '1234',
            status: 'SUCCEEDED',
            startTime: Date.now(),
            endTime: Date.now()
        };
        deferred.resolve(jobInfo);
        return deferred.promise;
    }
    stopExperiment() {
        throw new errors_1.MethodNotImplementedError();
    }
    getMetricData(trialJobId, metricType) {
        throw new errors_1.MethodNotImplementedError();
    }
    getMetricDataByRange(minSeqId, maxSeqId) {
        throw new errors_1.MethodNotImplementedError();
    }
    getLatestMetricData() {
        throw new errors_1.MethodNotImplementedError();
    }
    getExperimentProfile() {
        const profile = {
            params: {
                authorName: 'test',
                experimentName: 'exp1',
                trialConcurrency: 2,
                maxExecDuration: 30,
                maxTrialNum: 3,
                trainingServicePlatform: 'local',
                searchSpace: '{lr: 0.01}',
                tuner: {
                    className: 'testTuner',
                    checkpointDir: ''
                }
            },
            id: '2345',
            execDuration: 0,
            startTime: Date.now(),
            endTime: Date.now(),
            nextSequenceId: 0,
            revision: 0
        };
        return Promise.resolve(profile);
    }
    listTrialJobs(status) {
        const job1 = {
            id: '1234',
            status: 'SUCCEEDED',
            startTime: Date.now(),
            endTime: Date.now(),
            finalMetricData: [{
                    timestamp: 0,
                    trialJobId: '3456',
                    parameterId: '123',
                    type: 'FINAL',
                    sequence: 0,
                    data: '0.2'
                }]
        };
        const job2 = {
            id: '3456',
            status: 'FAILED',
            startTime: Date.now(),
            endTime: Date.now(),
            finalMetricData: [{
                    timestamp: 0,
                    trialJobId: '3456',
                    parameterId: '123',
                    type: 'FINAL',
                    sequence: 0,
                    data: '0.2'
                }]
        };
        return Promise.resolve([job1, job2]);
    }
}
exports.MockedNNIManager = MockedNNIManager;
