'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai_1 = require("chai");
const request = require("request");
const typescript_ioc_1 = require("typescript-ioc");
const component = require("../../common/component");
const datastore_1 = require("../../common/datastore");
const manager_1 = require("../../common/manager");
const trainingService_1 = require("../../common/trainingService");
const utils_1 = require("../../common/utils");
const mockedDatastore_1 = require("../../core/test/mockedDatastore");
const mockedTrainingService_1 = require("../../core/test/mockedTrainingService");
const nniRestServer_1 = require("../nniRestServer");
const mockedNNIManager_1 = require("./mockedNNIManager");
describe('Unit test for rest server', () => {
    let ROOT_URL;
    before((done) => {
        utils_1.prepareUnitTest();
        typescript_ioc_1.Container.bind(manager_1.Manager).provider(mockedNNIManager_1.testManagerProvider);
        typescript_ioc_1.Container.bind(datastore_1.DataStore).to(mockedDatastore_1.MockedDataStore);
        typescript_ioc_1.Container.bind(trainingService_1.TrainingService).to(mockedTrainingService_1.MockedTrainingService);
        const restServer = component.get(nniRestServer_1.NNIRestServer);
        restServer.start().then(() => {
            ROOT_URL = `${restServer.endPoint}/api/v1/nni`;
            done();
        }).catch((e) => {
            chai_1.assert.fail(`Failed to start rest server: ${e.message}`);
        });
    });
    after(() => {
        component.get(nniRestServer_1.NNIRestServer).stop();
        utils_1.cleanupUnitTest();
    });
    it('Test GET check-status', (done) => {
        request.get(`${ROOT_URL}/check-status`, (err, res) => {
            if (err) {
                chai_1.assert.fail(err.message);
            }
            else {
                chai_1.expect(res.statusCode).to.equal(200);
            }
            done();
        });
    });
    it('Test GET trial-jobs/:id', (done) => {
        request.get(`${ROOT_URL}/trial-jobs/1234`, (err, res, body) => {
            if (err) {
                chai_1.assert.fail(err.message);
            }
            else {
                chai_1.expect(res.statusCode).to.equal(200);
                chai_1.expect(JSON.parse(body).id).to.equal('1234');
            }
            done();
        });
    });
    it('Test GET experiment', (done) => {
        request.get(`${ROOT_URL}/experiment`, (err, res) => {
            if (err) {
                chai_1.assert.fail(err.message);
            }
            else {
                chai_1.expect(res.statusCode).to.equal(200);
            }
            done();
        });
    });
    it('Test GET trial-jobs', (done) => {
        request.get(`${ROOT_URL}/trial-jobs`, (err, res) => {
            chai_1.expect(res.statusCode).to.equal(200);
            if (err) {
                chai_1.assert.fail(err.message);
            }
            done();
        });
    });
    it('Test change concurrent-trial-jobs', (done) => {
        request.get(`${ROOT_URL}/experiment`, (err, res, body) => {
            if (err) {
                chai_1.assert.fail(err.message);
            }
            else {
                chai_1.expect(res.statusCode).to.equal(200);
                const profile = JSON.parse(body);
                if (profile.params && profile.params.trialConcurrency) {
                    profile.params.trialConcurrency = 10;
                }
                const req = {
                    uri: `${ROOT_URL}/experiment?update_type=TRIAL_CONCURRENCY`,
                    method: 'PUT',
                    json: true,
                    body: profile
                };
                request(req, (error, response) => {
                    if (error) {
                        chai_1.assert.fail(error.message);
                    }
                    else {
                        chai_1.expect(response.statusCode).to.equal(200);
                    }
                    done();
                });
            }
        });
    });
    it('Test PUT experiment/cluster-metadata bad key', (done) => {
        const req = {
            uri: `${ROOT_URL}/experiment/cluster-metadata`,
            method: 'PUT',
            json: true,
            body: {
                exception_test_key: 'test'
            }
        };
        request(req, (err, res) => {
            if (err) {
                chai_1.assert.fail(err.message);
            }
            else {
                chai_1.expect(res.statusCode).to.equal(400);
            }
            done();
        });
    });
    it('Test PUT experiment/cluster-metadata', (done) => {
        const req = {
            uri: `${ROOT_URL}/experiment/cluster-metadata`,
            method: 'PUT',
            json: true,
            body: {
                machine_list: [{
                        ip: '10.10.10.101',
                        port: 22,
                        username: 'test',
                        passwd: '1234'
                    }, {
                        ip: '10.10.10.102',
                        port: 22,
                        username: 'test',
                        passwd: '1234'
                    }]
            }
        };
        request(req, (err, res) => {
            if (err) {
                chai_1.assert.fail(err.message);
            }
            else {
                chai_1.expect(res.statusCode).to.equal(200);
            }
            done();
        });
    });
});
