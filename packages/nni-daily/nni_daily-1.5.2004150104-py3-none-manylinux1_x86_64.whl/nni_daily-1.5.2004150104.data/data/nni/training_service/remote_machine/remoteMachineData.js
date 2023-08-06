'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const ssh2_1 = require("ssh2");
const ts_deferred_1 = require("ts-deferred");
class RemoteMachineMeta {
    constructor() {
        this.ip = '';
        this.port = 22;
        this.username = '';
        this.passwd = '';
        this.useActiveGpu = false;
    }
}
exports.RemoteMachineMeta = RemoteMachineMeta;
function parseGpuIndices(gpuIndices) {
    if (gpuIndices !== undefined) {
        const indices = gpuIndices.split(',')
            .map((x) => parseInt(x, 10));
        if (indices.length > 0) {
            return new Set(indices);
        }
        else {
            throw new Error('gpuIndices can not be empty if specified.');
        }
    }
}
exports.parseGpuIndices = parseGpuIndices;
class RemoteCommandResult {
    constructor(stdout, stderr, exitCode) {
        this.stdout = stdout;
        this.stderr = stderr;
        this.exitCode = exitCode;
    }
}
exports.RemoteCommandResult = RemoteCommandResult;
class RemoteMachineTrialJobDetail {
    constructor(id, status, submitTime, workingDirectory, form) {
        this.id = id;
        this.status = status;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.tags = [];
        this.gpuIndices = [];
    }
}
exports.RemoteMachineTrialJobDetail = RemoteMachineTrialJobDetail;
class SSHClient {
    constructor(sshClient, usedConnectionNumber) {
        this.sshClient = sshClient;
        this.usedConnectionNumber = usedConnectionNumber;
    }
    get getSSHClientInstance() {
        return this.sshClient;
    }
    get getUsedConnectionNumber() {
        return this.usedConnectionNumber;
    }
    addUsedConnectionNumber() {
        this.usedConnectionNumber += 1;
    }
    minusUsedConnectionNumber() {
        this.usedConnectionNumber -= 1;
    }
}
exports.SSHClient = SSHClient;
class SSHClientManager {
    constructor(sshClientArray, maxTrialNumberPerConnection, rmMeta) {
        this.rmMeta = rmMeta;
        this.sshClientArray = sshClientArray;
        this.maxTrialNumberPerConnection = maxTrialNumberPerConnection;
    }
    async getAvailableSSHClient() {
        const deferred = new ts_deferred_1.Deferred();
        for (const index of this.sshClientArray.keys()) {
            const connectionNumber = this.sshClientArray[index].getUsedConnectionNumber;
            if (connectionNumber < this.maxTrialNumberPerConnection) {
                this.sshClientArray[index].addUsedConnectionNumber();
                deferred.resolve(this.sshClientArray[index].getSSHClientInstance);
                return deferred.promise;
            }
        }
        return this.initNewSSHClient();
    }
    addNewSSHClient(client) {
        this.sshClientArray.push(new SSHClient(client, 1));
    }
    getFirstSSHClient() {
        return this.sshClientArray[0].getSSHClientInstance;
    }
    closeAllSSHClient() {
        for (const sshClient of this.sshClientArray) {
            sshClient.getSSHClientInstance.end();
        }
    }
    releaseConnection(client) {
        if (client === undefined) {
            throw new Error(`could not release a undefined ssh client`);
        }
        for (const index of this.sshClientArray.keys()) {
            if (this.sshClientArray[index].getSSHClientInstance === client) {
                this.sshClientArray[index].minusUsedConnectionNumber();
                break;
            }
        }
    }
    initNewSSHClient() {
        const deferred = new ts_deferred_1.Deferred();
        const conn = new ssh2_1.Client();
        const connectConfig = {
            host: this.rmMeta.ip,
            port: this.rmMeta.port,
            username: this.rmMeta.username,
            tryKeyboard: true
        };
        if (this.rmMeta.passwd !== undefined) {
            connectConfig.password = this.rmMeta.passwd;
        }
        else if (this.rmMeta.sshKeyPath !== undefined) {
            if (!fs.existsSync(this.rmMeta.sshKeyPath)) {
                deferred.reject(new Error(`${this.rmMeta.sshKeyPath} does not exist.`));
            }
            const privateKey = fs.readFileSync(this.rmMeta.sshKeyPath, 'utf8');
            connectConfig.privateKey = privateKey;
            connectConfig.passphrase = this.rmMeta.passphrase;
        }
        else {
            deferred.reject(new Error(`No valid passwd or sshKeyPath is configed.`));
        }
        conn.on('ready', () => {
            this.addNewSSHClient(conn);
            deferred.resolve(conn);
        })
            .on('error', (err) => {
            deferred.reject(new Error(err.message));
        }).on("keyboard-interactive", (name, instructions, lang, prompts, finish) => {
            finish([this.rmMeta.passwd]);
        })
            .connect(connectConfig);
        return deferred.promise;
    }
}
exports.SSHClientManager = SSHClientManager;
var ScheduleResultType;
(function (ScheduleResultType) {
    ScheduleResultType[ScheduleResultType["SUCCEED"] = 0] = "SUCCEED";
    ScheduleResultType[ScheduleResultType["TMP_NO_AVAILABLE_GPU"] = 1] = "TMP_NO_AVAILABLE_GPU";
    ScheduleResultType[ScheduleResultType["REQUIRE_EXCEED_TOTAL"] = 2] = "REQUIRE_EXCEED_TOTAL";
})(ScheduleResultType = exports.ScheduleResultType || (exports.ScheduleResultType = {}));
exports.REMOTEMACHINE_TRIAL_COMMAND_FORMAT = `#!/bin/bash
export NNI_PLATFORM=remote NNI_SYS_DIR={0} NNI_OUTPUT_DIR={1} NNI_TRIAL_JOB_ID={2} NNI_EXP_ID={3} \
NNI_TRIAL_SEQ_ID={4} export MULTI_PHASE={5}
cd $NNI_SYS_DIR
sh install_nni.sh
echo $$ >{6}
python3 -m nni_trial_tool.trial_keeper --trial_command '{7}' --nnimanager_ip '{8}' --nnimanager_port '{9}' \
--nni_manager_version '{10}' --log_collection '{11}' 1>$NNI_OUTPUT_DIR/trialkeeper_stdout 2>$NNI_OUTPUT_DIR/trialkeeper_stderr
echo $? \`date +%s%3N\` >{12}`;
exports.HOST_JOB_SHELL_FORMAT = `#!/bin/bash
cd {0}
echo $$ >{1}
eval {2} >stdout 2>stderr
echo $? \`date +%s%3N\` >{3}`;
