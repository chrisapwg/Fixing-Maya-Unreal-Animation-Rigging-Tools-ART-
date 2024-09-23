# Fucking Fixing ART Rigging System Tools
# By Chris Gultom

import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

windowName_ART = 'fixingART'
windowTitle_ART = 'Fixing ART Tools'
titleText_ART = 'Fucking Fixing ART Rigging System Tools'
sizeHeight_ART = 550
sizeWidth_ART = 400
holderSize_ART = 23
sliceText_ART = '# ------------------------------------------------------------------ #'

# --- Define ---

findNameResult = []
def findName(sel):
    global findNameResult
    i = str(sel)
    iSplit = i.split('_')
    iTotalNumber = len(i)
    iSplitLast = len(iSplit[-1])
    iNumber = iTotalNumber - iSplitLast
    ina = i[:iNumber-1]
    findNameResult = ina

def createDummyPoleVectorArm(pointValue, toCTL, parentTo):
    findName(toCTL)
    dummyMesh = pm.polyPlane(sx=1, sy=1, n=findNameResult + 'Fix_MSH')[0]
    armMoveValue = pm.intField('armMoveValue', query=True, value=True)
    pm.delete(dummyMesh + '.vtx[3]')
    cls1 = pm.cluster(dummyMesh + '.vtx[0]')
    cls2 = pm.cluster(dummyMesh + '.vtx[1]')
    cls3 = pm.cluster(dummyMesh + '.vtx[2]')
    pm.delete(pm.pointConstraint(pointValue[2], cls1, mo=False))
    pm.delete(pm.pointConstraint(pointValue[1], cls2, mo=False))
    pm.delete(pm.pointConstraint(pointValue[0], cls3, mo=False))
    pm.delete(dummyMesh, ch=True)
    pm.move(0, 0, armMoveValue, dummyMesh + '.vtx[1]', r=True, ls=True, cs=True, wd=True)
    cls = pm.cluster(dummyMesh + '.vtx[1]')
    pm.delete(pm.pointConstraint(cls, toCTL, mo=False))
    pm.parent(dummyMesh, parentTo)
    pm.delete(cls)
    pm.delete(dummyMesh)

def createDummyPoleVectorLeg(pointValue, toCTL, parentTo):
    findName(toCTL)
    dummyMesh = pm.polyPlane(sx=1, sy=1, n=findNameResult + 'Fix_MSH')[0]
    legMoveValue = pm.intField('legMoveValue', query=True, value=True)
    pm.delete(dummyMesh + '.vtx[3]')
    cls1 = pm.cluster(dummyMesh + '.vtx[0]')
    cls2 = pm.cluster(dummyMesh + '.vtx[1]')
    cls3 = pm.cluster(dummyMesh + '.vtx[2]')
    pm.delete(pm.pointConstraint(pointValue[2], cls1, mo=False))
    pm.delete(pm.pointConstraint(pointValue[1], cls2, mo=False))
    pm.delete(pm.pointConstraint(pointValue[0], cls3, mo=False))
    pm.delete(dummyMesh, ch=True)
    pm.move(0, 0, legMoveValue, dummyMesh + '.vtx[1]', r=True, ls=True, cs=True, wd=True)
    cls = pm.cluster(dummyMesh + '.vtx[1]')
    pm.delete(pm.pointConstraint(cls, toCTL, mo=False))
    pm.parent(dummyMesh, parentTo)
    pm.delete(cls)
    pm.delete(dummyMesh)

###

def toggleModule():
    listMSH = pm.ls('*_proxy_geo')
    listLRA = pm.ls('*_lra')
    listCTL = pm.ls('*_mover')
    
    if pm.getAttr(listMSH[0] + '.visibility') == True:
        for sel in listMSH:
            pm.setAttr(sel + '.visibility', l=0)
            pm.setAttr(sel + '.visibility', 0)
        '''
        for sel in listLRA:
            pm.setAttr(sel + '.visibility', l=0)
            pm.setAttr(sel + '.visibility', 0)
        for sel in listCTL:
            pm.setAttr(sel + '.displayLocalAxis', 1)
        '''
    else:
        for sel in listMSH:
            pm.setAttr(sel + '.visibility', l=0)
            pm.setAttr(sel + '.visibility', 1)
        '''
        for sel in listLRA:
            pm.setAttr(sel + '.visibility', l=0)
            pm.setAttr(sel + '.visibility', 1)
        for sel in listCTL:
            pm.setAttr(sel + '.displayLocalAxis', 0)
        '''

def mirrorModule():
    selected = pm.ls(os=True)
    
    for o in selected:
        pm.setAttr(o + '.translateX', pm.getAttr(o.replace('_r_', '_l_') + '.translateX') * -1)
        pm.setAttr(o + '.translateY', pm.getAttr(o.replace('_r_', '_l_') + '.translateY') * -1)
        pm.setAttr(o + '.translateZ', pm.getAttr(o.replace('_r_', '_l_') + '.translateZ') * -1)
        pm.setAttr(o + '.rotateX', pm.getAttr(o.replace('_r_', '_l_') + '.rotateX'))
        pm.setAttr(o + '.rotateY', pm.getAttr(o.replace('_r_', '_l_') + '.rotateY'))
        pm.setAttr(o + '.rotateZ', pm.getAttr(o.replace('_r_', '_l_') + '.rotateZ'))
        pm.setAttr(o + '.globalScale', pm.getAttr(o.replace('_r_', '_l_') + '.globalScale'))

def unlockJoint():
    rootJNT = 'root'
    drivenJNT = 'driver_root'
    rootList = pm.listRelatives(rootJNT, ad=True, type='joint')
    drivenList = pm.listRelatives(drivenJNT, ad=True, type='joint')
    rootList.append(rootJNT)
    drivenList.append(drivenJNT)
    
    for list in rootList:
        pm.setAttr(list + '.visibility', l=False)
    
    for list in drivenList:
        pm.setAttr(list + '.visibility', l=False)

def lockJoint():
    rootJNT = 'root'
    drivenJNT = 'driver_root'
    rootList = pm.listRelatives(rootJNT, ad=True, type='joint')
    drivenList = pm.listRelatives(drivenJNT, ad=True, type='joint')
    rootList.append(rootJNT)
    drivenList.append(drivenJNT)
    
    for list in rootList:
        pm.setAttr(list + '.visibility', l=True)
        pm.setAttr(list + '.visibility', 0)
    
    for list in drivenList:
        pm.setAttr(list + '.visibility', l=True)
        pm.setAttr(list + '.visibility', 0)

def toggleRoot():
    rootJNT = 'root'
    rootList = pm.listRelatives(rootJNT, ad=True, type='joint')
    rootList.append(rootJNT)
    
    toggleValue = pm.getAttr(rootJNT + '.visibility')
    
    if toggleValue == True:
        for list in rootList:
            try:
                pm.setAttr(list + '.visibility', 0)
                pm.setAttr(list + '.visibility', l=True)
            except:
                pass
            
    elif toggleValue == False:
        for list in rootList:
            try:
                pm.setAttr(list + '.visibility', l=False)
                pm.setAttr(list + '.visibility', 1)
            except:
                pass

def toggleDriven():
    drivenJNT = 'driver_root'
    drivenList = pm.listRelatives(drivenJNT, ad=True, type='joint')
    drivenList.append(drivenJNT)
    
    toggleValue = pm.getAttr(drivenJNT + '.visibility')
    
    if toggleValue == True:
        for list in drivenList:
            try:
                pm.setAttr(list + '.visibility', 0)
                pm.setAttr(list + '.visibility', l=True)
            except:
                pass
            
    elif toggleValue == False:
        for list in drivenList:
            try:
                pm.setAttr(list + '.visibility', l=False)
                pm.setAttr(list + '.visibility', 1)
            except:
                pass

def selectRootJoint():
    root = 'root'
    listJNT = [root]
    
    for sel in pm.listRelatives(root, ad=True, type='joint'):
        listJNT.append(str(sel))
    
    pm.select(listJNT)

def createControllerDummy():
    selected = pm.ls(os=True)
    miscGRP = 'misc_grp'
    listLoc = []
    
    if not pm.objExists(miscGRP):
        pm.group(empty=True, n=miscGRP)
        pm.parent(miscGRP, 'rig_grp')
        pm.setAttr(miscGRP + '.visibility', 0)
    
    for sel in selected:
        if not pm.objExists(sel+'_loc_grp'):
            pm.select(d=True)
            loc = pm.spaceLocator(n=sel+'_loc')
            grp = pm.group(loc, n=sel+'_loc_grp')
            pm.parent(grp, miscGRP)
            pm.delete(pm.parentConstraint(sel, grp, mo=False))
            pm.parentConstraint(sel, grp, n=grp+'_pac' , mo=True)
            pm.scaleConstraint('master_anim', grp, n=grp+'_scn' , mo=True)
        
        listLoc.append(sel+'_loc')
    
    pm.select(listLoc)

###

def fixingSpineFKIKFK():
    surfixName = pm.textField('spineNameFirstField', query=True, text=True)
    prefixName = pm.textField('spineNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    torsoHipName = 'torso'
    spine01Name = 'spine_01'
    spine02Name = 'spine_02'
    spine03Name = 'spine_03'
    
    torsoHipAnim = surfixName + torsoHipName + prefixName + '_hip_anim'
    
    torsoHipJoint = surfixName + 'pelvis' + prefixName
    spine01Joint = surfixName + spine01Name + prefixName
    spine02Joint = surfixName + spine02Name + prefixName
    spine03Joint = surfixName + spine03Name + prefixName
    
    torsoHipIkLoc = 'ik_' + surfixName + torsoHipName + prefixName + '_loc'
    spine01IkLoc = 'ik_' + surfixName + spine01Name + prefixName + '_loc'
    spine02IkLoc = 'ik_' + surfixName + spine02Name + prefixName + '_loc'
    spine03IkLoc = 'ik_' + surfixName + spine03Name + prefixName + '_loc'
    
    torsoHipFkLoc = 'fk_' + surfixName + torsoHipName + prefixName + '_loc'
    spine01FkLoc = 'fk_' + surfixName + spine01Name + prefixName + '_loc'
    spine02FkLoc = 'fk_' + surfixName + spine02Name + prefixName + '_loc'
    spine03FkLoc = 'fk_' + surfixName + spine03Name + prefixName + '_loc'
    
    torsoHipFkGRP = surfixName + torsoHipName + prefixName + '_hip_anim_grp'
    spine01FkGRP = 'fk_' + surfixName + spine01Name + prefixName + '_anim_grp'
    spine02FkGRP = 'fk_' + surfixName + spine02Name + prefixName + '_anim_grp'
    spine03FkGRP = 'fk_' + surfixName + spine03Name + prefixName + '_anim_grp'
    
    torsoHipFkOffset = surfixName + torsoHipName + prefixName + '_hip_anim_offset'
    spine01FkOffset = 'fk_' + surfixName + spine01Name + prefixName + '_anim_offset'
    spine02FkOffset = 'fk_' + surfixName + spine02Name + prefixName + '_anim_offset'
    spine03FkOffset = 'fk_' + surfixName + spine03Name + prefixName + '_anim_offset'
    
    torsoHipFkAnim = surfixName + torsoHipName + prefixName + '_hip_anim'
    spine01FkAnim = 'fk_' + surfixName + spine01Name + prefixName + '_anim'
    spine02FkAnim = 'fk_' + surfixName + spine02Name + prefixName + '_anim'
    spine03FkAnim = 'fk_' + surfixName + spine03Name + prefixName + '_anim'
    
    ###
    
    pm.setAttr(torsoHipAnim + '.mode', 1)
    
    pm.spaceLocator(name=torsoHipIkLoc)
    pm.spaceLocator(name=spine01IkLoc)
    pm.spaceLocator(name=spine02IkLoc)
    pm.spaceLocator(name=spine03IkLoc)
    
    pm.delete(pm.parentConstraint(torsoHipJoint, torsoHipIkLoc, mo=False))
    pm.delete(pm.parentConstraint(spine01Joint, spine01IkLoc, mo=False))
    pm.delete(pm.parentConstraint(spine02Joint, spine02IkLoc, mo=False))
    pm.delete(pm.parentConstraint(spine03Joint, spine03IkLoc, mo=False))
    
    pm.spaceLocator(name=torsoHipFkLoc)
    pm.spaceLocator(name=spine01FkLoc)
    pm.spaceLocator(name=spine02FkLoc)
    pm.spaceLocator(name=spine03FkLoc)
    
    pm.delete(pm.parentConstraint(torsoHipFkAnim, torsoHipFkLoc, mo=False))
    pm.delete(pm.parentConstraint(spine01FkAnim, spine01FkLoc, mo=False))
    pm.delete(pm.parentConstraint(spine02FkAnim, spine02FkLoc, mo=False))
    pm.delete(pm.parentConstraint(spine03FkAnim, spine03FkLoc, mo=False))
    
    pm.group(name=torsoHipFkOffset, empty=True)
    pm.group(name=spine01FkOffset, empty=True)
    pm.group(name=spine02FkOffset, empty=True)
    pm.group(name=spine03FkOffset, empty=True)
    
    pm.delete(pm.parentConstraint(torsoHipFkLoc, torsoHipFkOffset, mo=False))
    pm.delete(pm.parentConstraint(spine01FkLoc, spine01FkOffset, mo=False))
    pm.delete(pm.parentConstraint(spine02FkLoc, spine02FkOffset, mo=False))
    pm.delete(pm.parentConstraint(spine03FkLoc, spine03FkOffset, mo=False))
    
    pm.parent(torsoHipFkOffset, torsoHipFkGRP)
    pm.parent(spine01FkOffset, spine01FkGRP)
    pm.parent(spine02FkOffset, spine02FkGRP)
    pm.parent(spine03FkOffset, spine03FkGRP)
    
    pm.parent(torsoHipFkAnim, torsoHipFkOffset)
    pm.parent(spine01FkAnim, spine01FkOffset)
    pm.parent(spine02FkAnim, spine02FkOffset)
    pm.parent(spine03FkAnim, spine03FkOffset)
    
    #pm.delete(pm.parentConstraint(torsoHipIkLoc, torsoHipFkOffset, mo=False))
    pm.delete(pm.parentConstraint(spine01IkLoc, spine01FkOffset, mo=False))
    pm.delete(pm.parentConstraint(spine02IkLoc, spine02FkOffset, mo=False))
    pm.delete(pm.parentConstraint(spine03IkLoc, spine03FkOffset, mo=False))
    
    pm.delete(torsoHipIkLoc)
    pm.delete(spine01IkLoc)
    pm.delete(spine02IkLoc)
    pm.delete(spine03IkLoc)
    
    pm.delete(torsoHipFkLoc)
    pm.delete(spine01FkLoc)
    pm.delete(spine02FkLoc)
    pm.delete(spine03FkLoc)
    
    pm.setAttr(torsoHipAnim + '.mode', 0)

def fixingSpineFKIKIK():
    surfixName = pm.textField('spineNameFirstField', query=True, text=True)
    prefixName = pm.textField('spineNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    spine01Joint = surfixName + 'spine_01' + prefixName
    spine02Joint = surfixName + 'spine_02' + prefixName
    
    spineIK01Joint = 'splineIK_' + surfixName + 'spine_01' + prefixName
    spineIK02Joint = 'splineIK_' + surfixName + 'spine_02' + prefixName
    
    spine01Twist = 'twist_splineIK_' + surfixName + 'spine_01' + prefixName + '_orientConstraint1'
    spine02Twist = 'twist_splineIK_' + surfixName + 'spine_02' + prefixName + '_orientConstraint1'
    
    spine01TwistLoc = surfixName + 'spine_01' + prefixName + '_orientLoc_orientConstraint1'
    spine02TwistLoc = surfixName + 'spine_02' + prefixName + '_orientLoc_orientConstraint1'
    
    ###
    
    #pm.setAttr(spine01Twist + '.' + spine01Joint + '_orientLocW0', 0)
    #pm.setAttr(spine02Twist + '.' + spine02Joint + '_orientLocW0', 0)
    
    pm.setAttr(spine01TwistLoc + '.' + spineIK01Joint + 'W1', 0)
    pm.setAttr(spine02TwistLoc + '.' + spineIK02Joint + 'W1', 0)

###

def fixingArmFKIKFK():
    surfixName = pm.textField('armNameFirstField', query=True, text=True)
    prefixName = pm.textField('armNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    upperArmName = 'upperarm'
    lowerArmName = 'lowerarm'
    handName = 'hand'
    
    upperArmJoint = surfixName + upperArmName + prefixName
    lowerArmJoint = surfixName + lowerArmName + prefixName
    handJoint = surfixName + handName + prefixName
    
    upperArmFkLoc = 'fk_' + surfixName + upperArmName + prefixName + '_loc'
    lowerArmFkLoc = 'fk_' + surfixName + lowerArmName + prefixName + '_loc'
    handFkLoc = 'fk_' + surfixName + handName + prefixName + '_loc'
    
    upperArmFkGRP = 'fk_' + surfixName + upperArmName + prefixName + '_anim_grp'
    lowerArmFkGRP = 'fk_' + surfixName + lowerArmName + prefixName + '_anim_grp'
    handFkGRP = 'fk_' + surfixName + handName + prefixName + '_anim_grp'
    
    upperArmFkOffset = 'fk_' + surfixName + upperArmName + prefixName + '_anim_offset'
    lowerArmFkOffset = 'fk_' + surfixName + lowerArmName + prefixName + '_anim_offset'
    handFkOffset = 'fk_' + surfixName + handName + prefixName + '_anim_offset'
    
    upperArmFkAnim = 'fk_' + surfixName + upperArmName + prefixName + '_anim'
    lowerArmFkAnim = 'fk_' + surfixName + lowerArmName + prefixName + '_anim'
    handFkAnim = 'fk_' + surfixName + handName + prefixName + '_anim'
    
    ###
    
    pm.setAttr(upperArmFkAnim + '.mode', 1)
    
    pm.spaceLocator(name=upperArmFkLoc)
    pm.spaceLocator(name=lowerArmFkLoc)
    pm.spaceLocator(name=handFkLoc)
    
    pm.delete(pm.parentConstraint(upperArmFkAnim, upperArmFkLoc, mo=False))
    pm.delete(pm.parentConstraint(lowerArmFkAnim, lowerArmFkLoc, mo=False))
    pm.delete(pm.parentConstraint(handFkAnim, handFkLoc, mo=False))
    
    if not pm.objExists(upperArmFkOffset):
        pm.group(name=upperArmFkOffset, empty=True)
        pm.group(name=lowerArmFkOffset, empty=True)
        pm.group(name=handFkOffset, empty=True)
    
    pm.delete(pm.parentConstraint(upperArmFkLoc, upperArmFkOffset, mo=False))
    pm.delete(pm.parentConstraint(lowerArmFkLoc, lowerArmFkOffset, mo=False))
    pm.delete(pm.parentConstraint(handFkLoc, handFkOffset, mo=False))
    
    pm.parent(upperArmFkOffset, upperArmFkGRP)
    pm.parent(lowerArmFkOffset, lowerArmFkGRP)
    pm.parent(handFkOffset, handFkGRP)
    
    pm.parent(upperArmFkAnim, upperArmFkOffset)
    pm.parent(lowerArmFkAnim, lowerArmFkOffset)
    pm.parent(handFkAnim, handFkOffset)
    
    pm.delete(pm.parentConstraint(upperArmJoint, upperArmFkOffset, mo=False))
    pm.delete(pm.parentConstraint(lowerArmJoint, lowerArmFkOffset, mo=False))
    pm.delete(pm.parentConstraint(handJoint, handFkOffset, mo=False))
    
    pm.delete(upperArmFkLoc)
    pm.delete(lowerArmFkLoc)
    pm.delete(handFkLoc)
    
    pm.setAttr(upperArmFkAnim + '.mode', 0)

def fixingArmFKIKIK():
    surfixName = pm.textField('armNameFirstField', query=True, text=True)
    prefixName = pm.textField('armNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    upperArmName = 'upperarm'
    lowerArmName = 'lowerarm'
    handName = 'hand'
    
    upperArmJoint = surfixName + upperArmName + prefixName
    lowerArmJoint = surfixName + lowerArmName + prefixName
    handJoint = surfixName + handName + prefixName
    
    upperArmFkLoc = 'fk_' + surfixName + upperArmName + prefixName + '_loc'
    lowerArmFkLoc = 'fk_' + surfixName + lowerArmName + prefixName + '_loc'
    handFkLoc = 'fk_' + surfixName + handName + prefixName + '_loc'
    
    upperArmFkGRP = 'fk_' + surfixName + upperArmName + prefixName + '_anim_grp'
    lowerArmFkGRP = 'fk_' + surfixName + lowerArmName + prefixName + '_anim_grp'
    handFkGRP = 'fk_' + surfixName + handName + prefixName + '_anim_grp'
    
    upperArmFkOffset = 'fk_' + surfixName + upperArmName + prefixName + '_anim_offset'
    lowerArmFkOffset = 'fk_' + surfixName + lowerArmName + prefixName + '_anim_offset'
    handFkOffset = 'fk_' + surfixName + handName + prefixName + '_anim_offset'
    
    upperArmFkAnim = 'fk_' + surfixName + upperArmName + prefixName + '_anim'
    lowerArmFkAnim = 'fk_' + surfixName + lowerArmName + prefixName + '_anim'
    handFkAnim = 'fk_' + surfixName + handName + prefixName + '_anim'
    
    upperArmIkJoint = 'ik_' + surfixName + upperArmName + prefixName + '_jnt'
    lowerArmIkJoint = 'ik_' + surfixName + lowerArmName + prefixName + '_jnt'
    handIkJoint = 'ik_' + surfixName + handName + prefixName + '_jnt'
    handEndIkJoint = 'ik_ik_' + surfixName + handName + prefixName + '_jnt_end_jnt'
    
    ElbowIkAnim = surfixName + 'arm' + prefixName + '_ik_elbow_anim'
    ElbowIkGRP = surfixName + 'arm' + prefixName + '_ik_elbow_anim_space_switcher_follow'
    handIkAnim = 'ik_' + surfixName + handName + prefixName + '_anim'
    
    armIKHandle = surfixName + 'arm' + prefixName + '_rp_arm_ikHandle'
    handIKHandle = 'ik_' + surfixName + 'arm' + prefixName + '_ikHandle'
    
    armCtrlGRP = surfixName + 'arm' + prefixName + '_arm_ik_ctrls_grp'
    handPivot = surfixName + 'arm' + prefixName + '_hand_mid_pivot'
    
    clavicleName = 'clavicle'
    clavicleFKName = 'fk_' + surfixName + clavicleName + prefixName + '_anim'
    clavicleIKName = 'ik_' + surfixName + clavicleName + prefixName + '_anim'
    
    ###
    
    upperarmJointAttr = []
    lowerarmJointAttr = []
    handJointAttr = []
    
    pm.delete(armIKHandle)
    pm.setAttr(handIkAnim + '.mode', 0)
    
    attrs = ['.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.jointOrientX', '.jointOrientY', '.jointOrientZ']
    
    for attr in attrs:
        upperarmJointAttr.append(pm.getAttr(upperArmJoint + attr))
        lowerarmJointAttr.append(pm.getAttr(lowerArmJoint + attr))
        handJointAttr.append(pm.getAttr(handJoint + attr))
    
    for i in range(len(attrs)):
        pm.setAttr(upperArmIkJoint + attrs[i], upperarmJointAttr[i])
        pm.setAttr(lowerArmIkJoint + attrs[i], lowerarmJointAttr[i])
        pm.setAttr(handIkJoint + attrs[i], handJointAttr[i])
    
    angleList = ['.preferredAngleX', '.preferredAngleY', '.preferredAngleZ']
    
    for angle in angleList:
        pm.setAttr(upperArmIkJoint + angle, 0)
        pm.setAttr(lowerArmIkJoint + angle, 0)
        pm.setAttr(handIkJoint + angle, 0)
    
    pm.ikHandle(sj=upperArmIkJoint, ee=handIkJoint, n=armIKHandle)
    pm.ikHandle(sj=handIkJoint, ee=handEndIkJoint, n=handIKHandle)
    
    pm.parent(armIKHandle, handPivot)
    pm.parent(handIKHandle, armIKHandle)
    
    pm.select(d=1)
    createDummyPoleVectorArm([upperArmJoint, lowerArmJoint, handJoint], ElbowIkGRP, armCtrlGRP)
    pm.poleVectorConstraint(ElbowIkAnim, armIKHandle, w=1)
    pm.select(ElbowIkAnim)
    pm.setAttr(handIkAnim + '.mode', 1)
    
    #
    
    pm.setAttr(clavicleFKName + '.translateX', l=False, k=True)
    pm.setAttr(clavicleFKName + '.translateY', l=False, k=True)
    pm.setAttr(clavicleFKName + '.translateZ', l=False, k=True)
    
    pm.setAttr(clavicleIKName + '.rotateX', l=False, k=True)
    pm.setAttr(clavicleIKName + '.rotateY', l=False, k=True)
    pm.setAttr(clavicleIKName + '.rotateZ', l=False, k=True)
    
    pm.setAttr(clavicleIKName + '.clavMode', 0)

###

def fixingLegFKIKFK():
    surfixName = pm.textField('legNameFirstField', query=True, text=True)
    prefixName = pm.textField('legNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    legName = 'leg'
    thighName = 'thigh'
    calfName = 'calf'
    footName = 'foot'
    ballName = 'ball'
    toeName = 'toe'
    
    thighJoint = surfixName + thighName + prefixName
    calfJoint = surfixName + calfName + prefixName
    footJoint = surfixName + footName + prefixName
    ballJoint = surfixName + ballName + prefixName
    toeJoint = surfixName + toeName + prefixName
    
    thighFkLoc = 'fk_' + surfixName + thighName + prefixName + '_loc'
    calfFkLoc = 'fk_' + surfixName + calfName + prefixName + '_loc'
    footFkLoc = 'fk_' + surfixName + footName + prefixName + '_loc'
    ballFkLoc = 'fk_' + surfixName + ballName + prefixName + '_loc'
    
    thighFkGRP = 'fk_' + surfixName + thighName + prefixName + '_anim_grp'
    calfFkGRP = 'fk_' + surfixName + calfName + prefixName + '_anim_grp'
    footFkGRP = 'fk_' + surfixName + footName + prefixName + '_anim_grp'
    ballFkGRP = 'fk_' + surfixName + ballName + prefixName + '_anim_grp'
    
    thighFkOffset = 'fk_' + surfixName + thighName + prefixName + '_anim_offset'
    calfFkOffset = 'fk_' + surfixName + calfName + prefixName + '_anim_offset'
    footFkOffset = 'fk_' + surfixName + footName + prefixName + '_anim_offset'
    ballFkOffset = 'fk_' + surfixName + ballName + prefixName + '_anim_offset'
    
    thighFkAnim = 'fk_' + surfixName + thighName + prefixName + '_anim'
    calfFkAnim = 'fk_' + surfixName + calfName + prefixName + '_anim'
    footFkAnim = 'fk_' + surfixName + footName + prefixName + '_anim'
    ballFkAnim = 'fk_' + surfixName + ballName + prefixName + '_anim'
    
    ###
    
    pm.setAttr(thighFkAnim + '.mode', 1)
    
    pm.spaceLocator(name=thighFkLoc)
    pm.spaceLocator(name=calfFkLoc)
    pm.spaceLocator(name=footFkLoc)
    pm.spaceLocator(name=ballFkLoc)
    
    pm.delete(pm.parentConstraint(thighFkAnim, thighFkLoc, mo=False))
    pm.delete(pm.parentConstraint(calfFkAnim, calfFkLoc, mo=False))
    pm.delete(pm.parentConstraint(footFkAnim, footFkLoc, mo=False))
    pm.delete(pm.parentConstraint(ballFkAnim, ballFkLoc, mo=False))
    
    if not pm.objExists(thighFkOffset):
        pm.group(name=thighFkOffset, empty=True)
        pm.group(name=calfFkOffset, empty=True)
        pm.group(name=footFkOffset, empty=True)
        pm.group(name=ballFkOffset, empty=True)
    
    pm.delete(pm.parentConstraint(thighFkLoc, thighFkOffset, mo=False))
    pm.delete(pm.parentConstraint(calfFkLoc, calfFkOffset, mo=False))
    pm.delete(pm.parentConstraint(footFkLoc, footFkOffset, mo=False))
    pm.delete(pm.parentConstraint(ballFkLoc, ballFkOffset, mo=False))
    
    pm.parent(thighFkOffset, thighFkGRP)
    pm.parent(calfFkOffset, calfFkGRP)
    pm.parent(footFkOffset, footFkGRP)
    pm.parent(ballFkOffset, ballFkGRP)
    
    pm.parent(thighFkAnim, thighFkOffset)
    pm.parent(calfFkAnim, calfFkOffset)
    pm.parent(footFkAnim, footFkOffset)
    pm.parent(ballFkAnim, ballFkOffset)
    
    pm.delete(pm.parentConstraint(thighJoint, thighFkOffset, mo=False))
    pm.delete(pm.parentConstraint(calfJoint, calfFkOffset, mo=False))
    pm.delete(pm.parentConstraint(footJoint, footFkOffset, mo=False))
    pm.delete(pm.parentConstraint(ballJoint, ballFkOffset, mo=False))
    
    pm.delete(thighFkLoc)
    pm.delete(calfFkLoc)
    pm.delete(footFkLoc)
    pm.delete(ballFkLoc)
    
    pm.setAttr(thighFkAnim + '.mode', 0)

def fixingLegFKIKIK():
    surfixName = pm.textField('legNameFirstField', query=True, text=True)
    prefixName = pm.textField('legNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    legName = 'leg'
    thighName = 'thigh'
    calfName = 'calf'
    footName = 'foot'
    ballName = 'ball'
    toeName = 'toe'
    
    legJoint = surfixName + legName + prefixName
    thighJoint = surfixName + thighName + prefixName
    calfJoint = surfixName + calfName + prefixName
    footJoint = surfixName + footName + prefixName
    ballJoint = surfixName + ballName + prefixName
    toeJoint = surfixName + toeName + prefixName
    
    thighJointAttr = []
    calfJointAttr = []
    footJointAttr = []
    ballJointAttr = []
    toeJointAttr = []
    
    thighIkJoint = 'ikV1_' + surfixName + thighName + prefixName + '_joint'
    calfIkJoint = 'ikV1_' + surfixName + calfName + prefixName + '_joint'
    footIkJoint = 'ikV1_' + surfixName + footName + prefixName + '_joint'
    ballIkJoint = 'ikV1_' + surfixName + ballName + prefixName + '_joint'
    toeIkJoint = 'ikV1_' + surfixName + toeName + prefixName + '_joint'
    
    ballIkDrivenJoint = 'ik_' + surfixName + ballName + prefixName + '_driven_joint'
    
    thighFkLoc = 'fk_' + surfixName + thighName + prefixName + '_loc'
    calfFkLoc = 'fk_' + surfixName + calfName + prefixName + '_loc'
    footFkLoc = 'fk_' + surfixName + footName + prefixName + '_loc'
    ballFkLoc = 'fk_' + surfixName + ballName + prefixName + '_loc'
    toeFkLoc = 'fk_' + surfixName + toeName + prefixName + '_loc'
    
    thighIkLoc = 'ik_' + surfixName + thighName + prefixName + '_loc'
    calfIkLoc = 'ik_' + surfixName + calfName + prefixName + '_loc'
    footIkLoc = 'ik_' + surfixName + footName + prefixName + '_loc'
    ballIkLoc = 'ik_' + surfixName + ballName + prefixName + '_loc'
    toeIkLoc = 'ik_' + surfixName + toeName + prefixName + '_loc'
    
    thighFkGRP = 'ik_' + surfixName + thighName + prefixName + '_anim_grp'
    calfFkGRP = 'fk_' + surfixName + calfName + prefixName + '_anim_grp'
    footFkGRP = 'fk_' + surfixName + footName + prefixName + '_anim_grp'
    ballFkGRP = 'fk_' + surfixName + ballName + prefixName + '_anim_grp'
    toeFkGRP = 'fk_' + surfixName + toeName + prefixName + '_anim_grp'
    
    thighFkOffset = 'fk_' + surfixName + thighName + prefixName + '_anim_offset'
    calfFkOffset = 'fk_' + surfixName + calfName + prefixName + '_anim_offset'
    footFkOffset = 'fk_' + surfixName + footName + prefixName + '_anim_offset'
    ballFkOffset = 'fk_' + surfixName + ballName + prefixName + '_anim_offset'
    toeFkOffset = 'fk_' + surfixName + toeName + prefixName + '_anim_offset'
    
    thighFkAnim = 'fk_' + surfixName + thighName + prefixName + '_anim'
    calfFkAnim = 'fk_' + surfixName + calfName + prefixName + '_anim'
    footFkAnim = 'fk_' + surfixName + footName + prefixName + '_anim'
    ballFkAnim = 'fk_' + surfixName + ballName + prefixName + '_anim'
    toeFkAnim = 'fk_' + surfixName + toeName + prefixName + '_anim'
    
    thighIkGRP = 'ik_' + surfixName + thighName + prefixName + '_grp'
    calfIkGRP = 'ik_' + surfixName + calfName + prefixName + '_grp'
    footIkGRP = 'ik_' + surfixName + footName + prefixName + '_grp'
    ballIkGRP = 'ik_' + surfixName + ballName + prefixName + '_grp'
    toeIkGRP = 'ik_' + surfixName + toeName + prefixName + '_grp'
    
    thighIkAnim = 'ik_' + surfixName + thighName + prefixName + '_anim'
    calfIkAnim = 'ik_' + surfixName + calfName + prefixName + '_anim'
    footIkAnim = 'ik_' + surfixName + footName + prefixName + '_anim'
    ballIkAnim = 'ik_' + surfixName + ballName + prefixName + '_anim'
    toeIkAnim = 'ik_' + surfixName + toeName + prefixName + '_anim'
    
    footIKHandleGRP = surfixName + legName + prefixName + '_ik_foot_ball_pivot_grp'
    footIKHandleParent = surfixName + legName + prefixName + '_ik_foot_ball_pivot'
    toeIKHandleParent = surfixName + legName + prefixName + '_toe_wiggle_ctrl'
    
    footIKHandle = surfixName + legName + prefixName + '_noFlip_ikHandle'
    ballIKHandle = surfixName + legName + prefixName + '_ikHandle_ball'
    toeIKHandle = surfixName + legName + prefixName + '_ikHandle_toe'
    
    footIKEffector = surfixName + legName + prefixName + '_noFlip_ikHandle_eff'
    ballIKEffector = surfixName + legName + prefixName + '_ikHandle_ball_eff'
    toeIKEffector = surfixName + legName + prefixName + '_ikHandle_toe_eff'
    
    kneeIkAnim = surfixName + legName + prefixName + '_ik_knee_anim'
    
    ikUpper = 'ik_' + surfixName + footName + prefixName + '_anim_space_switcher_follow'
    ikLower1 = 'ik_' + surfixName + footName + prefixName + '_anim_fkMatchGrp'
    ikLower2 = surfixName + legName + prefixName + '_knee_loc_grp'
    ikLower3 = surfixName + legName + prefixName + '_master_foot_ball_pivot_grp'
    
    ###
    
    pm.parent(ikLower1, w=True)
    pm.parent(ikLower2, w=True)
    pm.parent(ikLower3, w=True)
    loc = pm.spaceLocator(n=footIkAnim + '_LOCTEMP')
    pm.delete(pm.parentConstraint(footIkAnim, loc, mo=False))
    pm.setAttr(loc + '.rotateX', 0)
    pm.setAttr(loc + '.rotateY', 0)
    pm.setAttr(loc + '.rotateZ', 0)
    pm.delete(pm.orientConstraint(loc, ikUpper, mo=False))
    pm.parent(ikLower1, footIkAnim)
    pm.parent(ikLower2, footIkAnim)
    pm.parent(ikLower3, footIkAnim)
    
    pm.delete(footIKHandle)
    pm.delete(ballIKHandle)
    pm.delete(toeIKHandle)
    
    pm.setAttr(thighFkAnim + '.mode', 0)
    pm.setAttr(kneeIkAnim + '.visibility', 0)
    
    #pm.delete(pm.parentConstraint(ballJoint, footIKHandleGRP, mo=False))
    pm.delete(pm.pointConstraint(ballJoint, footIKHandleGRP, mo=False))
    
    attrs = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.jointOrientX', '.jointOrientY', '.jointOrientZ']
    
    for o in range(len(attrs)):
        thighJointAttr.append(pm.getAttr(thighJoint + attrs[o]))
        calfJointAttr.append(pm.getAttr(calfJoint + attrs[o]))
        footJointAttr.append(pm.getAttr(footJoint + attrs[o]))
        ballJointAttr.append(pm.getAttr(ballJoint + attrs[o]))
    
    for i in range(len(attrs)):
        pm.setAttr(thighIkJoint + attrs[i], thighJointAttr[i])
        pm.setAttr(calfIkJoint + attrs[i], calfJointAttr[i])
        pm.setAttr(footIkJoint + attrs[i], footJointAttr[i])
        pm.setAttr(ballIkJoint + attrs[i], ballJointAttr[i])
        pm.setAttr(thighIkJoint + attrs[i], 0)
        pm.setAttr(ballIkDrivenJoint + attrs[i], 0)
    
    pm.ikHandle(sj=thighIkJoint, ee=footIkJoint, name=footIKHandle)
    pm.ikHandle(sj=footIkJoint, ee=ballIkJoint, name=ballIKHandle)
    pm.ikHandle(sj=ballIkJoint, ee=toeIkJoint, name=toeIKHandle)
    
    effectorSelect = pm.listRelatives(thighIkJoint, ad=1, typ="ikEffector")
    effectorSelect = pm.listRelatives(footIkJoint, ad=1, typ="ikEffector")
    effectorSelect = pm.listRelatives(ballIkJoint, ad=1, typ="ikEffector")
    
    pm.rename(effectorSelect, footIKEffector)
    pm.rename(effectorSelect, ballIKEffector)
    pm.rename(effectorSelect, toeIKEffector)
    
    pm.parent(footIKHandle, footIKHandleParent)
    pm.parent(ballIKHandle, footIKHandleParent)
    pm.parent(toeIKHandle, toeIKHandleParent)
    
    pm.setAttr(footIKHandle + '.visibility', 0)
    pm.setAttr(ballIKHandle + '.visibility', 0)
    pm.setAttr(toeIKHandle + '.visibility', 0)
    
    pm.circle(name=calfIkAnim, normalX=0, normalY=0, normalZ=0)
    pm.group(calfIkAnim, name=calfIkGRP)
    pm.parent(calfIkGRP, footIkAnim)
    pm.delete(pm.parentConstraint(calfIkJoint, calfIkGRP, mo=False))
    pm.setAttr(calfIkGRP + '.translateY', pm.getAttr(calfIkGRP + '.translateY') + 10)
    
    createDummyPoleVectorLeg([thighJoint, calfJoint, footJoint], calfIkGRP, footIkAnim)
    pm.poleVectorConstraint(calfIkAnim, footIKHandle, w=1)
    pm.connectAttr(footIkAnim + '.knee_twist', footIKHandle + '.twist')
    
    pm.setAttr(calfIkGRP + '.rotateX', 0)
    pm.setAttr(calfIkGRP + '.rotateY', 0)
    pm.setAttr(calfIkGRP + '.rotateZ', 0)
    
    pm.setAttr(thighFkAnim + '.mode', 1)

###

def fixingChainFKIKIK():
    surfixName = pm.textField('chainNameFirstField', query=True, text=True)
    prefixName = pm.textField('chainNameLastField', query=True, text=True)
    chainMoveValue = pm.intField('chainMoveValue', query=True, value=True)
    
    ###
    
    jointChain = pm.ls(surfixName + '_chain_' + prefixName + '*', type='joint')
    driverChainORN = pm.ls('driver_' + surfixName + '_chain_' + prefixName + '*_orientConstraint1')
    fkChainPAC = pm.ls('fk_' + surfixName + '_chain_' + prefixName + '*_anim_grp_parentConstraint1')
    ikChainORN = pm.ls(surfixName + '_chain_ik_chain_' + prefixName + '*_orientConstraint1')
    ikChain = pm.ls('ik_' + surfixName + '_chain_' + prefixName + '*_anim')
    ikDeformer = surfixName + '_chain_' + prefixName + 'ribbon_wire_deformer'
    
    ###
    
    for a in driverChainORN:
        pm.setAttr(a + '.interpType', 2)
    
    for b in fkChainPAC:
        pm.setAttr(b + '.interpType', 0)
    
    for c in ikChainORN:
        pm.setAttr(c + '.interpType', 0)
        
    for d in range(len(ikChain)):
        pm.select(d=True)
        loc = pm.spaceLocator(n=ikChain[d] + '_LOCTEMP')
        pm.delete(pm.pointConstraint(jointChain[d], loc, mo=False))
        #locValue = pm.getAttr(loc + '.translate')
        #pm.select(ikChain[d])
        #pm.move(locValue[0], locValue[1], locValue[2], rpr=True, spr=True, ws=True)
        #pm.connectAttr(loc + '.translate.translateX', ikChain[d] + '.rotatePivot.rotatePivotX.')
        #pm.connectAttr(loc + '.translate.translateY', ikChain[d] + '.rotatePivot.rotatePivotY.')
        #pm.connectAttr(loc + '.translate.translateZ', ikChain[d] + '.rotatePivot.rotatePivotZ.')
        #pm.connectAttr(loc + '.translate.translateX', ikChain[d] + '.scalePivot.scalePivotX.')
        #pm.connectAttr(loc + '.translate.translateY', ikChain[d] + '.scalePivot.scalePivotY.')
        #pm.connectAttr(loc + '.translate.translateZ', ikChain[d] + '.scalePivot.scalePivotZ.')
        pm.delete(loc)
    
    pm.setAttr(ikDeformer + '.dropoffDistance[0]', chainMoveValue)

###

def fixFile():
    # Delete namespace
    pm.namespace(setNamespace=':')
    namespaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    numRepeat = 1
    toBeDelete = []
    
    for o in namespaces:
        if ':' in str(o):
            oSplit = o.split(':')
            numRepeat = len(oSplit)
    
    for i in range(numRepeat):
        for o in namespaces:
            if str(o) == str('UI'):
                toBeDelete.append(o)
            elif str(o) == str('shared'):
                toBeDelete.append(o)
            else:
                try:
                    pm.namespace(setNamespace=':')
                    pm.namespace(rm=o)
                except:
                    pass
    
    # Delete unused node
    
    mel.eval('MLdeleteUnused;')
    
    # Replace file path
    
    filePathList = cmds.filePathEditor(query=True, listFiles="", attributeOnly=True)
    
    for o in filePathList:
        try:
            pm.filePathEditor(o, replaceField="fullPath", replaceString=("X:/", "P:/"), replaceAll=True)
            pm.filePathEditor(o, replaceField="fullPath", replaceString=("C:/", "P:/"), replaceAll=True)
        except:
            pass
    
    # Unlock jnt_anim
    
    selected = pm.ls('*jnt_anim')
    
    for object in selected:
        selList = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.visibility']
        for b in selList:
            pm.setAttr('{}{}'.format(object, b), l=False, k=True)

def fixWorldAxis():
    pass

def specialQuadrupedSystem():
    pass

###

def createNewGameJoint_Eye(targetOBJ, parentTo):
    findName(targetOBJ)
    jnt = pm.joint(n=targetOBJ[:-4])
    dummy = pm.joint(n='driver_' + targetOBJ[:-4])
    pm.delete(pm.parentConstraint(targetOBJ, jnt, mo=False))
    pm.delete(pm.parentConstraint(targetOBJ, dummy, mo=False))
    pm.parent(jnt, parentTo)
    pm.parent(dummy, 'driver_' + parentTo)
    pm.setAttr(targetOBJ + '.visibility', 0)
    
    pac = pm.parentConstraint(targetOBJ, dummy, n=findNameResult + '_PAC', mo=True)
    scn = pm.scaleConstraint(targetOBJ, dummy, n=findNameResult + '_SCN', mo=True)
    
    for i in ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.scaleX', '.scaleY', '.scaleZ', '.jointOrientX', '.jointOrientY', '.jointOrientZ']:
        try:
            pm.connectAttr(dummy + i, jnt + i)
        except:
            pass

def checkObject_Eye(obj, parentTo):
    if not pm.objExists(obj):
        pm.group(empty=True, n=obj, p=parentTo)

def createControllerDummy_Eye(selected):
    miscGRP = 'misc_grp'
    
    if not pm.objExists(miscGRP):
        pm.group(empty=True, n=miscGRP)
        pm.parent(miscGRP, 'rig_grp')
        pm.setAttr(miscGRP + '.visibility', 0)
    
    if pm.objExists(selected+'_loc_grp'):
        loc = selected+'_loc'
        return loc
    else:
        pm.select(d=True)
        loc = pm.spaceLocator(n=selected+'_loc')
        grp = pm.group(loc, n=selected+'_loc_grp')
        pm.parent(grp, miscGRP)
        pm.delete(pm.parentConstraint(selected, grp, mo=False))
        pm.parentConstraint(selected, grp, n=grp+'_pac' , mo=True)
        pm.scaleConstraint('master_anim', grp, n=grp+'_scn' , mo=True)
        return loc
    
    pm.select(selected)

def importEyeSystem():
    surfixName = pm.textField('headNameFirstField', query=True, text=True)
    prefixName = pm.textField('headNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    headController = surfixName + 'head' + prefixName
    leftEyes = pm.textField('eyeLeftNameField', query=True, text=True)
    rightEyes = pm.textField('eyeRightNameField', query=True, text=True)
    
    ###
    
    fileLocation = 'C:/Users/user/Documents/maya/projects/Dofala/scenes/eyesShape.ma'
    
    if not pm.objExists('M_IK_eyeAim_pos'):
        cmds.file(fileLocation, i=True)
    
    eyesCenterGRP = 'M_IK_eyeAim_aut'
    eyesLeftGRP = 'L_IK_eyeAim_ctl_pos'
    eyesRightGRP = 'R_IK_eyeAim_ctl_pos'
    
    eyesLeftLOC = 'L_IK_eye_jnt_aim'
    eyesRightLOC = 'R_IK_eye_jnt_aim'
    
    eyesLeftANN = 'L_IK_eye_jnt_ann'
    eyesRightANN = 'R_IK_eye_jnt_ann'
    
    leftEyesGRP = leftEyes + '_grp'
    rightEyesGRP = rightEyes + '_grp'
    
    headPointer = createControllerDummy_Eye(headController)
    leftEyesPointer = createControllerDummy_Eye(leftEyes)
    rightEyesPointer = createControllerDummy_Eye(rightEyes)
    
    ###
    
    try:
        pm.delete(eyesCenterGRP.replace('_aut', '_aut_pac'))
        pm.delete(eyesLeftANN.replace('_ann', '_ann_pac'))
        pm.delete(eyesRightANN.replace('_ann', '_ann_pac'))
        pm.delete(leftEyesGRP.replace('_grp', '_grp_pac'))
        pm.delete(rightEyesGRP.replace('_grp', '_grp_pac'))
    except:
        pass
    
    pm.delete(pm.pointConstraint(leftEyesPointer, rightEyesPointer, eyesCenterGRP, mo=False))
    pm.delete(pm.pointConstraint(leftEyesPointer, eyesLeftGRP, mo=False))
    pm.delete(pm.pointConstraint(rightEyesPointer, eyesRightGRP, mo=False))
    
    pm.setAttr(eyesCenterGRP + '.translateZ', pm.getAttr(eyesCenterGRP + '.translateZ') + 25)
    
    pm.delete(pm.pointConstraint(leftEyesPointer, eyesLeftANN, mo=False))
    pm.delete(pm.pointConstraint(rightEyesPointer, eyesRightANN, mo=False))
    
    pm.parentConstraint(headPointer, eyesCenterGRP, n=eyesCenterGRP.replace('_aut', '_aut_pac'), mo=True)
    pm.parentConstraint(headPointer, eyesLeftANN, n=eyesLeftANN.replace('_ann', '_ann_pac'), mo=True)
    pm.parentConstraint(headPointer, eyesRightANN, n=eyesRightANN.replace('_ann', '_ann_pac'), mo=True)
    
    aimLeft = pm.aimConstraint(eyesLeftLOC, leftEyesGRP, n=leftEyesGRP.replace('_grp', '_grp_pac'), mo=True)
    aimRight = pm.aimConstraint(eyesRightLOC, rightEyesGRP, n=rightEyesGRP.replace('_grp', '_grp_pac'), mo=True)
    
    for aim in [aimLeft, aimRight]:
        pm.setAttr(aim + '.offsetX', 0)
        pm.setAttr(aim + '.offsetY', 0)
        pm.setAttr(aim + '.offsetZ', 0)
        
        pm.setAttr(aim + '.aimVectorX', 0)
        pm.setAttr(aim + '.aimVectorY', 0)
        pm.setAttr(aim + '.aimVectorZ', 1)
        
        pm.setAttr(aim + '.upVectorX', 0)
        pm.setAttr(aim + '.upVectorY', 0)
        pm.setAttr(aim + '.upVectorZ', 1)
        
        pm.setAttr(aim + '.worldUpVectorX', 0)
        pm.setAttr(aim + '.worldUpVectorY', 1)
        pm.setAttr(aim + '.worldUpVectorZ', 0)
    
    # Iris Size
    
    try:
        pm.delete('*eyeball_L_grp_parentConstraint1')
        pm.delete('*eyeball_L_grp_scaleConstraint1')
        pm.delete('*eyeball_R_grp_parentConstraint1')
        pm.delete('*eyeball_R_grp_scaleConstraint1')
        
        pm.delete('*eye_L_GRP_parentConstraint')
        pm.delete('*eye_L_GRP_scaleConstraint')
        pm.delete('*eye_R_GRP_parentConstraint')
        pm.delete('*eye_R_GRP_scaleConstraint')
    except:
        pass
    
    aimGRP = 'M_IK_eyeAim_pos'
    irisGRP = 'eyeIris_controller_grp'
    
    aimLeft = 'L_IK_eyeAim_ctl'
    aimRight = 'R_IK_eyeAim_ctl'
    irisLeft = 'L_eyeIris_0_ctl'
    irisRight = 'R_eyeIris_0_ctl'
    
    pm.parent(aimGRP, 'offset_anim')
    pm.parent(irisGRP, 'offset_anim')
    pm.setAttr(irisGRP + '.visibility', 0)
    
    if not pm.attributeQuery('irisSize', node=aimLeft, ex=True):
        pm.addAttr(aimLeft, ln='irisSize', k=True, min=-1, max=1, dv=0)
    if not pm.attributeQuery('irisSize', node=aimRight, ex=True):
        pm.addAttr(aimRight, ln='irisSize', k=True, min=-1, max=1, dv=0)
    
    def sdk(driver, driven, valueL, moveL):
        pm.setDrivenKeyframe(driven, cd=driver, itt='linear', ott='linear', dv=valueL[0], v=moveL[0])
        pm.setDrivenKeyframe(driven, cd=driver, itt='linear', ott='linear', dv=valueL[1], v=moveL[1])
        pm.setDrivenKeyframe(driven, cd=driver, itt='linear', ott='linear', dv=valueL[2], v=moveL[2])
    
    dv = pm.getAttr(irisLeft + '.irisSize')
    sdk(aimLeft + '.irisSize', irisLeft + '.irisSize', [-1, 0, 1], [-1, dv, 1])
    dv = pm.getAttr(irisRight + '.irisSize')
    sdk(aimRight + '.irisSize', irisRight + '.irisSize', [-1, 0, 1], [-1, dv, 1])

def createEyeSystem01():
    surfixName = pm.textField('headNameFirstField', query=True, text=True)
    prefixName = pm.textField('headNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    headController = 'fk_' + surfixName + 'head' + prefixName + '_anim'
    leftEyes = pm.textField('eyeLeftNameField', query=True, text=True)
    rightEyes = pm.textField('eyeRightNameField', query=True, text=True)
    
    rigExtraGRP = 'rig_extra_grp'
    centerEyesRigGRP = 'eyesRig_c_grp'
    leftEyesRigGRP = 'eyesRig_l_grp'
    rightEyesRigGRP = 'eyesRig_r_grp'
    centerEyesRigTRN = 'eyesRig_c_trn'
    leftEyesRigTRN = 'eyesRig_l_trn'
    rightEyesRigTRN = 'eyesRig_r_trn'
    
    headJNT = surfixName + 'head' + prefixName
    
    checkObject_Eye(rigExtraGRP, 'offset_anim')
    checkObject_Eye(centerEyesRigGRP, rigExtraGRP)
    checkObject_Eye(leftEyesRigGRP, centerEyesRigGRP)
    checkObject_Eye(rightEyesRigGRP, centerEyesRigGRP)
    checkObject_Eye(centerEyesRigTRN, rigExtraGRP)
    checkObject_Eye(leftEyesRigTRN, centerEyesRigTRN)
    checkObject_Eye(rightEyesRigTRN, centerEyesRigTRN)
    
    headPointer = createControllerDummy_Eye(headController)
    leftEyesPointer = createControllerDummy_Eye(leftEyes)
    rightEyesPointer = createControllerDummy_Eye(rightEyes)
    
    try:
        pm.parentConstraint(headPointer, centerEyesRigGRP, n=centerEyesRigGRP.replace('_grp', '_grp_pac'), mo=True)
    except:
        pass
    
    sides = ['_l', '_r']
    nameCTL = '_anim'
    nameGRP = '_grp'
    nameJNT = '_jnt'
    nameTRN = '_trn'
    
    for side in sides:
        blinkUpper1CTL = 'eye_blink_upper_1' + side + nameCTL
        blinkUpper2CTL = 'eye_blink_upper_2' + side + nameCTL
        blinkUpper3CTL = 'eye_blink_upper_3' + side + nameCTL
        blinkLower1CTL = 'eye_blink_lower_1' + side + nameCTL
        blinkLower2CTL = 'eye_blink_lower_2' + side + nameCTL
        blinkLower3CTL = 'eye_blink_lower_3' + side + nameCTL
        
        blinkUpper1GRP = 'eye_blink_upper_1' + side + nameGRP
        blinkUpper2GRP = 'eye_blink_upper_2' + side + nameGRP
        blinkUpper3GRP = 'eye_blink_upper_3' + side + nameGRP
        blinkLower1GRP = 'eye_blink_lower_1' + side + nameGRP
        blinkLower2GRP = 'eye_blink_lower_2' + side + nameGRP
        blinkLower3GRP = 'eye_blink_lower_3' + side + nameGRP
        
        blinkUpper1JNT = 'eye_blink_upper_1' + side + nameJNT
        blinkUpper2JNT = 'eye_blink_upper_2' + side + nameJNT
        blinkUpper3JNT = 'eye_blink_upper_3' + side + nameJNT
        blinkLower1JNT = 'eye_blink_lower_1' + side + nameJNT
        blinkLower2JNT = 'eye_blink_lower_2' + side + nameJNT
        blinkLower3JNT = 'eye_blink_lower_3' + side + nameJNT
        
        blinkUpper1TRN = 'eye_blink_upper_1' + side + nameTRN
        blinkUpper2TRN = 'eye_blink_upper_2' + side + nameTRN
        blinkUpper3TRN = 'eye_blink_upper_3' + side + nameTRN
        blinkLower1TRN = 'eye_blink_lower_1' + side + nameTRN
        blinkLower2TRN = 'eye_blink_lower_2' + side + nameTRN
        blinkLower3TRN = 'eye_blink_lower_3' + side + nameTRN
        
        pm.select(d=True)
        
        pm.circle(n=blinkUpper1CTL)
        pm.circle(n=blinkUpper2CTL)
        pm.circle(n=blinkUpper3CTL)
        pm.circle(n=blinkLower1CTL)
        pm.circle(n=blinkLower2CTL)
        pm.circle(n=blinkLower3CTL)
        
        pm.select(d=True)
        
        pm.group(empty=True, n=blinkUpper1GRP)
        pm.group(empty=True, n=blinkUpper2GRP)
        pm.group(empty=True, n=blinkUpper3GRP)
        pm.group(empty=True, n=blinkLower1GRP)
        pm.group(empty=True, n=blinkLower2GRP)
        pm.group(empty=True, n=blinkLower3GRP)
        
        pm.select(d=True)
        
        pm.joint(n=blinkUpper1JNT)
        pm.joint(n=blinkUpper2JNT)
        pm.joint(n=blinkUpper3JNT)
        pm.joint(n=blinkLower1JNT)
        pm.joint(n=blinkLower2JNT)
        pm.joint(n=blinkLower3JNT)
        
        pm.select(d=True)
        
        pm.group(empty=True, n=blinkUpper1TRN)
        pm.group(empty=True, n=blinkUpper2TRN)
        pm.group(empty=True, n=blinkUpper3TRN)
        pm.group(empty=True, n=blinkLower1TRN)
        pm.group(empty=True, n=blinkLower2TRN)
        pm.group(empty=True, n=blinkLower3TRN)
        
        #
        
        pm.parent(blinkUpper1CTL, blinkUpper1GRP)
        pm.parent(blinkUpper2CTL, blinkUpper2GRP)
        pm.parent(blinkUpper3CTL, blinkUpper3GRP)
        pm.parent(blinkLower1CTL, blinkLower1GRP)
        pm.parent(blinkLower2CTL, blinkLower2GRP)
        pm.parent(blinkLower3CTL, blinkLower3GRP)
        
        pm.parent(blinkUpper1JNT, blinkUpper1TRN)
        pm.parent(blinkUpper2JNT, blinkUpper2TRN)
        pm.parent(blinkUpper3JNT, blinkUpper3TRN)
        pm.parent(blinkLower1JNT, blinkLower1TRN)
        pm.parent(blinkLower2JNT, blinkLower2TRN)
        pm.parent(blinkLower3JNT, blinkLower3TRN)
        
        if side == '_l':
            pm.parent(blinkUpper1GRP, leftEyesRigGRP)
            pm.parent(blinkUpper2GRP, leftEyesRigGRP)
            pm.parent(blinkUpper3GRP, leftEyesRigGRP)
            pm.parent(blinkLower1GRP, leftEyesRigGRP)
            pm.parent(blinkLower2GRP, leftEyesRigGRP)
            pm.parent(blinkLower3GRP, leftEyesRigGRP)
            
            pm.parent(blinkUpper1TRN, leftEyesRigTRN)
            pm.parent(blinkUpper2TRN, leftEyesRigTRN)
            pm.parent(blinkUpper3TRN, leftEyesRigTRN)
            pm.parent(blinkLower1TRN, leftEyesRigTRN)
            pm.parent(blinkLower2TRN, leftEyesRigTRN)
            pm.parent(blinkLower3TRN, leftEyesRigTRN)
        
        if side == '_r':
            pm.parent(blinkUpper1GRP, rightEyesRigGRP)
            pm.parent(blinkUpper2GRP, rightEyesRigGRP)
            pm.parent(blinkUpper3GRP, rightEyesRigGRP)
            pm.parent(blinkLower1GRP, rightEyesRigGRP)
            pm.parent(blinkLower2GRP, rightEyesRigGRP)
            pm.parent(blinkLower3GRP, rightEyesRigGRP)
            
            pm.parent(blinkUpper1TRN, rightEyesRigTRN)
            pm.parent(blinkUpper2TRN, rightEyesRigTRN)
            pm.parent(blinkUpper3TRN, rightEyesRigTRN)
            pm.parent(blinkLower1TRN, rightEyesRigTRN)
            pm.parent(blinkLower2TRN, rightEyesRigTRN)
            pm.parent(blinkLower3TRN, rightEyesRigTRN)
        
        #
        
        if side == '_l':
            pm.delete(pm.pointConstraint(leftEyes, blinkUpper1GRP, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkUpper2GRP, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkUpper3GRP, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkLower1GRP, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkLower2GRP, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkLower3GRP, mo=False))
            
            pm.delete(pm.pointConstraint(leftEyes, blinkUpper1TRN, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkUpper2TRN, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkUpper3TRN, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkLower1TRN, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkLower2TRN, mo=False))
            pm.delete(pm.pointConstraint(leftEyes, blinkLower3TRN, mo=False))
            '''
            pm.delete(pm.pointConstraint(leftUpperEyes, blinkUpper1TRN, mo=False))
            pm.delete(pm.pointConstraint(leftUpperEyes, blinkUpper2TRN, mo=False))
            pm.delete(pm.pointConstraint(leftUpperEyes, blinkUpper3TRN, mo=False))
            pm.delete(pm.pointConstraint(leftLowerEyes, blinkLower1TRN, mo=False))
            pm.delete(pm.pointConstraint(leftLowerEyes, blinkLower2TRN, mo=False))
            pm.delete(pm.pointConstraint(leftLowerEyes, blinkLower3TRN, mo=False))
            '''
        
        if side == '_r':
            pm.delete(pm.pointConstraint(rightEyes, blinkUpper1GRP, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkUpper2GRP, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkUpper3GRP, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkLower1GRP, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkLower2GRP, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkLower3GRP, mo=False))
            
            pm.delete(pm.pointConstraint(rightEyes, blinkUpper1TRN, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkUpper2TRN, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkUpper3TRN, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkLower1TRN, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkLower2TRN, mo=False))
            pm.delete(pm.pointConstraint(rightEyes, blinkLower3TRN, mo=False))
            '''
            pm.delete(pm.pointConstraint(rightUpperEyes, blinkUpper1TRN, mo=False))
            pm.delete(pm.pointConstraint(rightUpperEyes, blinkUpper2TRN, mo=False))
            pm.delete(pm.pointConstraint(rightUpperEyes, blinkUpper3TRN, mo=False))
            pm.delete(pm.pointConstraint(rightLowerEyes, blinkLower1TRN, mo=False))
            pm.delete(pm.pointConstraint(rightLowerEyes, blinkLower2TRN, mo=False))
            pm.delete(pm.pointConstraint(rightLowerEyes, blinkLower3TRN, mo=False))
            '''
        
        pm.setAttr(blinkUpper1TRN + '.translateY', pm.getAttr(blinkUpper1TRN + '.translateY') + 0.5)
        pm.setAttr(blinkUpper2TRN + '.translateY', pm.getAttr(blinkUpper2TRN + '.translateY') + 1.0)
        pm.setAttr(blinkUpper3TRN + '.translateY', pm.getAttr(blinkUpper3TRN + '.translateY') + 1.5)
        pm.setAttr(blinkLower1TRN + '.translateY', pm.getAttr(blinkLower1TRN + '.translateY') + -0.5)
        pm.setAttr(blinkLower2TRN + '.translateY', pm.getAttr(blinkLower2TRN + '.translateY') + -1.0)
        pm.setAttr(blinkLower3TRN + '.translateY', pm.getAttr(blinkLower3TRN + '.translateY') + -1.5)
        
        dummyCenterLOC = pm.spaceLocator(n='dummy_c_loc')
        '''
        if side == '_l':
            pm.delete(pm.pointConstraint(leftInEyes, leftOutEyes, dummyCenterLOC, mo=False))
        
        if side == '_r':
            pm.delete(pm.pointConstraint(rightInEyes, rightOutEyes, dummyCenterLOC, mo=False))
        '''
        '''
        pm.delete(pm.aimConstraint(dummyCenterLOC, blinkUpper1GRP, mo=False))
        pm.delete(pm.aimConstraint(dummyCenterLOC, blinkUpper2GRP, mo=False))
        pm.delete(pm.aimConstraint(dummyCenterLOC, blinkUpper3GRP, mo=False))
        pm.delete(pm.aimConstraint(dummyCenterLOC, blinkLower1GRP, mo=False))
        pm.delete(pm.aimConstraint(dummyCenterLOC, blinkLower2GRP, mo=False))
        pm.delete(pm.aimConstraint(dummyCenterLOC, blinkLower3GRP, mo=False))
        '''
        pm.delete(dummyCenterLOC)

def createEyeSystem02():
    surfixName = pm.textField('headNameFirstField', query=True, text=True)
    prefixName = pm.textField('headNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    headController = 'fk_' + surfixName + 'head' + prefixName + '_anim'
    leftEyes = pm.textField('eyeLeftNameField', query=True, text=True)
    rightEyes = pm.textField('eyeRightNameField', query=True, text=True)
    
    rigExtraGRP = 'rig_extra_grp'
    centerEyesRigGRP = 'eyesRig_c_grp'
    leftEyesRigGRP = 'eyesRig_l_grp'
    rightEyesRigGRP = 'eyesRig_r_grp'
    centerEyesRigTRN = 'eyesRig_c_trn'
    leftEyesRigTRN = 'eyesRig_l_trn'
    rightEyesRigTRN = 'eyesRig_r_trn'
    
    headPointer = headController + '_loc'
    leftEyesPointer = leftEyes + '_loc'
    rightEyesPointer = rightEyes + '_loc'
    headJNT = surfixName + 'head' + prefixName
    
    sides = ['_l', '_r']
    nameCTL = '_anim'
    nameGRP = '_grp'
    nameJNT = '_jnt'
    nameTRN = '_trn'
    
    eyesCenterCTL = 'M_IK_eyeAim_ctl'
    pm.addAttr(eyesCenterCTL, ln='eyelidFollow', at='bool', k=True, dv=False)
    
    for side in sides:
        blinkUpper1CTL = 'eye_blink_upper_1' + side + nameCTL
        blinkUpper2CTL = 'eye_blink_upper_2' + side + nameCTL
        blinkUpper3CTL = 'eye_blink_upper_3' + side + nameCTL
        blinkLower1CTL = 'eye_blink_lower_1' + side + nameCTL
        blinkLower2CTL = 'eye_blink_lower_2' + side + nameCTL
        blinkLower3CTL = 'eye_blink_lower_3' + side + nameCTL
        
        blinkUpper1GRP = 'eye_blink_upper_1' + side + nameGRP
        blinkUpper2GRP = 'eye_blink_upper_2' + side + nameGRP
        blinkUpper3GRP = 'eye_blink_upper_3' + side + nameGRP
        blinkLower1GRP = 'eye_blink_lower_1' + side + nameGRP
        blinkLower2GRP = 'eye_blink_lower_2' + side + nameGRP
        blinkLower3GRP = 'eye_blink_lower_3' + side + nameGRP
        
        blinkUpper1JNT = 'eye_blink_upper_1' + side + nameJNT
        blinkUpper2JNT = 'eye_blink_upper_2' + side + nameJNT
        blinkUpper3JNT = 'eye_blink_upper_3' + side + nameJNT
        blinkLower1JNT = 'eye_blink_lower_1' + side + nameJNT
        blinkLower2JNT = 'eye_blink_lower_2' + side + nameJNT
        blinkLower3JNT = 'eye_blink_lower_3' + side + nameJNT
        
        blinkUpper1TRN = 'eye_blink_upper_1' + side + nameTRN
        blinkUpper2TRN = 'eye_blink_upper_2' + side + nameTRN
        blinkUpper3TRN = 'eye_blink_upper_3' + side + nameTRN
        blinkLower1TRN = 'eye_blink_lower_1' + side + nameTRN
        blinkLower2TRN = 'eye_blink_lower_2' + side + nameTRN
        blinkLower3TRN = 'eye_blink_lower_3' + side + nameTRN
        
        attrs = ['.rotateX', '.rotateY', '.rotateZ']
        
        for attr in attrs:
            pm.setAttr(blinkUpper1TRN + attr, pm.getAttr(blinkUpper1GRP + attr))
            pm.setAttr(blinkUpper2TRN + attr, pm.getAttr(blinkUpper2GRP + attr))
            pm.setAttr(blinkUpper3TRN + attr, pm.getAttr(blinkUpper3GRP + attr))
            pm.setAttr(blinkLower1TRN + attr, pm.getAttr(blinkLower1GRP + attr))
            pm.setAttr(blinkLower2TRN + attr, pm.getAttr(blinkLower2GRP + attr))
            pm.setAttr(blinkLower3TRN + attr, pm.getAttr(blinkLower3GRP + attr))
        
        pm.parentConstraint(blinkUpper1CTL, blinkUpper1TRN, n=blinkUpper1TRN.replace('_trn', '_trn_pac'), mo=True)
        pm.parentConstraint(blinkUpper2CTL, blinkUpper2TRN, n=blinkUpper2TRN.replace('_trn', '_trn_pac'), mo=True)
        pm.parentConstraint(blinkUpper3CTL, blinkUpper3TRN, n=blinkUpper3TRN.replace('_trn', '_trn_pac'), mo=True)
        pm.parentConstraint(blinkLower1CTL, blinkLower1TRN, n=blinkLower1TRN.replace('_trn', '_trn_pac'), mo=True)
        pm.parentConstraint(blinkLower2CTL, blinkLower2TRN, n=blinkLower2TRN.replace('_trn', '_trn_pac'), mo=True)
        pm.parentConstraint(blinkLower3CTL, blinkLower3TRN, n=blinkLower3TRN.replace('_trn', '_trn_pac'), mo=True)
        
        pm.scaleConstraint(blinkUpper1CTL, blinkUpper1TRN, n=blinkUpper1TRN.replace('_trn', '_trn_scn'), mo=True)
        pm.scaleConstraint(blinkUpper2CTL, blinkUpper2TRN, n=blinkUpper2TRN.replace('_trn', '_trn_scn'), mo=True)
        pm.scaleConstraint(blinkUpper3CTL, blinkUpper3TRN, n=blinkUpper3TRN.replace('_trn', '_trn_scn'), mo=True)
        pm.scaleConstraint(blinkLower1CTL, blinkLower1TRN, n=blinkLower1TRN.replace('_trn', '_trn_scn'), mo=True)
        pm.scaleConstraint(blinkLower2CTL, blinkLower2TRN, n=blinkLower2TRN.replace('_trn', '_trn_scn'), mo=True)
        pm.scaleConstraint(blinkLower3CTL, blinkLower3TRN, n=blinkLower3TRN.replace('_trn', '_trn_scn'), mo=True)
        
        #
            
        if side == '_l':
            uPAC1 = pm.parentConstraint(leftEyesPointer, headPointer, blinkUpper1GRP, n=blinkUpper1GRP.replace('_grp', '_grp_pac'), mo=True)
            uPAC2 = pm.parentConstraint(blinkUpper1CTL, headPointer, blinkUpper2GRP, n=blinkUpper2GRP.replace('_grp', '_grp_pac'), mo=True)
            uPAC3 = pm.parentConstraint(blinkUpper1CTL, headPointer, blinkUpper3GRP, n=blinkUpper3GRP.replace('_grp', '_grp_pac'), mo=True)
            lPAC1 = pm.parentConstraint(leftEyesPointer, headPointer, blinkLower1GRP, n=blinkLower1GRP.replace('_grp', '_grp_pac'), mo=True)
            lPAC2 = pm.parentConstraint(blinkLower1CTL, headPointer, blinkLower2GRP, n=blinkLower2GRP.replace('_grp', '_grp_pac'), mo=True)
            lPAC3 = pm.parentConstraint(blinkLower1CTL, headPointer, blinkLower3GRP, n=blinkLower3GRP.replace('_grp', '_grp_pac'), mo=True)
            
            pm.setAttr(uPAC1 + '.' + leftEyesPointer + 'W0', 1.0)
            pm.setAttr(uPAC1 + '.' + headPointer + 'W1', 1.0)
            
            pm.setAttr(uPAC2 + '.' + blinkUpper1CTL + 'W0', 1.0)
            pm.setAttr(uPAC2 + '.' + headPointer + 'W1', 0.5)
            
            pm.setAttr(uPAC3 + '.' + blinkUpper1CTL + 'W0', 0.5)
            pm.setAttr(uPAC3 + '.' + headPointer + 'W1', 1.0)
            
            pm.setAttr(lPAC1 + '.' + leftEyesPointer + 'W0', 1.0)
            pm.setAttr(lPAC1 + '.' + headPointer + 'W1', 1.0)
            
            pm.setAttr(lPAC2 + '.' + blinkLower1CTL + 'W0', 1.0)
            pm.setAttr(lPAC2 + '.' + headPointer + 'W1', 0.5)
            
            pm.setAttr(lPAC3 + '.' + blinkLower1CTL + 'W0', 0.5)
            pm.setAttr(lPAC3 + '.' + headPointer + 'W1', 1.0)
            
            uSCN2 = pm.scaleConstraint(blinkUpper1CTL, headPointer, blinkUpper2GRP, n=blinkUpper2GRP.replace('_grp', '_grp_scn'), mo=True)
            uSCN3 = pm.scaleConstraint(blinkUpper1CTL, headPointer, blinkUpper3GRP, n=blinkUpper3GRP.replace('_grp', '_grp_scn'), mo=True)
            lSCN2 = pm.scaleConstraint(blinkLower1CTL, headPointer, blinkLower2GRP, n=blinkLower2GRP.replace('_grp', '_grp_scn'), mo=True)
            lSCN3 = pm.scaleConstraint(blinkLower1CTL, headPointer, blinkLower3GRP, n=blinkLower3GRP.replace('_grp', '_grp_scn'), mo=True)
            
            pm.setAttr(uSCN2 + '.' + blinkUpper1CTL + 'W0', 1.0)
            pm.setAttr(uSCN2 + '.' + headPointer + 'W1', 0.5)
            
            pm.setAttr(uSCN3 + '.' + blinkUpper1CTL + 'W0', 0.5)
            pm.setAttr(uSCN3 + '.' + headPointer + 'W1', 1.0)
            
            pm.setAttr(lSCN2 + '.' + blinkLower1CTL + 'W0', 1.0)
            pm.setAttr(lSCN2 + '.' + headPointer + 'W1', 0.5)
            
            pm.setAttr(lSCN3 + '.' + blinkLower1CTL + 'W0', 0.5)
            pm.setAttr(lSCN3 + '.' + headPointer + 'W1', 1.0)
            
            #
            
            pm.connectAttr(eyesCenterCTL + '.eyelidFollow', uPAC1 + '.' + leftEyesPointer + 'W0')
            pm.connectAttr(eyesCenterCTL + '.eyelidFollow', uPAC1 + '.' + headPointer + 'W1')
            pm.connectAttr(eyesCenterCTL + '.eyelidFollow', lPAC1 + '.' + leftEyesPointer + 'W0')
            pm.connectAttr(eyesCenterCTL + '.eyelidFollow', lPAC1 + '.' + headPointer + 'W1')
        
        if side == '_r':
            uPAC1 = pm.parentConstraint(rightEyesPointer, headPointer, blinkUpper1GRP, n=blinkUpper1GRP.replace('_grp', '_grp_pac'), mo=True)
            uPAC2 = pm.parentConstraint(blinkUpper1CTL, headPointer, blinkUpper2GRP, n=blinkUpper2GRP.replace('_grp', '_grp_pac'), mo=True)
            uPAC3 = pm.parentConstraint(blinkUpper1CTL, headPointer, blinkUpper3GRP, n=blinkUpper3GRP.replace('_grp', '_grp_pac'), mo=True)
            lPAC1 = pm.parentConstraint(rightEyesPointer, headPointer, blinkLower1GRP, n=blinkLower1GRP.replace('_grp', '_grp_pac'), mo=True)
            lPAC2 = pm.parentConstraint(blinkLower1CTL, headPointer, blinkLower2GRP, n=blinkLower2GRP.replace('_grp', '_grp_pac'), mo=True)
            lPAC3 = pm.parentConstraint(blinkLower1CTL, headPointer, blinkLower3GRP, n=blinkLower3GRP.replace('_grp', '_grp_pac'), mo=True)
            
            pm.setAttr(uPAC1 + '.' + rightEyesPointer + 'W0', 1.0)
            pm.setAttr(uPAC1 + '.' + headPointer + 'W1', 1.0)
            
            pm.setAttr(uPAC2 + '.' + blinkUpper1CTL + 'W0', 1.0)
            pm.setAttr(uPAC2 + '.' + headPointer + 'W1', 0.5)
            
            pm.setAttr(uPAC3 + '.' + blinkUpper1CTL + 'W0', 0.5)
            pm.setAttr(uPAC3 + '.' + headPointer + 'W1', 1.0)
            
            pm.setAttr(lPAC1 + '.' + rightEyesPointer + 'W0', 1.0)
            pm.setAttr(lPAC1 + '.' + headPointer + 'W1', 1.0)
            
            pm.setAttr(lPAC2 + '.' + blinkLower1CTL + 'W0', 1.0)
            pm.setAttr(lPAC2 + '.' + headPointer + 'W1', 0.5)
            
            pm.setAttr(lPAC3 + '.' + blinkLower1CTL + 'W0', 0.5)
            pm.setAttr(lPAC3 + '.' + headPointer + 'W1', 1.0)
            
            uSCN2 = pm.scaleConstraint(blinkUpper1CTL, headPointer, blinkUpper2GRP, n=blinkUpper2GRP.replace('_grp', '_grp_scn'), mo=True)
            uSCN3 = pm.scaleConstraint(blinkUpper1CTL, headPointer, blinkUpper3GRP, n=blinkUpper3GRP.replace('_grp', '_grp_scn'), mo=True)
            lSCN2 = pm.scaleConstraint(blinkLower1CTL, headPointer, blinkLower2GRP, n=blinkLower2GRP.replace('_grp', '_grp_scn'), mo=True)
            lSCN3 = pm.scaleConstraint(blinkLower1CTL, headPointer, blinkLower3GRP, n=blinkLower3GRP.replace('_grp', '_grp_scn'), mo=True)
            
            pm.setAttr(uSCN2 + '.' + blinkUpper1CTL + 'W0', 1.0)
            pm.setAttr(uSCN2 + '.' + headPointer + 'W1', 0.5)
            
            pm.setAttr(uSCN3 + '.' + blinkUpper1CTL + 'W0', 0.5)
            pm.setAttr(uSCN3 + '.' + headPointer + 'W1', 1.0)
            
            pm.setAttr(lSCN2 + '.' + blinkLower1CTL + 'W0', 1.0)
            pm.setAttr(lSCN2 + '.' + headPointer + 'W1', 0.5)
            
            pm.setAttr(lSCN3 + '.' + blinkLower1CTL + 'W0', 0.5)
            pm.setAttr(lSCN3 + '.' + headPointer + 'W1', 1.0)
            
            #
            
            pm.setAttr(uPAC2 + '.interpType', 0)
            pm.setAttr(uPAC3 + '.interpType', 0)
            pm.setAttr(lPAC2 + '.interpType', 0)
            pm.setAttr(lPAC3 + '.interpType', 0)
            
            #
            
            pm.connectAttr(eyesCenterCTL + '.eyelidFollow', uPAC1 + '.' + rightEyesPointer + 'W0')
            pm.connectAttr(eyesCenterCTL + '.eyelidFollow', uPAC1 + '.' + headPointer + 'W1')
            pm.connectAttr(eyesCenterCTL + '.eyelidFollow', lPAC1 + '.' + rightEyesPointer + 'W0')
            pm.connectAttr(eyesCenterCTL + '.eyelidFollow', lPAC1 + '.' + headPointer + 'W1')
        
        createNewGameJoint_Eye(blinkUpper1JNT, headJNT)
        createNewGameJoint_Eye(blinkUpper2JNT, headJNT)
        createNewGameJoint_Eye(blinkUpper3JNT, headJNT)
        createNewGameJoint_Eye(blinkLower1JNT, headJNT)
        createNewGameJoint_Eye(blinkLower2JNT, headJNT)
        createNewGameJoint_Eye(blinkLower3JNT, headJNT)

eyeJointValue = 12

def eyeLeftButton():
    sel = pm.ls(os=True)[0]
    pm.textField('eyeLeftNameField', e=True, text=sel)

def eyeRightButton():
    sel = pm.ls(os=True)[0]
    pm.textField('eyeRightNameField', e=True, text=sel)

def eyeModelButton():
    sel = pm.ls(os=True)[0]
    pm.textField('eyeModelField', e=True, text=sel)

def eyeDirectionButton():
    sel = pm.ls(os=True)[0]
    pm.textField('eyeDirectionField', e=True, text=sel)

def eyeJointField():
    global eyeJointValue
    eyeJointValue = pm.intField('eyeJointField', query=True, value=True)
    pm.intSlider('eyeJointSlider', edit=True, value=eyeJointValue)
    
def eyeJointDrag():
    global eyeJointValue
    eyeJointValue = pm.intSlider('eyeJointSlider', query=True, value=True)
    pm.intField('eyeJointField', edit=True, value=eyeJointValue)
    
def eyeJointSlider():
    global eyeJointValue
    eyeJointValue = pm.intSlider('eyeJointSlider', query=True, value=True)

def grouping(list, nameGRP):
    selected = [list]
    for sel in selected:
        i = str(sel)
        iSplit = i.split('_')
        iTotalNumber = len(i)
        iSplitLast = len(iSplit[-1])
        iNumber = iTotalNumber - iSplitLast-1
        iName = i[:iNumber]
        
        checkParent = []
        try:
            checkParent = pm.listRelatives(sel, parent=True)
        except:
            pass
        
        if iSplit <= 1:
            createGroup = pm.group(empty=True, n=sel+nameGRP)
        else:
            createGroup = pm.group(empty=True, n=iName+nameGRP)
        
        pm.delete(pm.parentConstraint(i, createGroup))
        pm.delete(pm.scaleConstraint(i, createGroup))
        pm.parent(i, createGroup)
        
        if checkParent != []:
            pm.parent(createGroup, checkParent[0])
        
        pm.select(selected)

def hideAttribute(selected):
    selList = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.visibility']
    for b in selList:
        pm.setAttr('{}{}'.format(selected, b), l=True, k=False)

def createNewGameJoint(targetOBJ, parentTo):
    findName(targetOBJ)
    jnt = pm.joint(n=targetOBJ[:-4])
    dummy = pm.joint(n='driver_' + targetOBJ[:-4])
    pm.delete(pm.parentConstraint(targetOBJ, jnt, mo=False))
    pm.delete(pm.parentConstraint(targetOBJ, dummy, mo=False))
    pm.parent(jnt, parentTo)
    pm.parent(dummy, 'driver_' + parentTo)
    pm.setAttr(targetOBJ + '.visibility', 0)
            
    pac = pm.parentConstraint(targetOBJ, dummy, n=findNameResult + '_PAC', mo=True)
    scn = pm.scaleConstraint(targetOBJ, dummy, n=findNameResult + '_SCN', mo=True)
    
    for i in ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.scaleX', '.scaleY', '.scaleZ', '.jointOrientX', '.jointOrientY', '.jointOrientZ']:
        try:
            pm.connectAttr(dummy + i, jnt + i)
        except:
            pass

def createEyesColor():
    surfixName = pm.textField('headNameFirstField', query=True, text=True)
    prefixName = pm.textField('headNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    headController = 'fk_' + surfixName + 'head' + prefixName + '_anim'
    leftEyes = pm.textField('eyeLeftNameField', query=True, text=True)
    rightEyes = pm.textField('eyeRightNameField', query=True, text=True)
    eyeModel = pm.textField('eyeModelField', query=True, text=True)
    eyeDirection = pm.textField('eyeDirectionField', query=True, text=True)
    eyesJointValue = eyeJointValue
    sides = ['l', 'r']
    #leftEyesAIMCTL = 'L_IK_eyeAim_ctl'
    #rightEyesAIMCTL = 'R_IK_eyeAim_ctl'
    leftEyesAIMCTL = 'eyectrl_L'
    rightEyesAIMCTL = 'eyectrl_R'
    leftEyesJNT = leftEyes.replace('_anim', '')
    rightEyesJNT = rightEyes.replace('_anim', '')
    
    ### Eye Scaling
    
    leftEyesCenterP = leftEyes + '_centerPointer_LOC'
    leftEyesFrontP = leftEyes + '_frontPointer_LOC'
    rightEyesCenterP = rightEyes + '_centerPointer_LOC'
    rightEyesFrontP = rightEyes + '_frontPointer_LOC'
    eyeJNTGroup = 'eyeScalingColor_grp'
    leftJNTGroup = 'eyePupilSize_l_grp'
    rightJNTGroup = 'eyePupilSize_r_grp'
    pupilMaxGroup = 'pupilSizeMaxValue_grp'
    pupilMinGroup = 'pupilSizeMinValue_grp'
    irisMaxGroup = 'irisSizeMaxValue_grp'
    irisMinGroup = 'irisSizeMinValue_grp'
    
    pm.group(empty=True, n=eyeJNTGroup)
    pm.group(empty=True, n=leftJNTGroup, p=eyeJNTGroup)
    pm.group(empty=True, n=rightJNTGroup, p=eyeJNTGroup)
    pm.group(empty=True, n=pupilMaxGroup, p=eyeJNTGroup)
    pm.group(empty=True, n=pupilMinGroup, p=eyeJNTGroup)
    pm.group(empty=True, n=irisMaxGroup, p=eyeJNTGroup)
    pm.group(empty=True, n=irisMinGroup, p=eyeJNTGroup)
    
    pm.delete(pm.parentConstraint(leftEyes, leftJNTGroup, mo=False))
    pm.delete(pm.parentConstraint(leftEyes, rightJNTGroup, mo=False))
    pm.delete(pm.parentConstraint(leftEyes, rightEyes, pupilMaxGroup, mo=False))
    pm.delete(pm.parentConstraint(leftEyes, rightEyes, pupilMinGroup, mo=False))
    pm.delete(pm.parentConstraint(leftEyes, rightEyes, irisMaxGroup, mo=False))
    pm.delete(pm.parentConstraint(leftEyes, rightEyes, irisMinGroup, mo=False))
    
    hideAttribute(pupilMaxGroup)
    hideAttribute(pupilMinGroup)
    hideAttribute(irisMaxGroup)
    hideAttribute(irisMinGroup)
    
    miscGRP = 'misc_grp'
    
    if not pm.objExists(miscGRP):
        pm.group(empty=True, n=miscGRP, p='rig_grp')
    
    pm.parent(eyeJNTGroup, miscGRP)
    
    pm.spaceLocator(n=leftEyesCenterP)
    pm.spaceLocator(n=rightEyesCenterP)
    pm.delete(pm.parentConstraint(leftEyes, leftEyesCenterP, mo=False))
    pm.delete(pm.parentConstraint(leftEyes, rightEyesCenterP, mo=False))
    
    pm.addAttr(leftEyesAIMCTL, ln='pupilScale', at='double', k=True, min=-1, max=1, dv=0)
    pm.addAttr(leftEyesAIMCTL, ln='irisScale', at='double', k=True, min=-1, max=1, dv=0)
    pm.addAttr(rightEyesAIMCTL, ln='pupilScale', at='double', k=True, min=-1, max=1, dv=0)
    pm.addAttr(rightEyesAIMCTL, ln='irisScale', at='double', k=True, min=-1, max=1, dv=0)
    
    pm.addAttr(leftEyesAIMCTL, ln='pupilMax', at='double', k=False, min=0, max=1, dv=1)
    pm.addAttr(leftEyesAIMCTL, ln='pupilMin', at='double', k=False, min=0, max=1, dv=1)
    pm.addAttr(leftEyesAIMCTL, ln='irisMax', at='double', k=False, min=0, max=1, dv=1)
    pm.addAttr(leftEyesAIMCTL, ln='irisMin', at='double', k=False, min=0, max=1, dv=1)
    pm.addAttr(rightEyesAIMCTL, ln='pupilMax', at='double', k=False, min=0, max=1, dv=1)
    pm.addAttr(rightEyesAIMCTL, ln='pupilMin', at='double', k=False, min=0, max=1, dv=1)
    pm.addAttr(rightEyesAIMCTL, ln='irisMax', at='double', k=False, min=0, max=1, dv=1)
    pm.addAttr(rightEyesAIMCTL, ln='irisMin', at='double', k=False, min=0, max=1, dv=1)
    
    pm.setDrivenKeyframe(leftEyesAIMCTL + '.pupilMax', cd=leftEyesAIMCTL + '.pupilScale', itt='linear', ott='linear', dv=0, v=0)
    pm.setDrivenKeyframe(leftEyesAIMCTL + '.pupilMax', cd=leftEyesAIMCTL + '.pupilScale', itt='linear', ott='linear', dv=1, v=1)
    pm.setDrivenKeyframe(leftEyesAIMCTL + '.pupilMin', cd=leftEyesAIMCTL + '.pupilScale', itt='linear', ott='linear', dv=0, v=0)
    pm.setDrivenKeyframe(leftEyesAIMCTL + '.pupilMin', cd=leftEyesAIMCTL + '.pupilScale', itt='linear', ott='linear', dv=-1, v=1)
    pm.setDrivenKeyframe(leftEyesAIMCTL + '.irisMax', cd=leftEyesAIMCTL + '.irisScale', itt='linear', ott='linear', dv=0, v=0)
    pm.setDrivenKeyframe(leftEyesAIMCTL + '.irisMax', cd=leftEyesAIMCTL + '.irisScale', itt='linear', ott='linear', dv=1, v=1)
    pm.setDrivenKeyframe(leftEyesAIMCTL + '.irisMin', cd=leftEyesAIMCTL + '.irisScale', itt='linear', ott='linear', dv=0, v=0)
    pm.setDrivenKeyframe(leftEyesAIMCTL + '.irisMin', cd=leftEyesAIMCTL + '.irisScale', itt='linear', ott='linear', dv=-1, v=1)
    
    pm.setDrivenKeyframe(rightEyesAIMCTL + '.pupilMax', cd=rightEyesAIMCTL + '.pupilScale', itt='linear', ott='linear', dv=0, v=0)
    pm.setDrivenKeyframe(rightEyesAIMCTL + '.pupilMax', cd=rightEyesAIMCTL + '.pupilScale', itt='linear', ott='linear', dv=1, v=1)
    pm.setDrivenKeyframe(rightEyesAIMCTL + '.pupilMin', cd=rightEyesAIMCTL + '.pupilScale', itt='linear', ott='linear', dv=0, v=0)
    pm.setDrivenKeyframe(rightEyesAIMCTL + '.pupilMin', cd=rightEyesAIMCTL + '.pupilScale', itt='linear', ott='linear', dv=-1, v=1)
    pm.setDrivenKeyframe(rightEyesAIMCTL + '.irisMax', cd=rightEyesAIMCTL + '.irisScale', itt='linear', ott='linear', dv=0, v=0)
    pm.setDrivenKeyframe(rightEyesAIMCTL + '.irisMax', cd=rightEyesAIMCTL + '.irisScale', itt='linear', ott='linear', dv=1, v=1)
    pm.setDrivenKeyframe(rightEyesAIMCTL + '.irisMin', cd=rightEyesAIMCTL + '.irisScale', itt='linear', ott='linear', dv=0, v=0)
    pm.setDrivenKeyframe(rightEyesAIMCTL + '.irisMin', cd=rightEyesAIMCTL + '.irisScale', itt='linear', ott='linear', dv=-1, v=1)
    
    for side in sides:
        bbox = pm.exactWorldBoundingBox(eyeModel)
        cube = pm.polyCube(n=eyeModel+"_cube", w=(-bbox[0]+bbox[3]), h=(-bbox[1]+bbox[4]), d=(-bbox[2]+bbox[5]))
        
        pm.setAttr(cube[1] + '.subdivisionsDepth', eyesJointValue*2)
        pm.setAttr(cube[0] + '.scaleX', 0.2)
        pm.setAttr(cube[0] + '.scaleY', 0.2)
        pm.makeIdentity(cube[0], a=True, s=True)
        pm.delete(pm.parentConstraint(leftEyesCenterP, cube[0], mo=False))
        
        if side == 'l':
            loc = pm.spaceLocator(n=leftEyesFrontP)
        elif side == 'r':
            loc = pm.spaceLocator(n=rightEyesFrontP)
        
        if side == 'l':
            aimCTL = leftEyesAIMCTL
            eyesCenterP = loc
            jntGRP = leftJNTGroup
            eyeJNT = leftEyesJNT
        elif side == 'r':
            aimCTL = rightEyesAIMCTL
            eyesCenterP = loc
            jntGRP = rightJNTGroup
            eyeJNT = rightEyesJNT
        
        pm.delete(pm.aimConstraint(eyeDirection, cube[0], aim=[0, 0, 1], mo=False))
        pm.delete(pm.aimConstraint(eyeDirection, jntGRP, aim=[0, 0, 1], mo=False))
        
        sel = pm.ls(cube[0] + '.f[0]')
        cls = pm.cluster(sel, n=cube[0] + "_cls")[1]
        
        pm.delete(pm.parentConstraint(cls, loc, mo=False))
        #pm.delete(cls)
        
        centerV = pm.getAttr(leftEyesCenterP + '.translateZ')
        frontV = pm.getAttr(loc + '.translateZ')
        moveValue = (centerV - frontV) / eyesJointValue
        value = 0
        
        for o in range(eyesJointValue):
            pm.select(d=True)
            jnt = pm.joint(n='eyePupilSize_' + str(o) + '_' + side + '_jnt')
            pm.delete(pm.parentConstraint(eyesCenterP, jnt, mo=False))
            pm.setAttr(jnt + '.translateZ', pm.getAttr(jnt + '.translateZ') + value)
            pm.parent(jnt, jntGRP)
            grouping(jnt, '_trn')
            
            createNewGameJoint(jnt, eyeJNT)
            
            value += moveValue
            
            # pupilMax
            
            tName = 'joint_' + str(o) + '_translatePupilMax'
            sName = 'joint_' + str(o) + '_scalePupilMax'
            
            if side == 'l':
                pm.addAttr(pupilMaxGroup, ln=tName, at='double', k=True)
                pm.addAttr(pupilMaxGroup, ln=sName, at='double', k=True, dv=1)
            
            md = pm.createNode('multiplyDivide', n=jnt + '_md')
            mdScale = pm.createNode('multiplyDivide', n=jnt + '_mdScale')
            pmaScale = pm.createNode('plusMinusAverage', n=jnt + '_pmaScale')
            
            pm.connectAttr(aimCTL + '.pupilMax', md + '.input1.input1X.')
            pm.connectAttr(pupilMaxGroup + '.' + tName, md + '.input2.input2X.')
            
            pm.setAttr(md + '.input1Y.', 1)
            pm.connectAttr(aimCTL + '.pupilMax', mdScale + '.input1.input1X.')
            pm.connectAttr(pupilMaxGroup + '.' + sName, mdScale + '.input2.input2X.')
            pm.setAttr(pmaScale + '.input1D[0]', 1)
            pm.connectAttr(mdScale + '.output.outputX', pmaScale + '.input1D[1]')
            pm.connectAttr(pmaScale + '.output1D', md + '.input2.input2Y.')
            
            pmaTFinal = pm.createNode('plusMinusAverage', n=jnt + '_pmaTFinal')
            pmaSFinal = pm.createNode('plusMinusAverage', n=jnt + '_pmaSFinal')
            
            pm.connectAttr(md + '.output.outputX', pmaTFinal + '.input1D[0].')
            pm.connectAttr(md + '.output.outputY', pmaSFinal + '.input1D[0].')
            
            pm.connectAttr(pmaTFinal + '.output1D', jnt + '.translate.translateZ.')
            pm.connectAttr(pmaSFinal + '.output1D', jnt + '.scale.scaleX.')
            pm.connectAttr(pmaSFinal + '.output1D', jnt + '.scale.scaleY.')
            pm.connectAttr(pmaSFinal + '.output1D', jnt + '.scale.scaleZ.')
            
            pm.setAttr(pupilMaxGroup + '.' + tName, float(1/eyesJointValue))
            pm.setAttr(pupilMaxGroup + '.' + sName, float(1/eyesJointValue))
            
            # pupilMin
            
            tName = 'joint_' + str(o) + '_translatePupilMin'
            sName = 'joint_' + str(o) + '_scalePupilMin'
            
            if side == 'l':
                pm.addAttr(pupilMinGroup, ln=tName, at='double', k=True)
                pm.addAttr(pupilMinGroup, ln=sName, at='double', k=True, dv=1)
            
            md = pm.createNode('multiplyDivide', n=jnt + '_md')
            mdScale = pm.createNode('multiplyDivide', n=jnt + '_mdScale')
            pmaScale = pm.createNode('plusMinusAverage', n=jnt + '_pmaScale')
            
            pm.connectAttr(aimCTL + '.pupilMin', md + '.input1.input1X.')
            pm.connectAttr(pupilMinGroup + '.' + tName, md + '.input2.input2X.')
            
            pm.setAttr(md + '.input1Y.', 1)
            pm.connectAttr(aimCTL + '.pupilMin', mdScale + '.input1.input1X.')
            pm.connectAttr(pupilMinGroup + '.' + sName, mdScale + '.input2.input2X.')
            pm.setAttr(pmaScale + '.input1D[0]', 1)
            pm.connectAttr(mdScale + '.output.outputX', pmaScale + '.input1D[1]')
            pm.connectAttr(pmaScale + '.output1D', md + '.input2.input2Y.')
            
            pm.connectAttr(md + '.output.outputX', pmaTFinal + '.input1D[1].')
            pm.connectAttr(md + '.output.outputY', pmaSFinal + '.input1D[1].')
            
            pm.setAttr(pupilMinGroup + '.' + tName, float(1/eyesJointValue))
            pm.setAttr(pupilMinGroup + '.' + sName, float(1/eyesJointValue))
            
            # irisMax
            
            tName = 'joint_' + str(o) + '_translatIriseMax'
            sName = 'joint_' + str(o) + '_scaleIrisMax'
            
            if side == 'l':
                pm.addAttr(irisMaxGroup, ln=tName, at='double', k=True)
                pm.addAttr(irisMaxGroup, ln=sName, at='double', k=True, dv=1)
            
            md = pm.createNode('multiplyDivide', n=jnt + '_md')
            mdScale = pm.createNode('multiplyDivide', n=jnt + '_mdScale')
            pmaScale = pm.createNode('plusMinusAverage', n=jnt + '_pmaScale')
            
            pm.connectAttr(aimCTL + '.irisMax', md + '.input1.input1X.')
            pm.connectAttr(irisMaxGroup + '.' + tName, md + '.input2.input2X.')
            
            pm.setAttr(md + '.input1Y.', 1)
            pm.connectAttr(aimCTL + '.irisMax', mdScale + '.input1.input1X.')
            pm.connectAttr(irisMaxGroup + '.' + sName, mdScale + '.input2.input2X.')
            pm.setAttr(pmaScale + '.input1D[0]', 1)
            pm.connectAttr(mdScale + '.output.outputX', pmaScale + '.input1D[1]')
            pm.connectAttr(pmaScale + '.output1D', md + '.input2.input2Y.')
            
            pm.connectAttr(md + '.output.outputX', pmaTFinal + '.input1D[2].')
            pm.connectAttr(md + '.output.outputY', pmaSFinal + '.input1D[2].')
            
            pm.setAttr(irisMaxGroup + '.' + tName, float(1/eyesJointValue))
            pm.setAttr(irisMaxGroup + '.' + sName, float(1/eyesJointValue))
            
            # irisMin
            
            tName = 'joint_' + str(o) + '_translateIrisMin'
            sName = 'joint_' + str(o) + '_scaleIrisMin'
            
            if side == 'l':
                pm.addAttr(irisMinGroup, ln=tName, at='double', k=True)
                pm.addAttr(irisMinGroup, ln=sName, at='double', k=True, dv=1)
            
            md = pm.createNode('multiplyDivide', n=jnt + '_md')
            mdScale = pm.createNode('multiplyDivide', n=jnt + '_mdScale')
            pmaScale = pm.createNode('plusMinusAverage', n=jnt + '_pmaScale')
            
            pm.connectAttr(aimCTL + '.irisMin', md + '.input1.input1X.')
            pm.connectAttr(irisMinGroup + '.' + tName, md + '.input2.input2X.')
            
            pm.setAttr(md + '.input1Y.', 1)
            pm.connectAttr(aimCTL + '.irisMin', mdScale + '.input1.input1X.')
            pm.connectAttr(irisMinGroup + '.' + sName, mdScale + '.input2.input2X.')
            pm.setAttr(pmaScale + '.input1D[0]', 1)
            pm.connectAttr(mdScale + '.output.outputX', pmaScale + '.input1D[1]')
            pm.connectAttr(pmaScale + '.output1D', md + '.input2.input2Y.')
            
            pm.connectAttr(md + '.output.outputX', pmaTFinal + '.input1D[3].')
            pm.connectAttr(md + '.output.outputY', pmaSFinal + '.input1D[3].')
            
            pm.setAttr(irisMinGroup + '.' + tName, float(1/eyesJointValue))
            pm.setAttr(irisMinGroup + '.' + sName, float(1/eyesJointValue))
            
            #
        
        #pm.delete(cube)
        '''
        pm.setAttr(leftJNTGroup + '.rotateX', 0)
        pm.setAttr(leftJNTGroup + '.rotateY', 0)
        pm.setAttr(leftJNTGroup + '.rotateZ', 0)
        pm.setAttr(rightJNTGroup + '.rotateX', 0)
        pm.setAttr(rightJNTGroup + '.rotateY', 0)
        pm.setAttr(rightJNTGroup + '.rotateZ', 0)
        '''
    
    leftJNTOffset = 'eyePupilSize_l_offset_grp'
    rightJNTOffset = 'eyePupilSize_r_offset_grp'
    
    pm.group(empty=True, n=leftJNTOffset)
    pm.group(empty=True, n=rightJNTOffset)
    pm.parent(leftJNTOffset, eyeJNTGroup)
    pm.parent(rightJNTOffset, eyeJNTGroup)
    pm.parent(leftJNTGroup, leftJNTOffset)
    pm.parent(rightJNTGroup, rightJNTOffset)
    
    dup = pm.duplicate(eyeDirection, n=eyeDirection + '_dup')[0]
    pm.setAttr(dup + '.translateX', pm.getAttr(dup + '.translateX') * -1)
    pm.setAttr(rightEyesCenterP + '.translateX', pm.getAttr(rightEyesCenterP + '.translateX') * -1)
    
    pm.delete(pm.parentConstraint(rightEyesCenterP, rightJNTGroup, mo=False))
    pm.delete(pm.aimConstraint(dup, rightJNTGroup, aim=[0, 0, 1], mo=False))
    #pm.setAttr(rightJNTOffset + '.scaleX', -1)
    
    #pm.delete(leftEyesCenterP)
    #pm.delete(leftEyesFrontP)
    #pm.delete(rightEyesCenterP)
    #pm.delete(rightEyesFrontP)
    
    ### Eye Shading
    
    eyeMaterial = []
    
    if eyeMaterial == []:
        eyeMaterial = pm.listConnections(cmds.listHistory(eyeModel, f=True), type='lambert')[0]
    elif eyeMaterial == []:
        eyeMaterial = pm.listConnections(cmds.listHistory(eyeModel, f=True), type='blinn')[0]
    elif eyeMaterial == []:
        eyeMaterial = pm.listConnections(cmds.listHistory(eyeModel, f=True), type='phong')[0]
    
    eyeColorFile = pm.listConnections(eyeMaterial, type='file')[0]
    eyeRemapRGB01 = 'eyeball_remapColor01'
    eyeRemapHSV01 = 'eyeball_remapHSV01'
    eyeCompColor01 = 'eyeball_compColor01'
    eyeCompAlpha01 = 'eyeball_compAlpha01'
    
    pm.shadingNode('remapColor', asUtility = True, n=eyeRemapRGB01)
    pm.shadingNode('remapHsv', asUtility = True, n=eyeRemapHSV01)
    pm.shadingNode('colorComposite', asUtility = True, n=eyeCompColor01)
    pm.shadingNode('ramp', asUtility = True, n=eyeCompAlpha01)
    
    pm.connectAttr(eyeColorFile + '.outColor', eyeRemapHSV01 + '.color', f=True)
    pm.connectAttr(eyeRemapHSV01 + '.outColor', eyeCompColor01 + '.colorA', f=True)
    pm.connectAttr(eyeRemapRGB01 + '.outColor', eyeCompColor01 + '.colorB', f=True)
    pm.connectAttr(eyeCompAlpha01 + '.outAlpha', eyeCompColor01 + '.factor', f=True)
    pm.connectAttr(eyeCompColor01 + '.outColor', eyeMaterial + '.color', f=True)
    
    pm.setAttr(eyeCompColor01 + '.operation', 3)
    pm.setAttr(eyeRemapRGB01 + '.color', [1, 1, 1])
    pm.setAttr(eyeRemapHSV01 + '.h[0].hp', l=True)
    pm.setAttr(eyeRemapHSV01 + '.s[0].sp', l=True)
    pm.setAttr(eyeRemapHSV01 + '.v[0].vp', l=True)
    pm.setAttr(eyeRemapRGB01 + '.r[0].rp', l=True)
    pm.setAttr(eyeRemapRGB01 + '.r[0].rfv', l=True)
    pm.setAttr(eyeRemapRGB01 + '.g[0].gp', l=True)
    pm.setAttr(eyeRemapRGB01 + '.g[0].gfv', l=True)
    pm.setAttr(eyeRemapRGB01 + '.b[0].bp', l=True)
    pm.setAttr(eyeRemapRGB01 + '.b[0].bfv', l=True)
    pm.setAttr(eyeCompAlpha01 + '.type', 4)
    pm.setAttr(eyeCompAlpha01 + '.interpolation', 0)
    pm.setAttr(eyeCompAlpha01 + '.colorEntryList[1].position', 0)
    pm.setAttr(eyeCompAlpha01 + '.colorEntryList[0].position', 0.225)
    pm.setAttr(eyeCompAlpha01 + '.colorEntryList[1].color', [1, 1, 1])
    pm.setAttr(eyeCompAlpha01 + '.colorEntryList[0].color', [0, 0, 0])
    
    ### Bridge to Unreal
    
    colorHSVJNT = 'color_hsv_jnt'
    colorRGBJNT = 'color_rgb_jnt'
    scalePupilLeftJNT = 'scale_pupil_l_jnt'
    scaleIrisLeftJNT = 'scale_iris_l_jnt'
    scalePupilRightJNT = 'scale_pupil_r_jnt'
    scaleIrisRightJNT = 'scale_iris_r_jnt'
    
    def createJointColor(name, parentTo):
        pm.select(d=True)
        pm.joint(n=name)
        pm.parent(name, parentTo)
    
    createJointColor(colorHSVJNT, 'root')
    createJointColor(colorRGBJNT, 'root')
    createJointColor(scalePupilLeftJNT, 'root')
    createJointColor(scaleIrisLeftJNT, 'root')
    createJointColor(scalePupilRightJNT, 'root')
    createJointColor(scaleIrisRightJNT, 'root')
    
    pm.connectAttr(eyeRemapHSV01 + '.hue[0].hue_FloatValue', colorHSVJNT + '.rotateX', f=True)
    pm.connectAttr(eyeRemapHSV01 + '.saturation[0].saturation_FloatValue', colorHSVJNT + '.rotateY', f=True)
    pm.connectAttr(eyeRemapHSV01 + '.value[0].value_FloatValue', colorHSVJNT + '.rotateZ', f=True)
    
    pm.connectAttr(eyeRemapRGB01 + '.outColorR', colorRGBJNT + '.rotateX', f=True)
    pm.connectAttr(eyeRemapRGB01 + '.outColorG', colorRGBJNT + '.rotateY', f=True)
    pm.connectAttr(eyeRemapRGB01 + '.outColorB', colorRGBJNT + '.rotateZ', f=True)
    
    pm.connectAttr(leftEyesAIMCTL + '.pupilMin', scalePupilLeftJNT + '.rotateX', f=True)
    pm.connectAttr(leftEyesAIMCTL + '.pupilMax', scalePupilLeftJNT + '.rotateY', f=True)
    pm.connectAttr(leftEyesAIMCTL + '.irisMin', scaleIrisLeftJNT + '.rotateX', f=True)
    pm.connectAttr(leftEyesAIMCTL + '.irisMax', scaleIrisLeftJNT + '.rotateY', f=True)
    
    pm.connectAttr(rightEyesAIMCTL + '.pupilMin', scalePupilRightJNT + '.rotateX', f=True)
    pm.connectAttr(rightEyesAIMCTL + '.pupilMax', scalePupilRightJNT + '.rotateY', f=True)
    pm.connectAttr(rightEyesAIMCTL + '.irisMin', scaleIrisRightJNT + '.rotateX', f=True)
    pm.connectAttr(rightEyesAIMCTL + '.irisMax', scaleIrisRightJNT + '.rotateY', f=True)

###

def sourceInputButton():
    sel = pm.ls(os=True)[0]
    pm.textField('sourceInputField', e=True, text=sel)

def fkInputButton():
    sel = pm.ls(os=True)[0]
    pm.textField('fkInputField', e=True, text=sel)

def ikInputButton():
    sel = pm.ls(os=True)[0]
    pm.textField('ikInputField', e=True, text=sel)

def createSwitchParent():
    selected = pm.ls(os=True)[0]
    sourceInput = pm.textField('sourceInputField', query=True, text=True)
    fkInput = pm.textField('fkInputField', query=True, text=True)
    ikInput = pm.textField('ikInputField', query=True, text=True)
    selectedPAC = pm.parentConstraint(fkInput, ikInput, selected, mo=True)
    selectedREV = pm.createNode('reverse', n=selected + '_REV')
    
    pm.connectAttr(sourceInput + '.mode', selectedREV + '.input.inputX.')
    pm.connectAttr(selectedREV + '.output.outputX', selectedPAC + '.' + fkInput + 'W0')
    pm.connectAttr(sourceInput + '.mode', selectedPAC + '.' + ikInput + 'W1')
    
    pm.select(selected)

###

def buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock):
    rotateLock1LOC = objectList[-1] + 'LockRotation1_loc'
    rotateLock1GRP = objectList[-1] + 'LockRotation1_grp'
    rotateLock2LOC = objectList[-1] + 'LockRotation2_loc'
    rotateLock2GRP = objectList[-1] + 'LockRotation2_grp'
    
    if rotationLock == True:
        if not pm.objExists(rotateLock1LOC):
            pm.spaceLocator(n=rotateLock1LOC)
            pm.group(rotateLock1LOC, n=rotateLock1GRP)
            pm.parent(rotateLock1GRP, objectList[0])
            pm.delete(pm.parentConstraint(listController, rotateLock1GRP, mo=False))
            pm.parentConstraint(objectList[-1], rotateLock1GRP, n=rotateLock1GRP + '_pac', mo=True)
            
            pm.spaceLocator(n=rotateLock2LOC)
            pm.group(rotateLock2LOC, n=rotateLock2GRP)
            pm.parent(rotateLock2GRP, objectList[0])
            pm.delete(pm.parentConstraint(listController, rotateLock2GRP, mo=False))
            pm.pointConstraint(rotateLock1LOC, rotateLock2GRP, n=rotateLock2GRP + '_pac', mo=True)
        
        objectList.append(rotateLock2LOC)
        listName.append(listName[-1] + 'RO')
    
    for o in listName:
        if listName[-1] != o:
            listNameNew = listNameNew+str(o)+':'
        else:
            listNameNew = listNameNew+str(o)
            
    print ''
    print attrName
    print objectList
    print listNameNew
    print listController
    
    listGroup = pm.group(listController, n=listController+'_offset_set_grp')
    
    if not pm.attributeQuery(attrName, node=listController, ex=True):
        pm.addAttr(listController, ln=attrName, at='enum', k=1, en=listNameNew)
        PAC = pm.parentConstraint(objectList, listGroup, n=listGroup+'_PAC', mo=True)
        SCN = pm.scaleConstraint(objectList, listGroup, n=listGroup+'_SCN', mo=True)
        
        for o in range(len(objectList)):
            nname = '{}_Cond'.format(objectList[o]+listController)
            pm.createNode('condition', n=nname)
            pm.setAttr('{}.secondTerm'.format(nname), o)
            pm.setAttr('{}.colorIfTrueR'.format(nname), 1)
            pm.setAttr('{}.colorIfFalseR'.format(nname), 0)
            pm.connectAttr('{}.{}'.format(listController, attrName), '{}.firstTerm'.format(nname))
            pm.connectAttr('{}.outColorR'.format(nname), '{}.{}W{}'.format(PAC, objectList[o], o))
            pm.connectAttr('{}.outColorR'.format(nname), '{}.{}W{}'.format(SCN, objectList[o], o))
    else:
        pass
    
    pm.setAttr(listController + '.' + attrName, 1)

def createFollowSystem():
    leftSide = pm.textField('leftField', query=True, text=True)
    rightSide = pm.textField('rightField', query=True, text=True)
    
    # Head
    surfixName = pm.textField('headNameFirstField', query=True, text=True)
    prefixName = pm.textField('headNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    headCTL = 'fk_' + surfixName + 'head' + prefixName + '_anim'
    neck01CTL = 'fk_' + surfixName + 'neck_01' + prefixName + '_anim'
    
    # Spine
    surfixName = pm.textField('spineNameFirstField', query=True, text=True)
    prefixName = pm.textField('spineNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    spineMode = 'torso_settings'
    
    torsoHipCTL = surfixName + 'torso' + prefixName + 'hip_anim'
    spine01CTL = 'fk_' + surfixName + 'spine_01' + prefixName + '_anim'
    spine02CTL = 'fk_' + surfixName + 'spine_02' + prefixName + '_anim'
    spine03CTL = 'fk_' + surfixName + 'spine_03' + prefixName + '_anim'
    spine03IK = surfixName + 'spine_03' + prefixName + '_ik_follow'
    
    spine03LocGRP = spine03CTL + '_loc_grp'
    spine03LocPAC = spine03CTL + '_loc_grp_pac'
    spine03Loc1GRP = spine03CTL + '_locLockRotation1_grp'
    spine03Loc1PAC = spine03CTL + '_locLockRotation1_grp_pac'
    
    # Arm
    surfixName = pm.textField('armNameFirstField', query=True, text=True)
    prefixName = pm.textField('armNameLastField', query=True, text=True)
    
    if not surfixName == '':
        surfixName = surfixName + '_'
    
    if not prefixName == '':
        prefixName = '_' + prefixName
    
    ###
    
    if leftSide in prefixName:
        leftClavicleFKCTL = 'fk_' + surfixName + 'clavicle' + prefixName + '_anim'
        leftClavicleIKCTL = 'ik_' + surfixName + 'clavicle' + prefixName + '_anim'
        prefixName = '_' + rightSide
        rightClavicleFKCTL = 'fk_' + surfixName + 'clavicle' + prefixName + '_anim'
        rightClavicleIKCTL = 'ik_' + surfixName + 'clavicle' + prefixName + '_anim'
    
    if rightSide in prefixName:
        leftClavicleFKCTL = 'fk_' + surfixName + 'clavicle' + prefixName + '_anim'
        leftClavicleIKCTL = 'ik_' + surfixName + 'clavicle' + prefixName + '_anim'
        prefixName = '_' + leftSide
        rightClavicleFKCTL = 'fk_' + surfixName + 'clavicle' + prefixName + '_anim'
        rightClavicleIKCTL = 'ik_' + surfixName + 'clavicle' + prefixName + '_anim'
    
    #
    
    masterLOC = createControllerDummy_Eye('master_anim')
    neck01LOC = createControllerDummy_Eye(neck01CTL)
    leftClavicleFKLOC = createControllerDummy_Eye(leftClavicleFKCTL)
    leftClavicleIKLOC = createControllerDummy_Eye(leftClavicleIKCTL)
    rightClavicleFKLOC = createControllerDummy_Eye(rightClavicleFKCTL)
    rightClavicleIKLOC = createControllerDummy_Eye(rightClavicleIKCTL)
    spine03LOC = createControllerDummy_Eye(spine03CTL)
    spine02LOC = createControllerDummy_Eye(spine02CTL)
    spine01LOC = createControllerDummy_Eye(spine01CTL)
    
    # Head
    rotationLock = True
    attrName = 'follow'
    objectList = [masterLOC, neck01LOC]
    listName = ['master', 'neck']
    listController = headCTL
    listNameNew = ''
    buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock)
    
    # Neck 01
    rotationLock = True
    attrName = 'follow'
    objectList = [masterLOC, spine03LOC]
    listName = ['master', 'spine']
    listController = neck01CTL
    listNameNew = ''
    buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock)
    
    # Left Clavicle FK
    rotationLock = True
    attrName = 'follow'
    objectList = [masterLOC, spine03LOC]
    listName = ['master', 'spine']
    listController = leftClavicleFKCTL
    listNameNew = ''
    buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock)
    
    # Right Clavicle FK
    rotationLock = True
    attrName = 'follow'
    objectList = [masterLOC, spine03LOC]
    listName = ['master', 'spine']
    listController = rightClavicleFKCTL
    listNameNew = ''
    buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock)
    
    # Left Clavicle IK
    rotationLock = True
    attrName = 'follow'
    objectList = [masterLOC, spine03LOC]
    listName = ['master', 'spine']
    listController = leftClavicleIKCTL
    listNameNew = ''
    buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock)
    
    # Right Clavicle IK
    rotationLock = True
    attrName = 'follow'
    objectList = [masterLOC, spine03LOC]
    listName = ['master', 'spine']
    listController = rightClavicleIKCTL
    listNameNew = ''
    buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock)
    
    # Spine 03 FK
    rotationLock = True
    attrName = 'follow'
    objectList = [masterLOC, spine02LOC]
    listName = ['master', 'spine']
    listController = spine03CTL
    listNameNew = ''
    buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock)
    
    # Spine 02 FK
    rotationLock = True
    attrName = 'follow'
    objectList = [masterLOC, spine01LOC]
    listName = ['master', 'spine']
    listController = spine02CTL
    listNameNew = ''
    buildAttr(attrName, objectList, listName, listController, listNameNew, rotationLock)
    
    # Fix Something
    
    pm.delete(spine03LocPAC)
    pm.delete(spine03Loc1PAC)
    
    spinePAC = pm.parentConstraint(spine03CTL, spine03IK, spine03LocGRP, n=spine03LocGRP + '_pac', mo=True)
    spineREV = pm.createNode('reverse', n=spine03LocGRP + '_rev')
    
    pm.connectAttr(spineMode + '.mode', spineREV + '.input.inputX.')
    pm.connectAttr(spineREV + '.output.outputX', spinePAC + '.' + spine03CTL + 'W0')
    pm.connectAttr(spineMode + '.mode', spinePAC + '.' + spine03IK + 'W1')
    
    spinePAC = pm.parentConstraint(spine03CTL, spine03IK, spine03Loc1GRP, n=spine03Loc1GRP + '_pac', mo=True)
    spineREV = pm.createNode('reverse', n=spine03Loc1GRP + '_rev')
    
    pm.connectAttr(spineMode + '.mode', spineREV + '.input.inputX.')
    pm.connectAttr(spineREV + '.output.outputX', spinePAC + '.' + spine03CTL + 'W0')
    pm.connectAttr(spineMode + '.mode', spinePAC + '.' + spine03IK + 'W1')

# --- Windows Setting ---

def resizeMainWindow():
    pass

if (pm.window(windowName_ART, exists=True)):
    pm.deleteUI(windowName_ART)

pm.window(windowName_ART, title=windowTitle_ART, iconName=windowName_ART, resizeToFitChildren=1, h=sizeHeight_ART, w=sizeWidth_ART)

windowWidth = pm.window(windowName_ART, query=True, width=True)
windowHeight = pm.window(windowName_ART, query=True, height=True)

pm.columnLayout('mainWindowColumnLayout', adjustableColumn=1, w=windowWidth)
pm.scrollLayout('mainWindowScrollLayout', rc='resizeMainWindow()', minChildWidth=sizeWidth_ART, hst=0, vst=0, h=windowHeight, w=windowWidth)

mWS1m = windowWidth/3-holderSize_ART/2
mWS2m = (windowWidth-mWS1m)/1-(holderSize_ART/1+1)
mWS3m = (windowWidth-mWS1m)/2-(holderSize_ART/2+1)
mWS4m = (windowWidth-mWS1m)/3-(holderSize_ART/3+1)
mWS5m = (windowWidth-mWS1m)/4-(holderSize_ART/4+1.5)
mWS6m = (windowWidth-mWS1m)/5-(holderSize_ART/5+2)

menuWidthSize1 = mWS1m
menuWidthSize2 = mWS1m, mWS2m+1
menuWidthSize3 = mWS1m, mWS3m, mWS3m
menuWidthSize4 = mWS1m, mWS4m, mWS4m, mWS4m
menuWidthSize5 = mWS1m, mWS5m, mWS5m, mWS5m, mWS5m+1.5
menuWidthSize6 = mWS1m, mWS6m, mWS6m, mWS6m, mWS6m, mWS6m+2

cWS1m = (windowWidth/1)-(holderSize_ART/1+2)
cWS2m = (windowWidth/2)-(holderSize_ART/2+2)
cWS3m = (windowWidth/3)-(holderSize_ART/3+2)
cWS4m = (windowWidth/4)-(holderSize_ART/4+2)
cWS5m = (windowWidth/5)-(holderSize_ART/5+2)
cWS6m = (windowWidth/6)-(holderSize_ART/6+2)

colomnWidthSize1 = cWS1m+4
colomnWidthSize2 = cWS2m, cWS2m+4
colomnWidthSize3 = cWS3m, cWS3m, cWS3m+3
colomnWidthSize4 = cWS4m, cWS4m, cWS4m, cWS4m+1
colomnWidthSize5 = cWS5m, cWS5m, cWS5m, cWS5m, cWS5m+4
colomnWidthSize6 = cWS6m, cWS6m, cWS6m, cWS6m, cWS6m, cWS6m

# pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
# pm.rowLayout(numberOfColumns=2, columnWidth2=(menuWidthSize2), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
# pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
# pm.rowLayout(numberOfColumns=4, columnWidth4=(menuWidthSize4), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
# pm.rowLayout(numberOfColumns=5, columnWidth5=(menuWidthSize5), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0), (5, 'both', 0)])
# pm.rowLayout(numberOfColumns=6, columnWidth6=(menuWidthSize6), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0), (5, 'both', 0), (6, 'both', 0)])

# --- Windows Tool(s) ---
'''
pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.text('textTitle', label=titleText_ART, align='center', font='boldLabelFont')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.text('authorTitle', label='by Chris Gultom', align='center', font='tinyBoldLabelFont')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.text('sliceText_ART1', label=sliceText_ART, align='center')
pm.setParent('..')

pm.rowLayout(numberOfColumns=2, columnWidth2=(colomnWidthSize2), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
pm.button('toggleModule', label='Toggle Visibility Module', command='toggleModule()')
pm.button('mirrorModule', label='Mirror L > R Module', command='mirrorModule()')
pm.setParent('..')

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)
'''
pm.rowLayout(numberOfColumns=4, columnWidth4=(colomnWidthSize4), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
pm.button('unlockJoint', label='Unlock Joint', command='unlockJoint()')
pm.button('toggleRoot', label='Toggle Root', command='toggleRoot()')
pm.button('toggleDriven', label='Toggle Driven', command='toggleDriven()')
pm.button('lockJoint', label='Lock Joint', command='lockJoint()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('selectRootJoint', label='Select Root Joint', command='selectRootJoint()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('createControllerDummy', label='Create Controller Dummy', command='createControllerDummy()')
pm.setParent('..')

###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

menuWidthSize5SP = mWS1m*3.25/5, mWS1m*1.75/5, mWS4m, mWS4m, mWS4m

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.text('fixingSpineFKIK', label='Fixing Spine')
pm.setParent('..')

pm.rowLayout(numberOfColumns=4, columnWidth4=(menuWidthSize4), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
pm.text('spineName', label='Spine Name           ')
pm.textField('spineNameFirstField', text='(surfix)')
pm.textField('spineNameCenterField', text='spine', en=False)
pm.textField('spineNameLastField', text='(prefix)')
pm.setParent('..')

pm.rowLayout(numberOfColumns=2, columnWidth2=(colomnWidthSize2), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
pm.button('fixingSpineFKIKFK', label='Fixing FK', command='fixingSpineFKIKFK()')
pm.button('fixingSpineFKIKIK', label='Fixing IK', command='fixingSpineFKIKIK()')
pm.setParent('..')

###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.text('fixingArmFKIK', label='Fixing Arm')
pm.setParent('..')

pm.rowLayout(numberOfColumns=5, columnWidth5=(menuWidthSize5SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0), (5, 'both', 0)])
pm.text('armName', label='Arm Name')
pm.intField('armMoveValue', value=-20)
pm.textField('armNameFirstField', text='(surfix)')
pm.textField('armNameCenterField', text='arm', en=False)
pm.textField('armNameLastField', text='(prefix)')
pm.setParent('..')

pm.rowLayout(numberOfColumns=2, columnWidth2=(colomnWidthSize2), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
pm.button('fixingArmFKIKFK', label='Fixing FK', command='fixingArmFKIKFK()')
pm.button('fixingArmFKIKIK', label='Fixing IK', command='fixingArmFKIKIK()')
pm.setParent('..')

###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.text('fixingLegFKIK', label='Fixing Leg')
pm.setParent('..')

pm.rowLayout(numberOfColumns=5, columnWidth5=(menuWidthSize5SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0), (5, 'both', 0)])
pm.text('legName', label='Leg Name')
pm.intField('legMoveValue', value=-20)
pm.textField('legNameFirstField', text='(surfix)')
pm.textField('legNameCenterField', text='leg', en=False)
pm.textField('legNameLastField', text='(prefix)')
pm.setParent('..')

pm.rowLayout(numberOfColumns=2, columnWidth2=(colomnWidthSize2), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
pm.button('fixingLegFKIKFK', label='Fixing FK', command='fixingLegFKIKFK()')
pm.button('fixingLegFKIKIK', label='Fixing IK', command='fixingLegFKIKIK()')
pm.setParent('..')

###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.text('fixingChainFKIK', label='Fixing Chain')
pm.setParent('..')

pm.rowLayout(numberOfColumns=5, columnWidth5=(menuWidthSize5SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0), (5, 'both', 0)])
pm.text('chainName', label='Chain Name')
pm.intField('chainMoveValue', value=10000)
pm.textField('chainNameFirstField', text='(surfix)')
pm.textField('chainNameCenterField', text='jnt', en=False)
pm.textField('chainNameLastField', text='(prefix)')
pm.setParent('..')

pm.rowLayout(numberOfColumns=2, columnWidth2=(colomnWidthSize2), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
pm.button('fixingChainFKIKFK', label='Fixing FK', command='fixingChainFKIKFK()')
pm.button('fixingChainFKIKIK', label='Fixing IK', command='fixingChainFKIKIK()')
pm.setParent('..')

###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

menuWidthSize3SP = mWS1m, mWS3m+100, mWS3m-101

pm.rowLayout(numberOfColumns=4, columnWidth4=(menuWidthSize4), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
pm.text('headName', label='Head Name')
pm.textField('headNameFirstField', text='(surfix)')
pm.textField('headNameCenterField', text='head', en=False)
pm.textField('headNameLastField', text='(prefix)')
pm.setParent('..')

pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
pm.text('eyeLeftName', label='Eye Left Name')
pm.textField('eyeLeftNameField', text='eyes_l_jnt_anim')
pm.button('eyeLeftButton', label='@', command='eyeLeftButton()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
pm.text('eyeRightName', label='Eye Right Name')
pm.textField('eyeRightNameField', text='eyes_r_jnt_anim')
pm.button('eyeRightButton', label='@', command='eyeRightButton()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('importEyeSystem', label='Import Eye System', command='importEyeSystem()')
pm.setParent('..')
'''
pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('createEyeSystem01', label='Create Eye System - 01', command='createEyeSystem01()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('createEyeSystem02', label='Create Eye System - 02', command='createEyeSystem02()')
pm.setParent('..')

menuWidthSize3SPP = mWS1m, mWS3m-90, mWS3m+90

pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
pm.text(label='Eye Model Name')
pm.textField('eyeModelField', text='CHA_EXBs_002_body_eye_L_eyeball_ply')
pm.button('eyeModelButton', label='@', command='eyeModelButton()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
pm.text(label='Eye Direction Name')
pm.textField('eyeDirectionField', text='CHA_EXBs_002_body_eye_L_eyeball_plyShape_CLSHandle_LOC0')
pm.button('eyeDirectionButton', label='@', command='eyeDirectionButton()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3SPP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
pm.text(label='Eyes Joint', align='center')
pm.intField('eyeJointField', value=eyeJointValue, cc='eyeJointField()')
pm.intSlider('eyeJointSlider', min=1, max=20, value=eyeJointValue, step=1, dc='eyeJointDrag()', cc='eyeJointSlider()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('createEyesColor', label='Create Eyes Color', command='createEyesColor()')
pm.setParent('..')
'''
###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.text('sliceText_ART3', label=sliceText_ART, align='center')
pm.setParent('..')

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
pm.text('sourceInputName', label='Source Input Name')
pm.textField('sourceInputField', text='arm_l_settings')
pm.button('sourceInputButton', label='@', command='sourceInputButton()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
pm.text('fkInputName', label='FK Input Name')
pm.textField('fkInputField', text='fk_upperarm_l_anim')
pm.button('fkInputButton', label='@', command='fkInputButton()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=3, columnWidth3=(menuWidthSize3SP), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
pm.text('ikInputName', label='IK Input Name')
pm.textField('ikInputField', text='ik_upperarm_l_jnt')
pm.button('ikInputButton', label='@', command='ikInputButton()')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('createSwitchParent', label='Create Switch Parent', command='createSwitchParent()')
pm.setParent('..')

###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

pm.rowLayout(numberOfColumns=2, columnWidth2=(menuWidthSize2), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
pm.text('leftText', label='Left Name')
pm.textField('leftField', text='l')
pm.setParent('..')

pm.rowLayout(numberOfColumns=2, columnWidth2=(menuWidthSize2), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
pm.text('rightText', label='Right Name')
pm.textField('rightField', text='r')
pm.setParent('..')

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('createFollowSystem', label='Create Follow System', command='createFollowSystem()')
pm.setParent('..')

###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('fixFile', label='Fix File', command='fixFile()')
pm.setParent('..')
'''
###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('fixWorldAxis', label='Fix World Axis', command='fixWorldAxis()')
pm.setParent('..')
'''
###

pm.separator(w=sizeWidth_ART-holderSize_ART, h=10)

###

pm.rowLayout(numberOfColumns=1, columnWidth1=(colomnWidthSize1), columnAttach=[(1, 'both', 0)])
pm.button('specialQuadrupedSystem', label='Special Quadruped System', command='specialQuadrupedSystem()')
pm.setParent('..')

# --- Run Script ---

pm.showWindow()
