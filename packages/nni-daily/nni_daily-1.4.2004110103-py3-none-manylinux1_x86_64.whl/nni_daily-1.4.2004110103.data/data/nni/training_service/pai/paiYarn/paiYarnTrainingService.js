"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var PAIYarnTrainingService_1;
Object.defineProperty(exports, "__esModule", { value: true });
'use strict';
const fs = require("fs");
const path = require("path");
const request = require("request");
const component = require("../../../common/component");
const ts_deferred_1 = require("ts-deferred");
const typescript_string_operations_1 = require("typescript-string-operations");
const utils_1 = require("../../../common/utils");
const containerJobData_1 = require("../../common/containerJobData");
const trialConfigMetadataKey_1 = require("../../common/trialConfigMetadataKey");
const util_1 = require("../../common/util");
const hdfsClientUtility_1 = require("./hdfsClientUtility");
const paiYarnConfig_1 = require("./paiYarnConfig");
const paiYarnData_1 = require("./paiYarnData");
const paiTrainingService_1 = require("../paiTrainingService");
const paiConfig_1 = require("../paiConfig");
const WebHDFS = require("webhdfs");
const paiJobRestServer_1 = require("../paiJobRestServer");
let PAIYarnTrainingService = PAIYarnTrainingService_1 = class PAIYarnTrainingService extends paiTrainingService_1.PAITrainingService {
    constructor() {
        super();
    }
    async submitTrialJob(form) {
        if (this.paiClusterConfig === undefined) {
            throw new Error(`paiBaseClusterConfig not initialized!`);
        }
        this.log.info(`submitTrialJob: form: ${JSON.stringify(form)}`);
        const trialJobId = utils_1.uniqueString(5);
        const trialWorkingFolder = path.join(this.expRootDir, 'trials', trialJobId);
        const paiJobName = `nni_exp_${this.experimentId}_trial_${trialJobId}`;
        const hdfsCodeDir = hdfsClientUtility_1.HDFSClientUtility.getHdfsTrialWorkDir(this.paiClusterConfig.userName, trialJobId);
        const hdfsOutputDir = utils_1.unixPathJoin(hdfsCodeDir, 'nnioutput');
        const hdfsLogPath = typescript_string_operations_1.String.Format(paiYarnData_1.PAI_LOG_PATH_FORMAT, this.paiClusterConfig.host, hdfsOutputDir);
        const trialJobDetail = new paiConfig_1.PAITrialJobDetail(trialJobId, 'WAITING', paiJobName, Date.now(), trialWorkingFolder, form, hdfsLogPath);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        this.jobQueue.push(trialJobId);
        return trialJobDetail;
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIpConfig = JSON.parse(value);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.PAI_YARN_CLUSTER_CONFIG:
                this.paiJobRestServer = new paiJobRestServer_1.PAIJobRestServer(component.get(PAIYarnTrainingService_1));
                this.paiClusterConfig = JSON.parse(value);
                this.paiClusterConfig.host = this.formatPAIHost(this.paiClusterConfig.host);
                this.hdfsClient = WebHDFS.createClient({
                    user: this.paiClusterConfig.userName,
                    port: 80,
                    path: '/webhdfs/api/v1',
                    host: this.paiClusterConfig.host
                });
                this.paiClusterConfig.host = this.formatPAIHost(this.paiClusterConfig.host);
                if (this.paiClusterConfig.passWord) {
                    await this.updatePaiToken();
                }
                else if (this.paiClusterConfig.token) {
                    this.paiToken = this.paiClusterConfig.token;
                }
                else {
                    throw new Error('pai cluster config format error, please set password or token!');
                }
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                if (this.paiClusterConfig === undefined) {
                    this.log.error('pai cluster config is not initialized');
                    break;
                }
                this.paiTrialConfig = JSON.parse(value);
                await util_1.validateCodeDir(this.paiTrialConfig.codeDir);
                this.copyExpCodeDirPromise = hdfsClientUtility_1.HDFSClientUtility.copyDirectoryToHdfs(this.paiTrialConfig.codeDir, hdfsClientUtility_1.HDFSClientUtility.getHdfsExpCodeDir(this.paiClusterConfig.userName), this.hdfsClient);
                if (this.paiTrialConfig.authFile) {
                    this.authFileHdfsPath = utils_1.unixPathJoin(hdfsClientUtility_1.HDFSClientUtility.hdfsExpRootDir(this.paiClusterConfig.userName), 'authFile');
                    this.copyAuthFilePromise = hdfsClientUtility_1.HDFSClientUtility.copyFileToHdfs(this.paiTrialConfig.authFile, this.authFileHdfsPath, this.hdfsClient);
                }
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.VERSION_CHECK:
                this.versionCheck = (value === 'true' || value === 'True');
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.LOG_COLLECTION:
                this.logCollection = value;
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.MULTI_PHASE:
                this.isMultiPhase = (value === 'true' || value === 'True');
                break;
            default:
                throw new Error(`Uknown key: ${key}`);
        }
    }
    async submitTrialJobToPAI(trialJobId) {
        const deferred = new ts_deferred_1.Deferred();
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`Failed to find PAITrialJobDetail for job ${trialJobId}`);
        }
        if (this.paiClusterConfig === undefined) {
            throw new Error('PAI Cluster config is not initialized');
        }
        if (this.paiTrialConfig === undefined) {
            throw new Error('trial config is not initialized');
        }
        if (this.paiToken === undefined) {
            throw new Error('PAI token is not initialized');
        }
        if (this.paiJobRestServer === undefined) {
            throw new Error('paiJobRestServer is not initialized');
        }
        this.paiRestServerPort = this.paiJobRestServer.clusterRestServerPort;
        if (this.copyExpCodeDirPromise !== undefined) {
            await this.copyExpCodeDirPromise;
        }
        if (this.paiTrialConfig.authFile) {
            await this.copyAuthFilePromise;
        }
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        await util_1.execMkdir(trialLocalTempFolder);
        const runScriptContent = containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT;
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'install_nni.sh'), runScriptContent, { encoding: 'utf8' });
        if (trialJobDetail.form !== undefined) {
            await fs.promises.writeFile(path.join(trialLocalTempFolder, utils_1.generateParamFileName(trialJobDetail.form.hyperParameters)), trialJobDetail.form.hyperParameters.value, { encoding: 'utf8' });
        }
        const hdfsCodeDir = hdfsClientUtility_1.HDFSClientUtility.getHdfsTrialWorkDir(this.paiClusterConfig.userName, trialJobId);
        const hdfsOutputDir = utils_1.unixPathJoin(hdfsCodeDir, 'nnioutput');
        const nniManagerIp = this.nniManagerIpConfig ? this.nniManagerIpConfig.nniManagerIp : utils_1.getIPV4Address();
        const version = this.versionCheck ? await utils_1.getVersion() : '';
        const nniPaiTrialCommand = typescript_string_operations_1.String.Format(paiYarnData_1.PAI_TRIAL_COMMAND_FORMAT, `$PWD/${trialJobId}`, `$PWD/${trialJobId}/nnioutput`, trialJobId, this.experimentId, trialJobDetail.form.sequenceId, this.isMultiPhase, this.paiTrialConfig.command, nniManagerIp, this.paiRestServerPort, hdfsOutputDir, this.paiClusterConfig.host, this.paiClusterConfig.userName, hdfsClientUtility_1.HDFSClientUtility.getHdfsExpCodeDir(this.paiClusterConfig.userName), version, this.logCollection)
            .replace(/\r\n|\n|\r/gm, '');
        this.log.info(`nniPAItrial command is ${nniPaiTrialCommand.trim()}`);
        const paiTaskRoles = [
            new paiYarnConfig_1.PAITaskRole(`nni_trail_${trialJobId}`, 1, this.paiTrialConfig.cpuNum, this.paiTrialConfig.memoryMB, this.paiTrialConfig.gpuNum, nniPaiTrialCommand, this.paiTrialConfig.shmMB, this.paiTrialConfig.portList)
        ];
        const paiJobConfig = new paiYarnConfig_1.PAIJobConfig(trialJobDetail.paiJobName, this.paiTrialConfig.image, `$PAI_DEFAULT_FS_URI${hdfsCodeDir}`, paiTaskRoles, this.paiTrialConfig.virtualCluster === undefined ? 'default' : this.paiTrialConfig.virtualCluster.toString(), this.authFileHdfsPath);
        try {
            await hdfsClientUtility_1.HDFSClientUtility.copyDirectoryToHdfs(trialLocalTempFolder, hdfsCodeDir, this.hdfsClient);
        }
        catch (error) {
            this.log.error(`PAI Training service: copy ${this.paiTrialConfig.codeDir} to HDFS ${hdfsCodeDir} failed, error is ${error}`);
            trialJobDetail.status = 'FAILED';
            return true;
        }
        const submitJobRequest = {
            uri: `${this.protocol}://${this.paiClusterConfig.host}/rest-server/api/v1/user/${this.paiClusterConfig.userName}/jobs`,
            method: 'POST',
            json: true,
            body: paiJobConfig,
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.paiToken}`
            }
        };
        request(submitJobRequest, (error, response, body) => {
            if ((error !== undefined && error !== null) || response.statusCode >= 400) {
                const errorMessage = (error !== undefined && error !== null) ? error.message :
                    `Submit trial ${trialJobId} failed, http code:${response.statusCode}, http body: ${response.body.message}`;
                trialJobDetail.status = 'FAILED';
                deferred.resolve(true);
            }
            else {
                trialJobDetail.submitTime = Date.now();
                deferred.resolve(true);
            }
        });
        return deferred.promise;
    }
    async updateTrialJob(trialJobId, form) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`updateTrialJob failed: ${trialJobId} not found`);
        }
        await this.writeParameterFile(trialJobId, form.hyperParameters);
        return trialJobDetail;
    }
    async writeParameterFile(trialJobId, hyperParameters) {
        if (this.paiClusterConfig === undefined) {
            throw new Error('PAI Cluster config is not initialized');
        }
        if (this.paiTrialConfig === undefined) {
            throw new Error('PAI trial config is not initialized');
        }
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        const hpFileName = utils_1.generateParamFileName(hyperParameters);
        const localFilepath = path.join(trialLocalTempFolder, hpFileName);
        await fs.promises.writeFile(localFilepath, hyperParameters.value, { encoding: 'utf8' });
        const hdfsCodeDir = hdfsClientUtility_1.HDFSClientUtility.getHdfsTrialWorkDir(this.paiClusterConfig.userName, trialJobId);
        const hdfsHpFilePath = path.join(hdfsCodeDir, hpFileName);
        await hdfsClientUtility_1.HDFSClientUtility.copyFileToHdfs(localFilepath, hdfsHpFilePath, this.hdfsClient);
        await this.postParameterFileMeta({
            experimentId: this.experimentId,
            trialId: trialJobId,
            filePath: hdfsHpFilePath
        });
    }
    postParameterFileMeta(parameterFileMeta) {
        const deferred = new ts_deferred_1.Deferred();
        if (this.paiJobRestServer === undefined) {
            throw new Error('paiJobRestServer not implemented!');
        }
        const req = {
            uri: `${this.paiJobRestServer.endPoint}${this.paiJobRestServer.apiRootUrl}/parameter-file-meta`,
            method: 'POST',
            json: true,
            body: parameterFileMeta
        };
        request(req, (err, res) => {
            if (err) {
                deferred.reject(err);
            }
            else {
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
};
PAIYarnTrainingService = PAIYarnTrainingService_1 = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], PAIYarnTrainingService);
exports.PAIYarnTrainingService = PAIYarnTrainingService;
