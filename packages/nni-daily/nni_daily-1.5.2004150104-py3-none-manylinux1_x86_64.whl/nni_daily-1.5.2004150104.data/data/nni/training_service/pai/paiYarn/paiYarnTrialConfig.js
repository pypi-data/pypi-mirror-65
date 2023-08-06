'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const trialConfig_1 = require("../../common/trialConfig");
class PAIYarnTrialConfig extends trialConfig_1.TrialConfig {
    constructor(command, codeDir, gpuNum, cpuNum, memoryMB, image, dataDir, outputDir) {
        super(command, codeDir, gpuNum);
        this.cpuNum = cpuNum;
        this.memoryMB = memoryMB;
        this.image = image;
        this.dataDir = dataDir;
        this.outputDir = outputDir;
    }
}
exports.PAIYarnTrialConfig = PAIYarnTrialConfig;
