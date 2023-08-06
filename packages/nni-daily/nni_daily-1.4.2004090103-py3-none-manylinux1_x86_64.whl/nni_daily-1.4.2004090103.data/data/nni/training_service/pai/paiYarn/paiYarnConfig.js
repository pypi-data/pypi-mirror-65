'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const trialConfig_1 = require("../../common/trialConfig");
class PAITaskRole {
    constructor(name, taskNumber, cpuNumber, memoryMB, gpuNumber, command, shmMB, portList) {
        this.name = name;
        this.taskNumber = taskNumber;
        this.cpuNumber = cpuNumber;
        this.memoryMB = memoryMB;
        this.gpuNumber = gpuNumber;
        this.command = command;
        this.shmMB = shmMB;
        this.portList = portList;
    }
}
exports.PAITaskRole = PAITaskRole;
class PAIJobConfig {
    constructor(jobName, image, codeDir, taskRoles, virtualCluster, authFile) {
        this.jobName = jobName;
        this.image = image;
        this.codeDir = codeDir;
        this.taskRoles = taskRoles;
        this.virtualCluster = virtualCluster;
        this.authFile = authFile;
    }
}
exports.PAIJobConfig = PAIJobConfig;
class PortListMetaData {
    constructor() {
        this.label = '';
        this.beginAt = 0;
        this.portNumber = 0;
    }
}
exports.PortListMetaData = PortListMetaData;
class NNIPAITrialConfig extends trialConfig_1.TrialConfig {
    constructor(command, codeDir, gpuNum, cpuNum, memoryMB, image, virtualCluster, shmMB, authFile, portList) {
        super(command, codeDir, gpuNum);
        this.cpuNum = cpuNum;
        this.memoryMB = memoryMB;
        this.image = image;
        this.virtualCluster = virtualCluster;
        this.shmMB = shmMB;
        this.authFile = authFile;
        this.portList = portList;
    }
}
exports.NNIPAITrialConfig = NNIPAITrialConfig;
