"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const path = require("path");
const ts_deferred_1 = require("ts-deferred");
const experimentStartupInfo_1 = require("../../../common/experimentStartupInfo");
const log_1 = require("../../../common/log");
const utils_1 = require("../../../common/utils");
var HDFSClientUtility;
(function (HDFSClientUtility) {
    function hdfsExpRootDir(hdfsUserName) {
        return '/' + utils_1.unixPathJoin(hdfsUserName, 'nni', 'experiments', experimentStartupInfo_1.getExperimentId());
    }
    HDFSClientUtility.hdfsExpRootDir = hdfsExpRootDir;
    function getHdfsExpCodeDir(hdfsUserName) {
        return utils_1.unixPathJoin(hdfsExpRootDir(hdfsUserName), 'codeDir');
    }
    HDFSClientUtility.getHdfsExpCodeDir = getHdfsExpCodeDir;
    function getHdfsTrialWorkDir(hdfsUserName, trialId) {
        const root = hdfsExpRootDir(hdfsUserName);
        return utils_1.unixPathJoin(root, 'trials', trialId);
    }
    HDFSClientUtility.getHdfsTrialWorkDir = getHdfsTrialWorkDir;
    async function copyFileToHdfs(localFilePath, hdfsFilePath, hdfsClient) {
        const deferred = new ts_deferred_1.Deferred();
        fs.exists(localFilePath, (exists) => {
            if (exists) {
                const localFileStream = fs.createReadStream(localFilePath);
                const hdfsFileStream = hdfsClient.createWriteStream(hdfsFilePath);
                localFileStream.pipe(hdfsFileStream);
                hdfsFileStream.on('finish', () => {
                    deferred.resolve();
                });
                hdfsFileStream.on('error', (err) => {
                    log_1.getLogger()
                        .error(`HDFSCientUtility:copyFileToHdfs, copy file failed, err is ${err.message}`);
                    deferred.reject(err);
                });
            }
            else {
                log_1.getLogger()
                    .error(`HDFSCientUtility:copyFileToHdfs, ${localFilePath} doesn't exist locally`);
                deferred.reject('file not exist!');
            }
        });
        return deferred.promise;
    }
    HDFSClientUtility.copyFileToHdfs = copyFileToHdfs;
    async function copyDirectoryToHdfs(localDirectory, hdfsDirectory, hdfsClient) {
        const deferred = new ts_deferred_1.Deferred();
        const fileNameArray = fs.readdirSync(localDirectory);
        for (const fileName of fileNameArray) {
            const fullFilePath = path.join(localDirectory, fileName);
            try {
                if (fs.lstatSync(fullFilePath)
                    .isFile()) {
                    await copyFileToHdfs(fullFilePath, path.join(hdfsDirectory, fileName), hdfsClient);
                }
                else {
                    await copyDirectoryToHdfs(fullFilePath, path.join(hdfsDirectory, fileName), hdfsClient);
                }
            }
            catch (error) {
                deferred.reject(error);
            }
        }
        deferred.resolve();
        return deferred.promise;
    }
    HDFSClientUtility.copyDirectoryToHdfs = copyDirectoryToHdfs;
    async function pathExists(hdfsPath, hdfsClient) {
        const deferred = new ts_deferred_1.Deferred();
        hdfsClient.exists(hdfsPath, (exist) => {
            deferred.resolve(exist);
        });
        let timeoutId;
        const delayTimeout = new Promise((resolve, reject) => {
            timeoutId = setTimeout(() => { reject(`Check HDFS path ${hdfsPath} exists timeout`); }, 5000);
        });
        return Promise.race([deferred.promise, delayTimeout])
            .finally(() => { clearTimeout(timeoutId); });
    }
    HDFSClientUtility.pathExists = pathExists;
    async function readFileFromHDFS(hdfsPath, hdfsClient) {
        const deferred = new ts_deferred_1.Deferred();
        let buffer = Buffer.alloc(0);
        const exist = await pathExists(hdfsPath, hdfsClient);
        if (!exist) {
            deferred.reject(`${hdfsPath} doesn't exists`);
        }
        const remoteFileStream = hdfsClient.createReadStream(hdfsPath);
        remoteFileStream.on('error', (err) => {
            deferred.reject(err);
        });
        remoteFileStream.on('data', (chunk) => {
            buffer = Buffer.concat([buffer, chunk]);
        });
        remoteFileStream.on('finish', () => {
            deferred.resolve(buffer);
        });
        return deferred.promise;
    }
    HDFSClientUtility.readFileFromHDFS = readFileFromHDFS;
    function mkdir(hdfsPath, hdfsClient) {
        const deferred = new ts_deferred_1.Deferred();
        hdfsClient.mkdir(hdfsPath, (err) => {
            if (!err) {
                deferred.resolve(true);
            }
            else {
                deferred.reject(err.message);
            }
        });
        return deferred.promise;
    }
    HDFSClientUtility.mkdir = mkdir;
    async function readdir(hdfsPath, hdfsClient) {
        const deferred = new ts_deferred_1.Deferred();
        const exist = await pathExists(hdfsPath, hdfsClient);
        if (!exist) {
            deferred.reject(`${hdfsPath} doesn't exists`);
        }
        hdfsClient.readdir(hdfsPath, (err, files) => {
            if (err) {
                deferred.reject(err);
            }
            deferred.resolve(files);
        });
        return deferred.promise;
    }
    HDFSClientUtility.readdir = readdir;
    function deletePath(hdfsPath, hdfsClient, recursive = true) {
        const deferred = new ts_deferred_1.Deferred();
        hdfsClient.unlink(hdfsPath, recursive, (err) => {
            if (!err) {
                deferred.resolve(true);
            }
            else {
                deferred.reject(err.message);
            }
        });
        return deferred.promise;
    }
    HDFSClientUtility.deletePath = deletePath;
})(HDFSClientUtility = exports.HDFSClientUtility || (exports.HDFSClientUtility = {}));
