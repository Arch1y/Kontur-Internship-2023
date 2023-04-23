{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.6.6","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code]\nimport numpy as np\nimport torch\n\n\nclass AverageMeter:\n    \"\"\"Computes and stores the average and current value\n    \"\"\"\n    def __init__(self):\n        self.reset()\n\n    def reset(self):\n        self.val = 0\n        self.avg = 0\n        self.sum = 0\n        self.count = 0\n\n    def update(self, val, n=1):\n        self.val = val\n        self.sum += val * n\n        self.count += n\n        self.avg = self.sum / self.count\n\n\nclass EarlyStopping:\n    '''Early stopping for neural network\n    '''\n    def __init__(self, patience=7, mode=\"max\", delta=0.001):\n        self.patience = patience\n        self.counter = 0\n        self.mode = mode\n        self.best_score = None\n        self.early_stop = False\n        self.delta = delta\n        if self.mode == \"min\":\n            self.val_score = np.Inf\n        else:\n            self.val_score = -np.Inf\n\n    def __call__(self, epoch_score, model, model_path):\n\n        if self.mode == \"min\":\n            score = -1.0 * epoch_score\n        else:\n            score = np.copy(epoch_score)\n\n        if self.best_score is None:\n            self.best_score = score\n            self.save_checkpoint(epoch_score, model, model_path)\n        elif score < self.best_score + self.delta:\n            self.counter += 1\n            print('EarlyStopping counter: {} out of {}'.format(self.counter, self.patience))\n            if self.counter >= self.patience:\n                self.early_stop = True\n        else:\n            self.best_score = score\n            self.save_checkpoint(epoch_score, model, model_path)\n            self.counter = 0\n\n    def save_checkpoint(self, epoch_score, model, model_path):\n        if epoch_score not in [-np.inf, np.inf, -np.nan, np.nan]:\n            print('Validation score improved ({} --> {}). Saving model!'.format(self.val_score, epoch_score))\n            torch.save(model.state_dict(), model_path)\n        self.val_score = epoch_score\n\n\ndef jaccard(string1, string2):\n    '''Calculates Jaccard on strings.'''\n    string1 = set(string1.lower().split()) \n    string2 = set(string2.lower().split())\n    intersection_string = string1.intersection(string2)\n    if len(string1) == 0 and len(string2) == 0:\n        return 1\n    return float(len(intersection_string)) / (len(string1) + len(string2) - len(intersection_string))\n\ndef jaccard_array(array1, array2):\n    \"\"\"Calculates Jaccard on arrays.\"\"\"\n    array1 = set(array1)\n    array2 = set(array2)\n    intersection_arrays = array1.intersection(array2)\n    if len(array1) == len(array2):\n        return 1\n    return float(len(intersection_arrays)) / (len(array1) + len(array2) - len(intersection_arrays))\n\ndef accuracy(string1, string2):\n    string1 = set(string1.lower().split())\n    string2 = set(string2.lower().split())\n    if len(string1) == len(string2):\n        return 1\n    return 0","metadata":{"_uuid":"8f801297-2165-4042-b470-1a1dabd6d222","_cell_guid":"4b5754bd-c491-48e9-8b1d-dfaa2418f352","collapsed":false,"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2023-04-15T09:49:53.332034Z","iopub.execute_input":"2023-04-15T09:49:53.332443Z","iopub.status.idle":"2023-04-15T09:49:53.339978Z","shell.execute_reply.started":"2023-04-15T09:49:53.332411Z","shell.execute_reply":"2023-04-15T09:49:53.338141Z"},"trusted":true},"execution_count":1,"outputs":[{"traceback":["\u001b[0;36m  File \u001b[0;32m\"<ipython-input-1-ccc1c2897a84>\"\u001b[0;36m, line \u001b[0;32m1\u001b[0m\n\u001b[0;31m    if len(a) == 0 and len(b) == 0:\u001b[0m\n\u001b[0m                                   ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m unexpected EOF while parsing\n"],"ename":"SyntaxError","evalue":"unexpected EOF while parsing (<ipython-input-1-ccc1c2897a84>, line 1)","output_type":"error"}]}]}