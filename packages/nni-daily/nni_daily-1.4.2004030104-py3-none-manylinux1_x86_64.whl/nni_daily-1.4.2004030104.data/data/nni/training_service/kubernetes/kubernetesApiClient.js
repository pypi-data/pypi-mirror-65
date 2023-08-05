'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const kubernetes_client_1 = require("kubernetes-client");
const log_1 = require("../../common/log");
class GeneralK8sClient {
    constructor() {
        this.log = log_1.getLogger();
        this.client = new kubernetes_client_1.Client1_10({ config: kubernetes_client_1.config.fromKubeconfig(), version: '1.9' });
        this.client.loadSpec();
    }
    async createSecret(secretManifest) {
        let result;
        const response = await this.client.api.v1.namespaces('default').secrets
            .post({ body: secretManifest });
        if (response.statusCode && (response.statusCode >= 200 && response.statusCode <= 299)) {
            result = Promise.resolve(true);
        }
        else {
            result = Promise.reject(`Create secrets failed, statusCode is ${response.statusCode}`);
        }
        return result;
    }
}
exports.GeneralK8sClient = GeneralK8sClient;
class KubernetesCRDClient {
    constructor() {
        this.log = log_1.getLogger();
        this.client = new kubernetes_client_1.Client1_10({ config: kubernetes_client_1.config.fromKubeconfig() });
        this.client.loadSpec();
    }
    get jobKind() {
        if (this.crdSchema
            && this.crdSchema.spec
            && this.crdSchema.spec.names
            && this.crdSchema.spec.names.kind) {
            return this.crdSchema.spec.names.kind;
        }
        else {
            throw new Error('KubeflowOperatorClient: getJobKind failed, kind is undefined in crd schema!');
        }
    }
    get apiVersion() {
        if (this.crdSchema
            && this.crdSchema.spec
            && this.crdSchema.spec.version) {
            return this.crdSchema.spec.version;
        }
        else {
            throw new Error('KubeflowOperatorClient: get apiVersion failed, version is undefined in crd schema!');
        }
    }
    async createKubernetesJob(jobManifest) {
        let result;
        const response = await this.operator.post({ body: jobManifest });
        if (response.statusCode && (response.statusCode >= 200 && response.statusCode <= 299)) {
            result = Promise.resolve(true);
        }
        else {
            result = Promise.reject(`Create kubernetes job failed, statusCode is ${response.statusCode}`);
        }
        return result;
    }
    async getKubernetesJob(kubeflowJobName) {
        let result;
        const response = await this.operator(kubeflowJobName)
            .get();
        if (response.statusCode && (response.statusCode >= 200 && response.statusCode <= 299)) {
            result = Promise.resolve(response.body);
        }
        else {
            result = Promise.reject(`KubeflowOperatorClient get tfjobs failed, statusCode is ${response.statusCode}`);
        }
        return result;
    }
    async deleteKubernetesJob(labels) {
        let result;
        const matchQuery = Array.from(labels.keys())
            .map((labelKey) => `${labelKey}=${labels.get(labelKey)}`)
            .join(',');
        try {
            const deleteResult = await this.operator()
                .delete({
                qs: {
                    labelSelector: matchQuery,
                    propagationPolicy: 'Background'
                }
            });
            if (deleteResult.statusCode && deleteResult.statusCode >= 200 && deleteResult.statusCode <= 299) {
                result = Promise.resolve(true);
            }
            else {
                result = Promise.reject(`KubeflowOperatorClient, delete labels ${matchQuery} get wrong statusCode ${deleteResult.statusCode}`);
            }
        }
        catch (err) {
            result = Promise.reject(err);
        }
        return result;
    }
}
exports.KubernetesCRDClient = KubernetesCRDClient;
