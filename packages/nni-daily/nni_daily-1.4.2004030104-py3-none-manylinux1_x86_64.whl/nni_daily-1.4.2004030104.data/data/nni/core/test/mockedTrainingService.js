'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const ts_deferred_1 = require("ts-deferred");
const errors_1 = require("../../common/errors");
const trainingService_1 = require("../../common/trainingService");
const testTrainingServiceProvider = {
    get: () => { return new MockedTrainingService(); }
};
exports.testTrainingServiceProvider = testTrainingServiceProvider;
class MockedTrainingService extends trainingService_1.TrainingService {
    constructor() {
        super(...arguments);
        this.mockedMetaDataValue = "default";
        this.jobDetail1 = {
            id: '1234',
            status: 'SUCCEEDED',
            submitTime: Date.now(),
            startTime: Date.now(),
            endTime: Date.now(),
            tags: ['test'],
            url: 'http://test',
            workingDirectory: '/tmp/mocked',
            form: {
                sequenceId: 0,
                hyperParameters: { value: '', index: 0 }
            },
        };
        this.jobDetail2 = {
            id: '3456',
            status: 'SUCCEEDED',
            submitTime: Date.now(),
            startTime: Date.now(),
            endTime: Date.now(),
            tags: ['test'],
            url: 'http://test',
            workingDirectory: '/tmp/mocked',
            form: {
                sequenceId: 1,
                hyperParameters: { value: '', index: 1 }
            },
        };
    }
    listTrialJobs() {
        const deferred = new ts_deferred_1.Deferred();
        deferred.resolve([this.jobDetail1, this.jobDetail2]);
        return deferred.promise;
    }
    getTrialJob(trialJobId) {
        const deferred = new ts_deferred_1.Deferred();
        if (trialJobId === '1234') {
            deferred.resolve(this.jobDetail1);
        }
        else if (trialJobId === '3456') {
            deferred.resolve(this.jobDetail2);
        }
        else {
            deferred.reject();
        }
        return deferred.promise;
    }
    async run() {
    }
    addTrialJobMetricListener(listener) {
    }
    removeTrialJobMetricListener(listener) {
    }
    submitTrialJob(form) {
        const deferred = new ts_deferred_1.Deferred();
        return deferred.promise;
    }
    updateTrialJob(trialJobId, form) {
        throw new errors_1.MethodNotImplementedError();
    }
    get isMultiPhaseJobSupported() {
        return false;
    }
    cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const deferred = new ts_deferred_1.Deferred();
        if (trialJobId === '1234' || trialJobId === '3456') {
            deferred.resolve();
        }
        else {
            deferred.reject('job id error');
        }
        return deferred.promise;
    }
    setClusterMetadata(key, value) {
        const deferred = new ts_deferred_1.Deferred();
        if (key == 'mockedMetadataKey') {
            this.mockedMetaDataValue = value;
            deferred.resolve();
        }
        else {
            deferred.reject('key error');
        }
        return deferred.promise;
    }
    getClusterMetadata(key) {
        const deferred = new ts_deferred_1.Deferred();
        if (key == 'mockedMetadataKey') {
            deferred.resolve(this.mockedMetaDataValue);
        }
        else {
            deferred.reject('key error');
        }
        return deferred.promise;
    }
    cleanUp() {
        return Promise.resolve();
    }
}
exports.MockedTrainingService = MockedTrainingService;
