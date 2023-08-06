'''
@author: zhangkai
@license: (C) Copyright 2017-2023
@contact: jeffcobile@gmail.com
@Software : PyCharm
@file: logger.py
@time: 2020-03-31 17:33:44
@desc: 
'''
import os
import torch
import json


class Logger:
    def __init__(self, output=str):
        self.output = output
        self.__init_folders__()

    def __init_folders__(self):
        self.train_log_path = os.path.join(self.output, "train_logs")
        self.eval_log_path = os.path.join(self.output, "eval_logs")
        self.test_log_path = os.path.join(self.output, 'test_logs')

        folders = [self.output,
                   self.train_log_path,
                   self.eval_log_path,
                   self.test_log_path]

        for folder in folders:
            if not os.path.exists(folder):
                os.mkdir(folder)

        if not os.path.exists(os.path.join(self.train_log_path, "checkpoint.txt")):
            with open(os.path.join(self.train_log_path, "checkpoint.txt"), 'w') as file:
                file.close()

        if not os.path.exists(os.path.join(self.train_log_path, "loss.txt")):
            with open(os.path.join(self.train_log_path, "loss.txt"), 'w') as file:
                file.close()

        if not os.path.exists(os.path.join(self.eval_log_path, "eval.txt")):
            with open(os.path.join(self.eval_log_path, "eval.txt"), 'w') as file:
                file.close()

        self.checkpoint_file = os.path.join(self.train_log_path, "checkpoint.txt")
        self.loss_file = os.path.join(self.train_log_path, "loss.txt")
        self.eval_file = os.path.join(self.eval_log_path, "eval.txt")

    def logger(self, content, phase='c'):
        '''
        :param content:
        :param phase:c => checkpoint_file; l => loss_file; e => eval_file
        :return:
        '''
        f = None
        if phase == 'c':
            f = self.checkpoint_file
        elif phase == 'l':
            f = self.loss_file
        elif phase == 'e':
            f = self.eval_file
        else:
            raise Exception('phase must be c or l or e')

        with open(f, 'a') as file:
            file.writelines(content + '\n')

    def save_checkpoints_file(self, epoch, state_dict=dict):
        pth_file_name = os.path.join(self.train_log_path, '%d.pth' % epoch )
        torch.save(state_dict, pth_file_name)
        self.logger(content='epoch {epoch:d}: {filename}'.format(epoch=epoch, filename=pth_file_name),phase='c')

    def save_eval_json_file(self, epoch, jsonContent):
        with open(os.path.join(self.eval_log_path, "%d.json" % epoch), 'w') as f:
            f.write(json.dumps(jsonContent))

    def get_path_files(self):
        return self.train_log_path, self.eval_log_path, self.test_log_path, self.checkpoint_file, self.loss_file, self.eval_file
