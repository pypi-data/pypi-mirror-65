'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const fs = require("fs");
const ssh2_1 = require("ssh2");
const ts_deferred_1 = require("ts-deferred");
const sshClientUtility_1 = require("../remote_machine/sshClientUtility");
const LOCALFILE = '/tmp/sshclientUTData';
const REMOTEFILE = '/tmp/sshclientUTData';
async function copyFile(conn) {
    const deferred = new ts_deferred_1.Deferred();
    conn.sftp((err, sftp) => {
        if (err) {
            deferred.reject(err);
            return;
        }
        sftp.fastPut(LOCALFILE, REMOTEFILE, (fastPutErr) => {
            sftp.end();
            if (fastPutErr) {
                deferred.reject(fastPutErr);
            }
            else {
                deferred.resolve();
            }
        });
    });
    return deferred.promise;
}
async function copyFileToRemoteLoop(conn) {
    for (let i = 0; i < 500; i++) {
        console.log(i);
        await sshClientUtility_1.SSHClientUtility.copyFileToRemote(LOCALFILE, REMOTEFILE, conn);
    }
}
async function remoteExeCommandLoop(conn) {
    for (let i = 0; i < 500; i++) {
        console.log(i);
        await sshClientUtility_1.SSHClientUtility.remoteExeCommand('ls', conn);
    }
}
async function getRemoteFileContentLoop(conn) {
    for (let i = 0; i < 500; i++) {
        console.log(i);
        await sshClientUtility_1.SSHClientUtility.getRemoteFileContent(REMOTEFILE, conn);
    }
}
describe('sshClientUtility test', () => {
    let skip = true;
    let rmMeta;
    try {
        rmMeta = JSON.parse(fs.readFileSync('../../.vscode/rminfo.json', 'utf8'));
    }
    catch (err) {
        skip = true;
    }
    before(async () => {
        await cpp.exec(`echo '1234' > ${LOCALFILE}`);
    });
    after(() => {
        fs.unlinkSync(LOCALFILE);
    });
    it('Test SSHClientUtility', (done) => {
        if (skip) {
            done();
            return;
        }
        const conn = new ssh2_1.Client();
        conn.on('ready', async () => {
            await copyFile(conn);
            await Promise.all([
                copyFileToRemoteLoop(conn),
                copyFileToRemoteLoop(conn),
                copyFileToRemoteLoop(conn),
                remoteExeCommandLoop(conn),
                getRemoteFileContentLoop(conn)
            ]);
            done();
        }).connect(rmMeta);
    });
});
