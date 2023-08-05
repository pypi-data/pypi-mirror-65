'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const ts_deferred_1 = require("ts-deferred");
const utils_1 = require("../../common/utils");
const CommandType = require("../commands");
const ipcInterface_1 = require("../ipcInterface");
let dispatcher;
let procExit = false;
let procError = false;
function startProcess() {
    const stdio = ['ignore', 'pipe', process.stderr, 'pipe', 'pipe'];
    const dispatcherCmd = utils_1.getMsgDispatcherCommand({
        experimentName: 'exp1',
        maxExecDuration: 3600,
        searchSpace: '',
        trainingServicePlatform: 'local',
        authorName: '',
        trialConcurrency: 1,
        maxTrialNum: 5,
        tuner: {
            className: 'DummyTuner',
            codeDir: './',
            classFileName: 'dummy_tuner.py',
            checkpointDir: './'
        },
        assessor: {
            className: 'DummyAssessor',
            codeDir: './',
            classFileName: 'dummy_assessor.py',
            checkpointDir: './'
        }
    });
    const proc = utils_1.getTunerProc(dispatcherCmd, stdio, 'core/test', process.env);
    proc.on('error', (error) => {
        procExit = true;
        procError = true;
    });
    proc.on('exit', (code) => {
        procExit = true;
        procError = (code !== 0);
    });
    dispatcher = ipcInterface_1.createDispatcherInterface(proc);
    dispatcher.onCommand((commandType, content) => {
        console.log(commandType, content);
    });
}
describe('core/ipcInterface.terminate', () => {
    before(() => {
        utils_1.prepareUnitTest();
        startProcess();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    it('normal', () => {
        dispatcher.sendCommand(CommandType.REPORT_METRIC_DATA, '{"trial_job_id":"A","type":"PERIODICAL","value":1,"sequence":123}');
        const deferred = new ts_deferred_1.Deferred();
        setTimeout(() => {
            assert.ok(!procExit);
            assert.ok(!procError);
            deferred.resolve();
        }, 1000);
        return deferred.promise;
    });
    it('terminate', () => {
        dispatcher.sendCommand(CommandType.TERMINATE);
        const deferred = new ts_deferred_1.Deferred();
        setTimeout(() => {
            assert.ok(procExit);
            assert.ok(!procError);
            deferred.resolve();
        }, 5000);
        return deferred.promise;
    });
});
