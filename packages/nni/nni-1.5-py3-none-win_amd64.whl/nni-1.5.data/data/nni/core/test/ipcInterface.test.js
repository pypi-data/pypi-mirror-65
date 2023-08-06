'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const ts_deferred_1 = require("ts-deferred");
const utils_1 = require("../../common/utils");
const ipcInterface_1 = require("../ipcInterface");
let sentCommands = [];
const receivedCommands = [];
let commandTooLong;
let rejectCommandType;
function runProcess() {
    const deferred = new ts_deferred_1.Deferred();
    const stdio = ['ignore', 'pipe', process.stderr, 'pipe', 'pipe'];
    const command = utils_1.getCmdPy() + ' assessor.py';
    const proc = utils_1.getTunerProc(command, stdio, 'core/test', process.env);
    proc.on('error', (error) => { deferred.resolve(error); });
    proc.on('exit', (code) => {
        if (code !== 0) {
            deferred.resolve(new Error(`return code: ${code}`));
        }
        else {
            let str = proc.stdout.read().toString();
            if (str.search("\r\n") != -1) {
                sentCommands = str.split("\r\n");
            }
            else {
                sentCommands = str.split('\n');
            }
            deferred.resolve(null);
        }
    });
    const dispatcher = ipcInterface_1.createDispatcherInterface(proc);
    dispatcher.onCommand((commandType, content) => {
        receivedCommands.push({ commandType, content });
    });
    dispatcher.sendCommand('IN');
    dispatcher.sendCommand('ME', '123');
    try {
        dispatcher.sendCommand('ME', 'x'.repeat(1000000));
    }
    catch (error) {
        commandTooLong = error;
    }
    try {
        dispatcher.sendCommand('FE', '1');
    }
    catch (error) {
        rejectCommandType = error;
    }
    return deferred.promise;
}
describe('core/protocol', () => {
    before(async () => {
        utils_1.prepareUnitTest();
        await runProcess();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    it('should have sent 2 successful commands', () => {
        assert.equal(sentCommands.length, 3);
        assert.equal(sentCommands[2], '');
    });
    it('sendCommand() should work without content', () => {
        assert.equal(sentCommands[0], '(\'IN\', \'\')');
    });
    it('sendCommand() should work with content', () => {
        assert.equal(sentCommands[1], '(\'ME\', \'123\')');
    });
    it('sendCommand() should throw on too long command', () => {
        if (commandTooLong === undefined) {
            assert.fail('Should throw error');
        }
        else {
            const err = commandTooLong.cause;
            assert(err && err.name === 'RangeError');
            assert(err && err.message === 'Command too long');
        }
    });
    it('sendCommand() should throw on wrong command type', () => {
        assert.equal(rejectCommandType.name, 'AssertionError [ERR_ASSERTION]');
    });
    it('should have received 3 commands', () => {
        assert.equal(receivedCommands.length, 3);
    });
    it('onCommand() should work without content', () => {
        assert.deepStrictEqual(receivedCommands[0], {
            commandType: 'KI',
            content: ''
        });
    });
    it('onCommand() should work with content', () => {
        assert.deepStrictEqual(receivedCommands[1], {
            commandType: 'KI',
            content: 'hello'
        });
    });
    it('onCommand() should work with Unicode content', () => {
        assert.deepStrictEqual(receivedCommands[2], {
            commandType: 'KI',
            content: '世界'
        });
    });
});
