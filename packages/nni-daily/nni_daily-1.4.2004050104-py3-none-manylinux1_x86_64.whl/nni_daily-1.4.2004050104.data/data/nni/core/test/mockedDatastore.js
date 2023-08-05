'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const console_1 = require("console");
const fs = require("fs");
const ts_deferred_1 = require("ts-deferred");
class SimpleDb {
    constructor(name, filename) {
        this.name = '';
        this.fileName = '';
        this.db = new Array();
        this.map = new Map();
        this.name = name;
        this.fileName = filename;
    }
    async saveData(data, key) {
        let index;
        if (key && this.map.has(key)) {
            index = this.map.get(key);
        }
        if (index === undefined) {
            index = this.db.push(data) - 1;
        }
        else {
            this.db[index] = data;
        }
        if (key) {
            this.map.set(key, index);
        }
        await this.persist();
    }
    listAllData() {
        const deferred = new ts_deferred_1.Deferred();
        deferred.resolve(this.db);
        return deferred.promise;
    }
    getData(key) {
        const deferred = new ts_deferred_1.Deferred();
        if (this.map.has(key)) {
            const index = this.map.get(key);
            if (index !== undefined && index >= 0) {
                deferred.resolve(this.db[index]);
            }
            else {
                deferred.reject(new Error(`Key or index not found: ${this.name}, ${key}`));
            }
        }
        else {
            console.log(`Key not found: ${this.name}, ${key}`);
            deferred.resolve(undefined);
        }
        return deferred.promise;
    }
    persist() {
        const deferred = new ts_deferred_1.Deferred();
        fs.writeFileSync(this.fileName, JSON.stringify({
            name: this.name,
            data: this.db,
            index: JSON.stringify([...this.map])
        }, null, 4));
        deferred.resolve();
        return deferred.promise;
    }
}
class MockedDataStore {
    constructor() {
        this.dbExpProfile = new SimpleDb('exp_profile', './exp_profile.json');
        this.dbTrialJobs = new SimpleDb('trial_jobs', './trial_jobs.json');
        this.dbMetrics = new SimpleDb('metrics', './metrics.json');
        this.trailJob1 = {
            event: 'ADD_CUSTOMIZED',
            timestamp: Date.now(),
            trialJobId: "4321",
            data: ''
        };
        this.metrics1 = {
            timestamp: Date.now(),
            trialJobId: '4321',
            parameterId: 'param1',
            type: 'CUSTOM',
            sequence: 21,
            data: ''
        };
    }
    init() {
        this.dbTrialJobs.saveData(this.trailJob1);
        this.dbMetrics.saveData(this.metrics1);
        return Promise.resolve();
    }
    close() {
        return Promise.resolve();
    }
    async storeExperimentProfile(experimentProfile) {
        await this.dbExpProfile.saveData(experimentProfile, experimentProfile.id);
    }
    async getExperimentProfile(experimentId) {
        return await this.dbExpProfile.getData(experimentId);
    }
    async storeTrialJobEvent(event, trialJobId, data) {
        const dataRecord = {
            event: event,
            timestamp: Date.now(),
            trialJobId: trialJobId,
            data: data
        };
        await this.dbTrialJobs.saveData(dataRecord);
    }
    async getTrialJobStatistics() {
        const result = [];
        const jobs = await this.listTrialJobs();
        const map = new Map();
        jobs.forEach((value) => {
            let n = map.get(value.status);
            if (!n) {
                n = 0;
            }
            map.set(value.status, n + 1);
        });
        map.forEach((value, key) => {
            const statistics = {
                trialJobStatus: key,
                trialJobNumber: value
            };
            result.push(statistics);
        });
        return result;
    }
    async listTrialJobs(status) {
        const trialJobEvents = await this.dbTrialJobs.listAllData();
        const map = this.getTrialJobsByReplayEvents(trialJobEvents);
        const result = [];
        for (let key of map.keys()) {
            const jobInfo = map.get(key);
            if (jobInfo === undefined) {
                continue;
            }
            if (!(status && jobInfo.status !== status)) {
                if (jobInfo.status === 'SUCCEEDED') {
                    jobInfo.finalMetricData = await this.getFinalMetricData(jobInfo.id);
                }
                result.push(jobInfo);
            }
        }
        return result;
    }
    async storeMetricData(trialJobId, data) {
        const metrics = JSON.parse(data);
        console_1.assert(trialJobId === metrics.trial_job_id);
        await this.dbMetrics.saveData({
            trialJobId: metrics.trial_job_id,
            parameterId: metrics.parameter_id,
            type: metrics.type,
            data: metrics.value,
            timestamp: Date.now()
        });
    }
    async getMetricData(trialJobId, metricType) {
        const result = [];
        const allMetrics = await this.dbMetrics.listAllData();
        allMetrics.forEach((value) => {
            const metrics = value;
            if (metrics.type === metricType && metrics.trialJobId === trialJobId) {
                result.push(metrics);
            }
        });
        return result;
    }
    async exportTrialHpConfigs() {
        const ret = '';
        return Promise.resolve(ret);
    }
    async getImportedData() {
        const ret = [];
        return Promise.resolve(ret);
    }
    getTrialJob(trialJobId) {
        return Promise.resolve({
            id: '1234',
            status: 'SUCCEEDED',
            startTime: Date.now(),
            endTime: Date.now()
        });
    }
    async getFinalMetricData(trialJobId) {
        const metrics = await this.getMetricData(trialJobId, "FINAL");
        console_1.assert(metrics.length <= 1);
        if (metrics.length == 1) {
            return metrics[0];
        }
        else {
            return undefined;
        }
    }
    getJobStatusByLatestEvent(event) {
        switch (event) {
            case 'USER_TO_CANCEL':
                return 'USER_CANCELED';
            case 'ADD_CUSTOMIZED':
                return 'WAITING';
        }
        return event;
    }
    getTrialJobsByReplayEvents(trialJobEvents) {
        const map = new Map();
        for (let record of trialJobEvents) {
            let jobInfo;
            if (map.has(record.trialJobId)) {
                jobInfo = map.get(record.trialJobId);
            }
            else {
                jobInfo = {
                    id: record.trialJobId,
                    status: this.getJobStatusByLatestEvent(record.event),
                };
            }
            if (!jobInfo) {
                throw new Error('Empty JobInfo');
            }
            switch (record.event) {
                case 'RUNNING':
                    jobInfo.startTime = Date.now();
                    break;
                case 'SUCCEEDED':
                case 'FAILED':
                case 'USER_CANCELED':
                case 'SYS_CANCELED':
                case 'EARLY_STOPPED':
                    jobInfo.endTime = Date.now();
            }
            jobInfo.status = this.getJobStatusByLatestEvent(record.event);
            map.set(record.trialJobId, jobInfo);
        }
        return map;
    }
}
exports.MockedDataStore = MockedDataStore;
