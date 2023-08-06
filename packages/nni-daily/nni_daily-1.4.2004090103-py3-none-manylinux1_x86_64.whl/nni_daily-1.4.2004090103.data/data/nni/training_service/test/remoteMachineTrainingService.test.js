'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const fs = require("fs");
const tmp = require("tmp");
const component = require("../../common/component");
const utils_1 = require("../../common/utils");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const remoteMachineTrainingService_1 = require("../remote_machine/remoteMachineTrainingService");
const localCodeDir = tmp.dirSync().name;
const mockedTrialPath = './training_service/test/mockedTrial.py';
fs.copyFileSync(mockedTrialPath, localCodeDir + '/mockedTrial.py');
describe('Unit Test for RemoteMachineTrainingService', () => {
    let skip = false;
    let testRmInfo;
    let machineList;
    try {
        testRmInfo = JSON.parse(fs.readFileSync('../../.vscode/rminfo.json', 'utf8'));
        console.log(testRmInfo);
        machineList = `[{\"ip\":\"${testRmInfo.ip}\",\"port\":22,\"username\":\"${testRmInfo.user}\",\"passwd\":\"${testRmInfo.password}\"}]`;
    }
    catch (err) {
        console.log('Please configure rminfo.json to enable remote machine unit test.');
        skip = true;
    }
    let remoteMachineTrainingService;
    before(() => {
        chai.should();
        chai.use(chaiAsPromised);
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    beforeEach(() => {
        if (skip) {
            return;
        }
        remoteMachineTrainingService = component.get(remoteMachineTrainingService_1.RemoteMachineTrainingService);
        remoteMachineTrainingService.run();
    });
    afterEach(() => {
        if (skip) {
            return;
        }
        remoteMachineTrainingService.cleanUp();
    });
    it('List trial jobs', async () => {
        if (skip) {
            return;
        }
        chai.expect(await remoteMachineTrainingService.listTrialJobs()).to.be.empty;
    });
    it('Set cluster metadata', async () => {
        if (skip) {
            return;
        }
        await remoteMachineTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.MACHINE_LIST, machineList);
        await remoteMachineTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, `{"command":"sleep 1h && echo ","codeDir":"${localCodeDir}","gpuNum":1}`);
        const form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        const trialJob = await remoteMachineTrainingService.submitTrialJob(form);
        await remoteMachineTrainingService.cancelTrialJob(trialJob.id);
        const trialJob2 = await remoteMachineTrainingService.getTrialJob(trialJob.id);
        chai.expect(trialJob2.status).to.be.equals('USER_CANCELED');
        await remoteMachineTrainingService.cancelTrialJob(trialJob.id + 'ddd').should.eventually.be.rejected;
    });
    it('Submit job test', async () => {
        if (skip) {
            return;
        }
    });
    it('Submit job and read metrics data', async () => {
        if (skip) {
            return;
        }
        await remoteMachineTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.MACHINE_LIST, machineList);
        const trialConfig = `{\"command\":\"python3 mockedTrial.py\", \"codeDir\":\"${localCodeDir}\",\"gpuNum\":0}`;
        await remoteMachineTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, trialConfig);
        const form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        const jobDetail = await remoteMachineTrainingService.submitTrialJob(form);
        const listener1 = function f1(metric) {
        };
        const listener2 = function f1(metric) {
        };
        remoteMachineTrainingService.addTrialJobMetricListener(listener1);
        remoteMachineTrainingService.addTrialJobMetricListener(listener2);
        await utils_1.delay(10000);
        remoteMachineTrainingService.removeTrialJobMetricListener(listener1);
        await utils_1.delay(5000);
    }).timeout(30000);
    it('Test getTrialJob exception', async () => {
        if (skip) {
            return;
        }
        await remoteMachineTrainingService.getTrialJob('wrongid').catch((err) => {
            assert(err !== undefined);
        });
    });
});
