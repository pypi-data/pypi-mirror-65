'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const os = require("os");
const path = require("path");
const ts_deferred_1 = require("ts-deferred");
const errors_1 = require("../../common/errors");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
const util_1 = require("../common/util");
var SSHClientUtility;
(function (SSHClientUtility) {
    function copyFileToRemote(localFilePath, remoteFilePath, sshClient) {
        const log = log_1.getLogger();
        log.debug(`copyFileToRemote: localFilePath: ${localFilePath}, remoteFilePath: ${remoteFilePath}`);
        assert(sshClient !== undefined);
        const deferred = new ts_deferred_1.Deferred();
        sshClient.sftp((err, sftp) => {
            if (err !== undefined && err !== null) {
                log.error(`copyFileToRemote: ${err.message}, ${localFilePath}, ${remoteFilePath}`);
                deferred.reject(err);
                return;
            }
            assert(sftp !== undefined);
            sftp.fastPut(localFilePath, remoteFilePath, (fastPutErr) => {
                sftp.end();
                if (fastPutErr !== undefined && fastPutErr !== null) {
                    deferred.reject(fastPutErr);
                }
                else {
                    deferred.resolve(true);
                }
            });
        });
        return deferred.promise;
    }
    SSHClientUtility.copyFileToRemote = copyFileToRemote;
    function remoteExeCommand(command, client) {
        const log = log_1.getLogger();
        log.debug(`remoteExeCommand: command: [${command}]`);
        const deferred = new ts_deferred_1.Deferred();
        let stdout = '';
        let stderr = '';
        let exitCode;
        client.exec(command, (err, channel) => {
            if (err !== undefined && err !== null) {
                log.error(`remoteExeCommand: ${err.message}`);
                deferred.reject(err);
                return;
            }
            channel.on('data', (data, dataStderr) => {
                if (dataStderr !== undefined && dataStderr !== null) {
                    stderr += data.toString();
                }
                else {
                    stdout += data.toString();
                }
            })
                .on('exit', (code, signal) => {
                exitCode = code;
                deferred.resolve({
                    stdout: stdout,
                    stderr: stderr,
                    exitCode: exitCode
                });
            });
        });
        return deferred.promise;
    }
    SSHClientUtility.remoteExeCommand = remoteExeCommand;
    async function copyDirectoryToRemote(localDirectory, remoteDirectory, sshClient, remoteOS) {
        const tmpSuffix = utils_1.uniqueString(5);
        const localTarPath = path.join(os.tmpdir(), `nni_tmp_local_${tmpSuffix}.tar.gz`);
        const remoteTarPath = utils_1.unixPathJoin(utils_1.getRemoteTmpDir(remoteOS), `nni_tmp_remote_${tmpSuffix}.tar.gz`);
        await util_1.tarAdd(localTarPath, localDirectory);
        await copyFileToRemote(localTarPath, remoteTarPath, sshClient);
        await util_1.execRemove(localTarPath);
        await remoteExeCommand(`tar -oxzf ${remoteTarPath} -C ${remoteDirectory}`, sshClient);
        await remoteExeCommand(`rm ${remoteTarPath}`, sshClient);
    }
    SSHClientUtility.copyDirectoryToRemote = copyDirectoryToRemote;
    function getRemoteFileContent(filePath, sshClient) {
        const deferred = new ts_deferred_1.Deferred();
        sshClient.sftp((err, sftp) => {
            if (err !== undefined && err !== null) {
                log_1.getLogger()
                    .error(`getRemoteFileContent: ${err.message}`);
                deferred.reject(new Error(`SFTP error: ${err.message}`));
                return;
            }
            try {
                const sftpStream = sftp.createReadStream(filePath);
                let dataBuffer = '';
                sftpStream.on('data', (data) => {
                    dataBuffer += data;
                })
                    .on('error', (streamErr) => {
                    sftp.end();
                    deferred.reject(new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, streamErr.message));
                })
                    .on('end', () => {
                    sftp.end();
                    deferred.resolve(dataBuffer);
                });
            }
            catch (error) {
                log_1.getLogger()
                    .error(`getRemoteFileContent: ${error.message}`);
                sftp.end();
                deferred.reject(new Error(`SFTP error: ${error.message}`));
            }
        });
        return deferred.promise;
    }
    SSHClientUtility.getRemoteFileContent = getRemoteFileContent;
})(SSHClientUtility = exports.SSHClientUtility || (exports.SSHClientUtility = {}));
