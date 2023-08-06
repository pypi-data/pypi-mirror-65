'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const fs = require("fs");
const os = require("os");
const path = require("path");
const tmp = require("tmp");
const utils_1 = require("../../common/utils");
const hdfsClientUtility_1 = require("../pai/paiYarn/hdfsClientUtility");
var WebHDFS = require('webhdfs');
var rmdir = require('rmdir');
describe('WebHDFS', function () {
    let skip = false;
    let testHDFSInfo;
    let hdfsClient;
    try {
        testHDFSInfo = JSON.parse(fs.readFileSync('../../.vscode/hdfsInfo.json', 'utf8'));
        console.log(testHDFSInfo);
        hdfsClient = WebHDFS.createClient({
            user: testHDFSInfo.user,
            port: testHDFSInfo.port,
            host: testHDFSInfo.host
        });
    }
    catch (err) {
        console.log('Please configure rminfo.json to enable remote machine unit test.');
        skip = true;
    }
    before(() => {
        chai.should();
        chai.use(chaiAsPromised);
        tmp.setGracefulCleanup();
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    it('Test HDFS utility path functions', async () => {
        if (skip) {
            return;
        }
        const testPath = '/nni_unittest_' + utils_1.uniqueString(6);
        let exists = await hdfsClientUtility_1.HDFSClientUtility.pathExists(testPath, hdfsClient);
        chai.expect(exists).to.be.equals(false);
        const mkdirResult = await hdfsClientUtility_1.HDFSClientUtility.mkdir(testPath, hdfsClient);
        chai.expect(mkdirResult).to.be.equals(true);
        exists = await hdfsClientUtility_1.HDFSClientUtility.pathExists(testPath, hdfsClient);
        chai.expect(exists).to.be.equals(true);
        const deleteResult = await hdfsClientUtility_1.HDFSClientUtility.deletePath(testPath, hdfsClient);
        chai.expect(deleteResult).to.be.equals(true);
        exists = await hdfsClientUtility_1.HDFSClientUtility.pathExists(testPath, hdfsClient);
        chai.expect(exists).to.be.equals(false);
    });
    it('Test HDFS utility copyFileToHdfs', async () => {
        if (skip) {
            return;
        }
        const tmpLocalDirectoryPath = path.join(os.tmpdir(), 'nni_unittest_dir_' + utils_1.uniqueString(6));
        const tmpDataFilePath = path.join(tmpLocalDirectoryPath, 'file_' + utils_1.uniqueString(6));
        const testFileData = 'TestContent123';
        fs.mkdirSync(tmpLocalDirectoryPath);
        fs.writeFileSync(tmpDataFilePath, testFileData);
        const testHDFSFilePath = '/nni_unittest_' + utils_1.uniqueString(6);
        let exists = await hdfsClientUtility_1.HDFSClientUtility.pathExists(testHDFSFilePath, hdfsClient);
        chai.expect(exists).to.be.equals(false);
        await hdfsClientUtility_1.HDFSClientUtility.copyFileToHdfs(tmpDataFilePath, testHDFSFilePath, hdfsClient);
        exists = await hdfsClientUtility_1.HDFSClientUtility.pathExists(testHDFSFilePath, hdfsClient);
        chai.expect(exists).to.be.equals(true);
        const buffer = await hdfsClientUtility_1.HDFSClientUtility.readFileFromHDFS(testHDFSFilePath, hdfsClient);
        const actualFileData = buffer.toString('utf8');
        chai.expect(actualFileData).to.be.equals(testFileData);
        const testHDFSDirPath = path.join('/nni_unittest_' + utils_1.uniqueString(6) + '_dir');
        await hdfsClientUtility_1.HDFSClientUtility.copyDirectoryToHdfs(tmpLocalDirectoryPath, testHDFSDirPath, hdfsClient);
        const files = await hdfsClientUtility_1.HDFSClientUtility.readdir(testHDFSDirPath, hdfsClient);
        chai.expect(files.length).to.be.equals(1);
        chai.expect(files[0].pathSuffix).to.be.equals(path.parse(tmpDataFilePath).base);
        rmdir(tmpLocalDirectoryPath);
        let deleteRestult = await hdfsClientUtility_1.HDFSClientUtility.deletePath(testHDFSFilePath, hdfsClient);
        chai.expect(deleteRestult).to.be.equals(true);
        deleteRestult = await hdfsClientUtility_1.HDFSClientUtility.deletePath(testHDFSDirPath, hdfsClient);
        chai.expect(deleteRestult).to.be.equals(true);
    });
});
