'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const fs = require("fs");
const tmp = require("tmp");
const component = require("../../common/component");
const utils_1 = require("../../common/utils");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const paiYarnTrainingService_1 = require("../pai/paiYarn/paiYarnTrainingService");
const localCodeDir = tmp.dirSync().name;
const mockedTrialPath = './training_service/test/mockedTrial.py';
fs.copyFileSync(mockedTrialPath, localCodeDir + '/mockedTrial.py');
describe('Unit Test for PAIYarnTrainingService', () => {
    let skip = false;
    let testPaiClusterInfo;
    let paiCluster;
    let paiTrialConfig;
    try {
        testPaiClusterInfo = JSON.parse(fs.readFileSync('../../.vscode/paiCluster.json', 'utf8'));
        paiCluster = `{\"userName\":\"${testPaiClusterInfo.userName}\",\"passWord\":\"${testPaiClusterInfo.passWord}\",\"host\":\"${testPaiClusterInfo.host}\"}`;
        paiTrialConfig = `{\"command\":\"echo hello && ls\",\"codeDir\":\"/tmp/nni/examples/trials/mnist",\"gpuNum\":\"1\",
\"cpuNum\":\"1\",\"memoryMB\":\"8196\",\"image\":\"openpai/pai.example.tensorflow\",\"dataDir\":\"\",\"outputDir\":\"\"}`;
    }
    catch (err) {
        console.log('Please configure rminfo.json to enable remote machine unit test.');
        skip = true;
    }
    let paiYarnTrainingService;
    console.log(tmp.dirSync().name);
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
        paiYarnTrainingService = component.get(paiYarnTrainingService_1.PAIYarnTrainingService);
        paiYarnTrainingService.run();
    });
    afterEach(() => {
        if (skip) {
            return;
        }
        paiYarnTrainingService.cleanUp();
    });
    it('Get PAI token', async () => {
        if (skip) {
            return;
        }
        console.log(`paiCluster is ${paiCluster}`);
        await paiYarnTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.PAI_YARN_CLUSTER_CONFIG, paiCluster);
        await paiYarnTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, paiTrialConfig);
        const form = {
            sequenceId: 0,
            hyperParameters: { value: '', index: 0 }
        };
        try {
            const trialDetail = await paiYarnTrainingService.submitTrialJob(form);
            chai.expect(trialDetail.status).to.be.equals('WAITING');
        }
        catch (error) {
            console.log('Submit job failed:' + error);
            chai.assert(error);
        }
    });
});
