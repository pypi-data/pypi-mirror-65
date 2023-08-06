import os, shutil, random

def break_up_database(database, devide=[0.7,0.3]):
    assert os.path.isdir(database)
    assert len(devide) in [2, 3]
    assert sum(devide) == 1
    name = database
    if len(devide) == 2:
        os.mkdir(name + '_train')
        os.mkdir(name + '_test')

        for path in os.listdir(name):
            os.mkdir(os.path.join(name + '_train',path))
            os.mkdir(os.path.join(name + '_test',path))
            for file_path in os.listdir(os.path.join(name, path)):
                if random.random() < devide[0]:
                    shutil.copy(os.path.join(name, path,file_path),os.path.join(name + '_train', path,file_path))
                else:
                    shutil.copy(os.path.join(name, path,file_path),os.path.join(name + '_test', path,file_path))
    else:
        os.mkdir(name + '_train')
        os.mkdir(name + '_valid')
        os.mkdir(name + '_test')
        for path in os.listdir(name):
            os.mkdir(os.path.join(name + '_train',path))
            os.mkdir(os.path.join(name + '_valid',path))
            os.mkdir(os.path.join(name + '_test',path))
            for file_path in os.listdir(os.path.join(name, path)):
                if random.random() < devide[0]:
                    shutil.copy(os.path.join(name, path,file_path),os.path.join(name + '_train', path,file_path))
                elif random.random()< devide[0] + devide[1]:
                    shutil.copy(os.path.join(name, path,file_path),os.path.join(name + '_valid', path,file_path))
                else:
                    shutil.copy(os.path.join(name, path,file_path),os.path.join(name + '_test', path,file_path))


