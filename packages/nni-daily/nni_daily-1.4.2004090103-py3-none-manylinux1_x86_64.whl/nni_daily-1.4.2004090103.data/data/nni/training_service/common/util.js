'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const cp = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const typescript_string_operations_1 = require("typescript-string-operations");
const utils_1 = require("../../common/utils");
const gpuData_1 = require("./gpuData");
async function validateCodeDir(codeDir) {
    let fileCount;
    let fileNameValid = true;
    try {
        fileCount = await utils_1.countFilesRecursively(codeDir);
    }
    catch (error) {
        throw new Error(`Call count file error: ${error}`);
    }
    try {
        fileNameValid = await utils_1.validateFileNameRecursively(codeDir);
    }
    catch (error) {
        throw new Error(`Validate file name error: ${error}`);
    }
    if (fileCount !== undefined && fileCount > 1000) {
        const errMessage = `Too many files(${fileCount} found}) in ${codeDir},`
            + ` please check if it's a valid code dir`;
        throw new Error(errMessage);
    }
    if (!fileNameValid) {
        const errMessage = `File name in ${codeDir} is not valid, please check file names, only support digit number、alphabet and (.-_) in file name.`;
        throw new Error(errMessage);
    }
    return fileCount;
}
exports.validateCodeDir = validateCodeDir;
async function execMkdir(directory, share = false) {
    if (process.platform === 'win32') {
        await cpp.exec(`powershell.exe New-Item -Path "${directory}" -ItemType "directory" -Force`);
    }
    else if (share) {
        await cpp.exec(`(umask 0; mkdir -p '${directory}')`);
    }
    else {
        await cpp.exec(`mkdir -p '${directory}'`);
    }
    return Promise.resolve();
}
exports.execMkdir = execMkdir;
async function execCopydir(source, destination) {
    if (process.platform === 'win32') {
        await cpp.exec(`powershell.exe Copy-Item "${source}" -Destination "${destination}" -Recurse`);
    }
    else {
        await cpp.exec(`cp -r '${source}/.' '${destination}'`);
    }
    return Promise.resolve();
}
exports.execCopydir = execCopydir;
async function execNewFile(filename) {
    if (process.platform === 'win32') {
        await cpp.exec(`powershell.exe New-Item -Path "${filename}" -ItemType "file" -Force`);
    }
    else {
        await cpp.exec(`touch '${filename}'`);
    }
    return Promise.resolve();
}
exports.execNewFile = execNewFile;
function runScript(filePath) {
    if (process.platform === 'win32') {
        return cp.exec(`powershell.exe -ExecutionPolicy Bypass -file "${filePath}"`);
    }
    else {
        return cp.exec(`bash '${filePath}'`);
    }
}
exports.runScript = runScript;
async function execTail(filePath) {
    let cmdresult;
    if (process.platform === 'win32') {
        cmdresult = await cpp.exec(`powershell.exe Get-Content "${filePath}" -Tail 1`);
    }
    else {
        cmdresult = await cpp.exec(`tail -n 1 '${filePath}'`);
    }
    return Promise.resolve(cmdresult);
}
exports.execTail = execTail;
async function execRemove(directory) {
    if (process.platform === 'win32') {
        await cpp.exec(`powershell.exe Remove-Item "${directory}" -Recurse -Force`);
    }
    else {
        await cpp.exec(`rm -rf '${directory}'`);
    }
    return Promise.resolve();
}
exports.execRemove = execRemove;
async function execKill(pid) {
    if (process.platform === 'win32') {
        await cpp.exec(`cmd.exe /c taskkill /PID ${pid} /T /F`);
    }
    else {
        await cpp.exec(`pkill -P ${pid}`);
    }
    return Promise.resolve();
}
exports.execKill = execKill;
function setEnvironmentVariable(variable) {
    if (process.platform === 'win32') {
        return `$env:${variable.key}="${variable.value}"`;
    }
    else {
        return `export ${variable.key}='${variable.value}'`;
    }
}
exports.setEnvironmentVariable = setEnvironmentVariable;
async function tarAdd(tarPath, sourcePath) {
    if (process.platform === 'win32') {
        const tarFilePath = tarPath.split('\\')
            .join('\\\\');
        const sourceFilePath = sourcePath.split('\\')
            .join('\\\\');
        const script = [];
        script.push(`import os`, `import tarfile`, typescript_string_operations_1.String.Format(`tar = tarfile.open("{0}","w:gz")\r\nfor root,dir,files in os.walk("{1}"):`, tarFilePath, sourceFilePath), `    for file in files:`, `        fullpath = os.path.join(root,file)`, `        tar.add(fullpath, arcname=file)`, `tar.close()`);
        await fs.promises.writeFile(path.join(os.tmpdir(), 'tar.py'), script.join(utils_1.getNewLine()), { encoding: 'utf8', mode: 0o777 });
        const tarScript = path.join(os.tmpdir(), 'tar.py');
        await cpp.exec(`python ${tarScript}`);
    }
    else {
        await cpp.exec(`tar -czf ${tarPath} -C ${sourcePath} .`);
    }
    return Promise.resolve();
}
exports.tarAdd = tarAdd;
function getScriptName(fileNamePrefix) {
    if (process.platform === 'win32') {
        return typescript_string_operations_1.String.Format('{0}.ps1', fileNamePrefix);
    }
    else {
        return typescript_string_operations_1.String.Format('{0}.sh', fileNamePrefix);
    }
}
exports.getScriptName = getScriptName;
function getGpuMetricsCollectorBashScriptContent(scriptFolder) {
    return `echo $$ > ${scriptFolder}/pid ; METRIC_OUTPUT_DIR=${scriptFolder} python3 -m nni_gpu_tool.gpu_metrics_collector`;
}
exports.getGpuMetricsCollectorBashScriptContent = getGpuMetricsCollectorBashScriptContent;
function runGpuMetricsCollector(scriptFolder) {
    if (process.platform === 'win32') {
        const scriptPath = path.join(scriptFolder, 'gpu_metrics_collector.ps1');
        const content = typescript_string_operations_1.String.Format(gpuData_1.GPU_INFO_COLLECTOR_FORMAT_WINDOWS, scriptFolder, path.join(scriptFolder, 'pid'));
        fs.writeFile(scriptPath, content, { encoding: 'utf8' }, () => { runScript(scriptPath); });
    }
    else {
        cp.exec(getGpuMetricsCollectorBashScriptContent(scriptFolder), { shell: '/bin/bash' });
    }
}
exports.runGpuMetricsCollector = runGpuMetricsCollector;
