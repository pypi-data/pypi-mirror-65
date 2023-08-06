'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const errors_1 = require("../../common/errors");
const log_1 = require("../../common/log");
class KubernetesJobInfoCollector {
    constructor(jobMap) {
        this.log = log_1.getLogger();
        this.trialJobsMap = jobMap;
        this.statusesNeedToCheck = ['RUNNING', 'WAITING'];
    }
    async retrieveTrialStatus(kubernetesCRDClient) {
        assert(kubernetesCRDClient !== undefined);
        const updateKubernetesTrialJobs = [];
        for (const [trialJobId, kubernetesTrialJob] of this.trialJobsMap) {
            if (kubernetesTrialJob === undefined) {
                throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `trial job id ${trialJobId} not found`);
            }
            if (Date.now() - kubernetesTrialJob.submitTime < 20 * 1000) {
                return Promise.resolve();
            }
            updateKubernetesTrialJobs.push(this.retrieveSingleTrialJobInfo(kubernetesCRDClient, kubernetesTrialJob));
        }
        await Promise.all(updateKubernetesTrialJobs);
    }
    async retrieveSingleTrialJobInfo(kubernetesCRDClient, kubernetesTrialJob) {
        throw new errors_1.MethodNotImplementedError();
    }
}
exports.KubernetesJobInfoCollector = KubernetesJobInfoCollector;
