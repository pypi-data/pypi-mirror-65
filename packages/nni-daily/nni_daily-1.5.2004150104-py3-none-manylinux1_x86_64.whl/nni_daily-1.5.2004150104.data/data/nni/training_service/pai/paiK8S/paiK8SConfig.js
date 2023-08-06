'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const trialConfig_1 = require("../../common/trialConfig");
class NNIPAIK8STrialConfig extends trialConfig_1.TrialConfig {
    constructor(command, codeDir, gpuNum, cpuNum, memoryMB, image, nniManagerNFSMountPath, containerNFSMountPath, paiStoragePlugin, virtualCluster, paiConfigPath) {
        super(command, codeDir, gpuNum);
        this.cpuNum = cpuNum;
        this.memoryMB = memoryMB;
        this.image = image;
        this.virtualCluster = virtualCluster;
        this.nniManagerNFSMountPath = nniManagerNFSMountPath;
        this.containerNFSMountPath = containerNFSMountPath;
        this.paiStoragePlugin = paiStoragePlugin;
        this.paiConfigPath = paiConfigPath;
    }
}
exports.NNIPAIK8STrialConfig = NNIPAIK8STrialConfig;
