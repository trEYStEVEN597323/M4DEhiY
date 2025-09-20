# 代码生成时间: 2025-09-21 07:16:46
import os
import shutil
import json
from datetime import datetime
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

# 配置备份和恢复的文件夹路径
BACKUP_DIR = 'backups/'
RESTORE_DIR = 'restore/'

class BackupHandler(RequestHandler):
    """处理数据备份的请求"""
    def post(self):
        # 获取备份名称
        backup_name = self.get_argument('name')
        if not backup_name:
            self.write({'error': 'Backup name is required'})
            return

        # 创建备份
        try:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            backup_path = os.path.join(BACKUP_DIR, f'{backup_name}_{timestamp}.tar.gz')
            shutil.make_archive(backup_path, 'gztar', '.', 'data')
            self.write({'message': f'Backup created successfully at {backup_path}'})
        except Exception as e:
            self.write({'error': str(e)})

class RestoreHandler(RequestHandler):
    """处理数据恢复的请求"""
    def post(self):
        # 获取备份文件名
        backup_file = self.get_argument('file')
        if not backup_file:
            self.write({'error': 'Backup file is required'})
            return

        # 恢复备份
        try:
            backup_path = os.path.join(BACKUP_DIR, backup_file)
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f'Backup file {backup_file} not found')

            # 解压备份文件
            shutil.unpack_archive(backup_path, 'data', 'gztar')
            self.write({'message': f'Restored from {backup_file} successfully'})
        except Exception as e:
            self.write({'error': str(e)})

def make_app():
    """创建Tornado应用程序"""
    return Application([
        (r'/backup', BackupHandler),
        (r'/restore', RestoreHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()
