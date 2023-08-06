'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
exports.PAI_INSTALL_NNI_SHELL_FORMAT = `#!/bin/bash
if python3 -c 'import nni' > /dev/null 2>&1; then
  # nni module is already installed, skip
  return
else
  # Install nni
  python3 -m pip install --user nni
fi`;
exports.PAI_K8S_TRIAL_COMMAND_FORMAT = `export NNI_PLATFORM=pai NNI_SYS_DIR={0} NNI_OUTPUT_DIR={1} NNI_TRIAL_JOB_ID={2} NNI_EXP_ID={3} NNI_TRIAL_SEQ_ID={4} MULTI_PHASE={5} \
&& ls $NNI_SYS_DIR \
&& cd $NNI_SYS_DIR && sh install_nni.sh \
&& python3 -m nni_trial_tool.trial_keeper --trial_command '{6}' --nnimanager_ip '{7}' --nnimanager_port '{8}' \
--nni_manager_version '{9}' --log_collection '{10}'`;
