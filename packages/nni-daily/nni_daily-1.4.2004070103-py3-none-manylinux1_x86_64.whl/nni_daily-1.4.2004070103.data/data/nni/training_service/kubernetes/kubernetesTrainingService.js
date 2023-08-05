'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const path = require("path");
const azureStorage = require("azure-storage");
const events_1 = require("events");
const js_base64_1 = require("js-base64");
const typescript_string_operations_1 = require("typescript-string-operations");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
const azureStorageClientUtils_1 = require("./azureStorageClientUtils");
const kubernetesApiClient_1 = require("./kubernetesApiClient");
const kubernetesData_1 = require("./kubernetesData");
const fs = require('fs');
class KubernetesTrainingService {
    constructor() {
        this.NNI_KUBERNETES_TRIAL_LABEL = 'nni-kubernetes-trial';
        this.stopping = false;
        this.versionCheck = true;
        this.log = log_1.getLogger();
        this.metricsEmitter = new events_1.EventEmitter();
        this.trialJobsMap = new Map();
        this.trialLocalNFSTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-nfs-tmp');
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.CONTAINER_MOUNT_PATH = '/tmp/mount';
        this.genericK8sClient = new kubernetesApiClient_1.GeneralK8sClient();
        this.logCollection = 'none';
    }
    generatePodResource(memory, cpuNum, gpuNum) {
        const resources = {
            memory: `${memory}Mi`,
            cpu: `${cpuNum}`
        };
        if (gpuNum !== 0) {
            resources['nvidia.com/gpu'] = `${gpuNum}`;
        }
        return resources;
    }
    async listTrialJobs() {
        const jobs = [];
        for (const [key, value] of this.trialJobsMap) {
            jobs.push(await this.getTrialJob(key));
        }
        return Promise.resolve(jobs);
    }
    async getTrialJob(trialJobId) {
        const kubernetesTrialJob = this.trialJobsMap.get(trialJobId);
        if (kubernetesTrialJob === undefined) {
            return Promise.reject(`trial job ${trialJobId} not found`);
        }
        return Promise.resolve(kubernetesTrialJob);
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    get isMultiPhaseJobSupported() {
        return false;
    }
    getClusterMetadata(key) {
        return Promise.resolve('');
    }
    get MetricsEmitter() {
        return this.metricsEmitter;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            const errorMessage = `CancelTrialJob: trial job id ${trialJobId} not found`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        if (this.kubernetesCRDClient === undefined) {
            const errorMessage = `CancelTrialJob: trial job id ${trialJobId} failed because operatorClient is undefined`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        try {
            await this.kubernetesCRDClient.deleteKubernetesJob(new Map([
                ['app', this.NNI_KUBERNETES_TRIAL_LABEL],
                ['expId', experimentStartupInfo_1.getExperimentId()],
                ['trialId', trialJobId]
            ]));
        }
        catch (err) {
            const errorMessage = `Delete trial ${trialJobId} failed: ${err}`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        trialJobDetail.endTime = Date.now();
        trialJobDetail.status = utils_1.getJobCancelStatus(isEarlyStopped);
        return Promise.resolve();
    }
    async cleanUp() {
        this.stopping = true;
        for (const [trialJobId, kubernetesTrialJob] of this.trialJobsMap) {
            if (['RUNNING', 'WAITING', 'UNKNOWN'].includes(kubernetesTrialJob.status)) {
                try {
                    await this.cancelTrialJob(trialJobId);
                }
                catch (error) {
                }
                kubernetesTrialJob.status = 'SYS_CANCELED';
            }
        }
        try {
            if (this.kubernetesCRDClient !== undefined) {
                await this.kubernetesCRDClient.deleteKubernetesJob(new Map([
                    ['app', this.NNI_KUBERNETES_TRIAL_LABEL],
                    ['expId', experimentStartupInfo_1.getExperimentId()]
                ]));
            }
        }
        catch (error) {
            this.log.error(`Delete kubernetes job with label: app=${this.NNI_KUBERNETES_TRIAL_LABEL},\
            expId=${experimentStartupInfo_1.getExperimentId()} failed, error is ${error}`);
        }
        try {
            await cpp.exec(`sudo umount ${this.trialLocalNFSTempFolder}`);
        }
        catch (error) {
            this.log.error(`Unmount ${this.trialLocalNFSTempFolder} failed, error is ${error}`);
        }
        if (this.kubernetesJobRestServer === undefined) {
            throw new Error('kubernetesJobRestServer not initialized!');
        }
        try {
            await this.kubernetesJobRestServer.stop();
            this.log.info('Kubernetes Training service rest server stopped successfully.');
        }
        catch (error) {
            this.log.error(`Kubernetes Training service rest server stopped failed, error: ${error.message}`);
            return Promise.reject(error);
        }
        return Promise.resolve();
    }
    async createAzureStorage(vaultName, valutKeyName) {
        try {
            const result = await cpp.exec(`az keyvault secret show --name ${valutKeyName} --vault-name ${vaultName}`);
            if (result.stderr) {
                const errorMessage = result.stderr;
                this.log.error(errorMessage);
                return Promise.reject(errorMessage);
            }
            const storageAccountKey = JSON.parse(result.stdout).value;
            if (this.azureStorageAccountName === undefined) {
                throw new Error('azureStorageAccountName not initialized!');
            }
            this.azureStorageClient = azureStorage.createFileService(this.azureStorageAccountName, storageAccountKey);
            await azureStorageClientUtils_1.AzureStorageClientUtility.createShare(this.azureStorageClient, this.azureStorageShare);
            this.azureStorageSecretName = typescript_string_operations_1.String.Format('nni-secret-{0}', utils_1.uniqueString(8)
                .toLowerCase());
            await this.genericK8sClient.createSecret({
                apiVersion: 'v1',
                kind: 'Secret',
                metadata: {
                    name: this.azureStorageSecretName,
                    namespace: 'default',
                    labels: {
                        app: this.NNI_KUBERNETES_TRIAL_LABEL,
                        expId: experimentStartupInfo_1.getExperimentId()
                    }
                },
                type: 'Opaque',
                data: {
                    azurestorageaccountname: js_base64_1.Base64.encode(this.azureStorageAccountName),
                    azurestorageaccountkey: js_base64_1.Base64.encode(storageAccountKey)
                }
            });
        }
        catch (error) {
            this.log.error(error);
            return Promise.reject(error);
        }
        return Promise.resolve();
    }
    async generateRunScript(platform, trialJobId, trialWorkingFolder, command, trialSequenceId, roleName, gpuNum) {
        let nvidiaScript = '';
        if (gpuNum === 0) {
            nvidiaScript = 'export CUDA_VISIBLE_DEVICES=';
        }
        const nniManagerIp = this.nniManagerIpConfig ? this.nniManagerIpConfig.nniManagerIp : utils_1.getIPV4Address();
        const version = this.versionCheck ? await utils_1.getVersion() : '';
        const runScript = typescript_string_operations_1.String.Format(kubernetesData_1.kubernetesScriptFormat, platform, trialJobId, path.join(trialWorkingFolder, 'output', `${roleName}_output`), trialJobId, experimentStartupInfo_1.getExperimentId(), trialWorkingFolder, trialSequenceId, nvidiaScript, command, nniManagerIp, this.kubernetesRestServerPort, version, this.logCollection);
        return Promise.resolve(runScript);
    }
    async createNFSStorage(nfsServer, nfsPath) {
        await cpp.exec(`mkdir -p ${this.trialLocalNFSTempFolder}`);
        try {
            await cpp.exec(`sudo mount ${nfsServer}:${nfsPath} ${this.trialLocalNFSTempFolder}`);
        }
        catch (error) {
            const mountError = `Mount NFS ${nfsServer}:${nfsPath} to ${this.trialLocalNFSTempFolder} failed, error is ${error}`;
            this.log.error(mountError);
            return Promise.reject(mountError);
        }
        return Promise.resolve();
    }
    async createRegistrySecret(filePath) {
        if (filePath === undefined || filePath === '') {
            return undefined;
        }
        const body = fs.readFileSync(filePath).toString('base64');
        const registrySecretName = typescript_string_operations_1.String.Format('nni-secret-{0}', utils_1.uniqueString(8)
            .toLowerCase());
        await this.genericK8sClient.createSecret({
            apiVersion: 'v1',
            kind: 'Secret',
            metadata: {
                name: registrySecretName,
                namespace: 'default',
                labels: {
                    app: this.NNI_KUBERNETES_TRIAL_LABEL,
                    expId: experimentStartupInfo_1.getExperimentId()
                }
            },
            type: 'kubernetes.io/dockerconfigjson',
            data: {
                '.dockerconfigjson': body
            }
        });
        return registrySecretName;
    }
    async uploadFilesToAzureStorage(trialJobId, trialLocalTempFolder, codeDir, uploadRetryCount) {
        if (this.azureStorageClient === undefined) {
            throw new Error('azureStorageClient is not initialized');
        }
        let trialJobOutputUrl = '';
        let retryCount = 1;
        if (uploadRetryCount) {
            retryCount = uploadRetryCount;
        }
        let resultUploadNNIScript = false;
        let resultUploadCodeFile = false;
        try {
            do {
                if (!resultUploadNNIScript) {
                    resultUploadNNIScript = await azureStorageClientUtils_1.AzureStorageClientUtility.uploadDirectory(this.azureStorageClient, `nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`, this.azureStorageShare, `${trialLocalTempFolder}`);
                }
                if (!resultUploadCodeFile) {
                    resultUploadCodeFile = await azureStorageClientUtils_1.AzureStorageClientUtility.uploadDirectory(this.azureStorageClient, `nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`, this.azureStorageShare, `${codeDir}`);
                }
                if (resultUploadNNIScript && resultUploadCodeFile) {
                    trialJobOutputUrl = `https://${this.azureStorageAccountName}.file.core.windows.net/${this.azureStorageShare}` +
                        `/${path.join('nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
                    break;
                }
                else {
                    await utils_1.delay(5000);
                    this.log.info('Upload failed, Retry: upload files to azure-storage');
                }
            } while (retryCount-- >= 0);
        }
        catch (error) {
            this.log.error(error);
            return Promise.resolve("");
        }
        if (!trialJobOutputUrl) {
            this.log.info(`Retry-count is used up, upload files to azureStorage for trial ${trialJobId} failed!`);
        }
        return Promise.resolve(trialJobOutputUrl);
    }
}
exports.KubernetesTrainingService = KubernetesTrainingService;
