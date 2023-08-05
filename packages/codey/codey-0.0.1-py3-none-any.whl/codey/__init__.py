from makeblock import mBuild
cyber = mBuild.create()
__modules = {}
def __Ultrasonic(idx):
    if not ('ultrasonic' in __modules):
        __modules['ultrasonic'] = {}
    if not (idx in __modules['ultrasonic']):
        __modules['ultrasonic'][idx] = cyber.Ultrasonic(idx)
    return __modules['ultrasonic'][idx]
cyber.ultrasonic = __Ultrasonic