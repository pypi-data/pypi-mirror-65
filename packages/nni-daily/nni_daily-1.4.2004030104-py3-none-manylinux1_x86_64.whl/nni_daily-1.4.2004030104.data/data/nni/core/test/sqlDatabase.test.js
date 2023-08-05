'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const utils_1 = require("../../common/utils");
const sqlDatabase_1 = require("../sqlDatabase");
const expParams1 = {
    authorName: 'ZhangSan',
    experimentName: 'Exp1',
    trialConcurrency: 3,
    maxExecDuration: 100,
    maxTrialNum: 5,
    trainingServicePlatform: 'local',
    searchSpace: 'SS',
    tuner: {
        className: 'testTuner',
        checkpointDir: '/tmp'
    }
};
const expParams2 = {
    authorName: 'LiSi',
    experimentName: 'Exp2',
    trialConcurrency: 5,
    maxExecDuration: 1000,
    maxTrialNum: 5,
    trainingServicePlatform: 'local',
    searchSpace: '',
    tuner: {
        className: 'testTuner',
        checkpointDir: '/tmp'
    },
    assessor: {
        className: 'testAssessor',
        checkpointDir: '/tmp'
    }
};
const profiles = [
    { params: expParams1, id: '#1', execDuration: 0, logDir: '/log', startTime: Date.now(), endTime: undefined, nextSequenceId: 0, revision: 1, },
    { params: expParams1, id: '#1', execDuration: 0, logDir: '/log', startTime: Date.now(), endTime: Date.now(), nextSequenceId: 1, revision: 2 },
    { params: expParams2, id: '#2', execDuration: 0, logDir: '/log', startTime: Date.now(), endTime: Date.now(), nextSequenceId: 0, revision: 2 },
    { params: expParams2, id: '#2', execDuration: 0, logDir: '/log', startTime: Date.now(), endTime: Date.now(), nextSequenceId: 2, revision: 3 }
];
const events = [
    { timestamp: Date.now(), event: 'WAITING', trialJobId: 'A', data: 'hello' },
    { timestamp: Date.now(), event: 'UNKNOWN', trialJobId: 'B', data: 'world' },
    { timestamp: Date.now(), event: 'RUNNING', trialJobId: 'B', data: undefined },
    { timestamp: Date.now(), event: 'RUNNING', trialJobId: 'A', data: '123' },
    { timestamp: Date.now(), event: 'FAILED', trialJobId: 'A', data: undefined }
];
const metrics = [
    { timestamp: Date.now(), trialJobId: 'A', parameterId: '1', type: 'PERIODICAL', sequence: 0, data: 1.1 },
    { timestamp: Date.now(), trialJobId: 'B', parameterId: '2', type: 'PERIODICAL', sequence: 0, data: 2.1 },
    { timestamp: Date.now(), trialJobId: 'A', parameterId: '1', type: 'PERIODICAL', sequence: 1, data: 1.2 },
    { timestamp: Date.now(), trialJobId: 'A', parameterId: '1', type: 'FINAL', sequence: 0, data: 1.3 },
    { timestamp: Date.now(), trialJobId: 'C', parameterId: '2', type: 'PERIODICAL', sequence: 1, data: 2.1 },
    { timestamp: Date.now(), trialJobId: 'C', parameterId: '2', type: 'FINAL', sequence: 0, data: 2.2 }
];
function assertRecordEqual(record, value) {
    assert.ok(record.timestamp > new Date(2018, 6, 1).getTime());
    assert.ok(record.timestamp < Date.now());
    for (const key in value) {
        if (key !== 'timestamp') {
            assert.equal(record[key], value[key]);
        }
    }
}
function assertRecordsEqual(records, inputs, indices) {
    assert.equal(records.length, indices.length);
    for (let i = 0; i < records.length; i++) {
        assertRecordEqual(records[i], inputs[indices[i]]);
    }
}
describe('core/sqlDatabase', () => {
    let db;
    before(async () => {
        utils_1.prepareUnitTest();
        const dbDir = utils_1.getDefaultDatabaseDir();
        await utils_1.mkDirP(dbDir);
        db = new sqlDatabase_1.SqlDB();
        await db.init(true, dbDir);
        for (const profile of profiles) {
            await db.storeExperimentProfile(profile);
        }
        for (const event of events) {
            await db.storeTrialJobEvent(event.event, event.trialJobId, Date.now(), event.data);
        }
        for (const metric of metrics) {
            await db.storeMetricData(metric.trialJobId, JSON.stringify(metric));
        }
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    it('queryExperimentProfile without revision', async () => {
        const records = await db.queryExperimentProfile('#1');
        assert.equal(records.length, 2);
        assert.deepEqual(records[0], profiles[1]);
        assert.deepEqual(records[1], profiles[0]);
    });
    it('queryExperimentProfile with revision', async () => {
        const records = await db.queryExperimentProfile('#1', 2);
        assert.equal(records.length, 1);
        assert.deepEqual(records[0], profiles[1]);
    });
    it('queryLatestExperimentProfile', async () => {
        const record = await db.queryLatestExperimentProfile('#2');
        assert.deepEqual(record, profiles[3]);
    });
    it('queryTrialJobEventByEvent without trialJobId', async () => {
        const records = await db.queryTrialJobEvent(undefined, 'RUNNING');
        assertRecordsEqual(records, events, [2, 3]);
    });
    it('queryTrialJobEventByEvent with trialJobId', async () => {
        const records = await db.queryTrialJobEvent('A', 'RUNNING');
        assertRecordsEqual(records, events, [3]);
    });
    it('queryTrialJobEventById', async () => {
        const records = await db.queryTrialJobEvent('B');
        assertRecordsEqual(records, events, [1, 2]);
    });
    it('queryMetricDataByType without trialJobId', async () => {
        const records = await db.queryMetricData(undefined, 'FINAL');
        assertRecordsEqual(records, metrics, [3, 5]);
    });
    it('queryMetricDataByType with trialJobId', async () => {
        const records = await db.queryMetricData('A', 'PERIODICAL');
        assertRecordsEqual(records, metrics, [0, 2]);
    });
    it('queryMetricDataById', async () => {
        const records = await db.queryMetricData('B');
        assertRecordsEqual(records, metrics, [1]);
    });
    it('empty result', async () => {
        const records = await db.queryMetricData('X');
        assert.equal(records.length, 0);
    });
});
