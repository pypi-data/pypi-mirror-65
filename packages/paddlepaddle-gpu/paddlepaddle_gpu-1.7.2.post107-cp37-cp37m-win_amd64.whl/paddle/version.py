# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.7.2'
major           = '1'
minor           = '7'
patch           = '2'
rc              = '0'
istaged         = False
commit          = '92cc33c0e48a98c07a6cf686a22f15bf396fe701'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
