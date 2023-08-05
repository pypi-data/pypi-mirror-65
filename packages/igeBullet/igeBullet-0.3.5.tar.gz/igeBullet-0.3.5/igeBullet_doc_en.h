/////////////////////////////////////
/////////////////////////////////////
PyDoc_STRVAR(vehicle_doc,
	"Simulates wheeled vehicles.\n"\
	"\n"\
	"Constructors\n"\
	"-----------\n"\
	"	igeBullet.vehicle(world, body)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"	world : igeBullet.world\n"\
	"		dynamics world object.\n"\
	"	body : igeBullet.rigidBody\n"\
	"		rigidBody of vehicle body.\n");

PyDoc_STRVAR(addWheel_doc,
	"Adds a wheel to the vehicle.\n"\
	"	\n"\
	"vehicle.addWheel(connectionPointCS, wheelDirectionCS0, wheelAxleCS, suspensionRestLength, wheelRadius, isFrontWheel)\n"\
	"Parameters\n"\
	"----------\n"\
	"	connectionPointCS : (x,y,z)\n"\
	"	wheelDirectionCS0 : (x,y,z)\n"\
	"	wheelAxleCS : (x,y,z)\n"\
	"	suspensionRestLength : float\n"\
	"	wheelRadius : float\n"\
	"	isFrontWheel : bool\n");

PyDoc_STRVAR(setSteeringValue_doc, 
	"Steering value of vehicle.\n"
	"	\n"\
	"vehicle.setSteeringValue(value, index)\n"\
	"Parameters\n"\
	"----------\n"\
	"	value : float\n"\
	"		Steering value"
	"	index : int\n"\
	"		Index of weel");

PyDoc_STRVAR(applyEngineForce_doc, 
	"Apply engine force.\n"
	"	\n"\
	"vehicle.applyEngineForce(force, index)\n"\
	"Parameters\n"\
	"----------\n"\
	"	force : float\n"\
	"		Engine force"
	"	index : int\n"\
	"		Index of weel");

PyDoc_STRVAR(setBrake_doc, 
	"Set break.\n"
	"	\n"\
	"vehicle.setBrake(break, index)\n"\
	"Parameters\n"\
	"----------\n"\
	"	break : float\n"\
	"		break force"
	"	index : int\n"\
	"		Index of weel");

PyDoc_STRVAR(getWheelPosition_doc, 
	"Get wheel position\n"\
	"	\n"\
	"vehicle.getWheelPosition(index)\n"\
	"	index : int\n"\
	"		Index of weel");

PyDoc_STRVAR(getWheelRotation_doc,
	"Get wheel rotation\n"\
	"	\n"\
	"vehicle.getWheelRotation(index)\n"\
	"	index : int\n"\
	"		Index of weel");

/////////////////////////////////////
/////////////////////////////////////
PyDoc_STRVAR(constraint_doc, 
	"3d physics constraint object\n"\
	"Constructors\n"\
	"-----------\n"\
	"	igeBullet.constraint(type, bodyA,bodyB,pivotA,pivotB,axisA,axisB,frameA,frameB,anchor,useReferenceFrameA,ratio,rotOrder)\n"\
	"	\n"\
	"		Use different arguments for each type.\n"\
	"	\n"\
	"	HINGE_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.HINGE_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, frameA, frameB, 	\n"\
	"			useReferenceFrameA)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.HINGE_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, pivotA, pivotB, 	\n"\
	"			axisA, axisB, useReferenceFrameA)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.HINGE_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, frameA, useReferenceFrameA)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.HINGE_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, pivotA, axisA, useReferenceFrameA)	\n"\
	"\n"\
	"	GEAR_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.GEAR_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, axisA, axisB, ratio)	\n"\
	"\n"\
	"	POINT2POINT_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.POINT2POINT_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, pivotA, pivotB)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.POINT2POINT_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, pivotA)	\n"\
	"\n"\
	"	SLIDER_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.SLIDER_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, frameA, frameB, 	\n"\
	"			useReferenceFrameA)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.SLIDER_CONSTRAINT_TYPE, 	\n"\
	"			bodyB, frameB, useReferenceFrameA)	\n"\
	"\n"\
	"	D6_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.D6_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, frameA, frameB, 	\n"\
	"			useReferenceFrameA)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.D6_CONSTRAINT_TYPE, 	\n"\
	"			bodyB, frameB, useReferenceFrameA)	\n"\
	"\n"\
	"	CONETWIST_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.CONETWIST_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, frameA, frameB)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.CONETWIST_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, frameA)	\n"\
	"\n"\
	"	FIXED_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.FIXED_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, frameA, frameB);	\n"\
	"\n"\
	"	D6_SPRING_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.D6_SPRING_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, frameA, frameB, 	\n"\
	"			useReferenceFrameA)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.D6_SPRING_CONSTRAINT_TYPE, 	\n"\
	"			bodyB, frameB, useReferenceFrameA)	\n"\
	"\n"\
	"	D6_SPRING_2_CONSTRAINT_TYPE	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.D6_SPRING_2_CONSTRAINT_TYPE, 	\n"\
	"			bodyA, bodyB, frameA, frameB, rotOrder)	\n"\
	"		igeBullet.constraint(	\n"\
	"			igeBullet.D6_SPRING_2_CONSTRAINT_TYPE, 	\n"\
	"			bodyB, frameB, rotOrder)	\n"\
	"Parameters\n"\
	"----------\n"\
	"type : int\n"\
	"	type of constraint\n"\
	"		igeBullet.HINGE_CONSTRAINT_TYPE	\n"\
	"		igeBullet.GEAR_CONSTRAINT_TYPE	\n"\
	"		igeBullet.POINT2POINT_CONSTRAINT_TYPE	\n"\
	"		igeBullet.SLIDER_CONSTRAINT_TYPE	\n"\
	"		igeBullet.D6_CONSTRAINT_TYPE	\n"\
	"		igeBullet.CONETWIST_CONSTRAINT_TYPE	\n"\
	"		igeBullet.FIXED_CONSTRAINT_TYPE	\n"\
	"		igeBullet.D6_SPRING_CONSTRAINT_TYPE	\n"\
	"		igeBullet.D6_SPRING_2_CONSTRAINT_TYPE	\n"\
	"bodyA : igeBullet.rigidBody\n"\
	"bodyB : igeBullet.rigidBody\n"\
	"pivotA : tuple(x,y,z)\n"\
	"pivotB : tuple(x,y,z)\n"\
	"axisA : tuple(x,y,z)\n"\
	"axisB : tuple(x,y,z)\n"\
	"frameA : (position(x,y,z), rotation(x,y,z,w))\n"\
	"frameB : (position(x,y,z), rotation(x,y,z,w))\n"\
	"anchor\n"\
	"useReferenceFrameA\n"\
	"ratio\n"\
	"rotOrder\n"\
	"	igeBullet.RO_XYZ	\n"\
	"	igeBullet.RO_XZY	\n"\
	"	igeBullet.RO_YXZ	\n"\
	"	igeBullet.RO_YZX	\n"\
	"	igeBullet.RO_ZXY	\n"\
	"	igeBullet.RO_ZYX	\n");

PyDoc_STRVAR(setLimit_doc,
	"Set the limit of constraint movement\n"\
	"\n"\
	"HINGE_CONSTRAINT_TYPE	\n"\
	"	constraint.setLimit(low, high, _softness, _biasFactor, _relaxationFactor)\n"\
	"\n"\
	"FIXED_CONSTRAINT_TYPE	\n"\
	"D6_CONSTRAINT_TYPE, D6_SPRING_CONSTRAINT_TYPE, D6_SPRING_2_CONSTRAINT_TYPE	\n"\
	"	constraint.setLimit(axis, low, high)\n"\
	"\n"\
	"CONETWIST_CONSTRAINT_TYPE	\n"\
	"	constraint.setLimit(limitIndex, limitValue)	\n"\
	"	constraint.setLimit(_swingSpan1, _swingSpan2, _twistSpan, _softness, _biasFactor, _relaxationFactor)	\n"\
	"GEAR_CONSTRAINT_TYPE, POINT2POINT_CONSTRAINT_TYPE, SLIDER_CONSTRAINT_TYPE	\n"\
	"	No setLimit\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"	axis : int\n"\
	"		first 3 are linear, next 3 are angular\n"\
	"\n"\
	"	_softness : float\n"\
	"		0->1, recommend ~0.8->1.\n"\
	"		describes % of limits where movement is free.\n"\
	"		beyond this softness %, the limit is gradually enforced until the 'hard' (1.0) limit is reached.\n"\
	"	_biasFactor : float\n"\
	"		0->1?, recommend 0.3 +/-0.3 or so.\n"\
	"		strength with which constraint resists zeroth order (angular, not angular velocity) limit violation.\n"\
	"	 __relaxationFactor : float\n"\
	"		0->1, recommend to stay near 1.\n"\
	"		the lower the value, the less the constraint will fight velocities which violate the angular limits.\n"\
	"\n");


/////////////////////////////////////
/////////////////////////////////////
PyDoc_STRVAR(shape_doc,
	"3d physics shape\n"\
	"\n"\
	"Formula\n"\
	"----------\n"\
	"    create box shape\n"\
	"        shape = igeBullet.shape(igeBullet.BOX_SHAPE_PROXYTYPE, halfExtents = (1, 1, 1))\n"\
	"    create sphere shape\n"\
	"        shape = igeBullet.shape(igeBullet.SPHERE_SHAPE_PROXYTYPE, radius = 1)\n"\
	"    create capsule shape\n"\
	"        shape = igeBullet.shape(igeBullet.CAPSULE_SHAPE_PROXYTYPE, radius = 1, height = 1, axis = 1)\n"\
	"    create cone shape\n"\
	"        shape = igeBullet.shape(igeBullet.CONE_SHAPE_PROXYTYPE, radius = 1, height = 1, axis = 1)\n"\
	"    create cylinder shape\n"\
	"        shape = igeBullet.shape(igeBullet.CYLINDER_SHAPE_PROXYTYPE, halfExtents = (x, y, z), axis = 1)\n"\
	"    create static plane shape\n"\
	"        shape = igeBullet.shape(igeBullet.STATIC_PLANE_PROXYTYPE, normal = (x, y, z), constant = 1)\n"\
	"    create compound shape\n"\
	"        shape = igeBullet.shape(igeBullet.COMPOUND_SHAPE_PROXYTYPE)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    type\n"\
	"        shape type\n"\
	"        igeBullet.BOX_SHAPE_PROXYTYPE : box shape\n"\
	"        igeBullet.SPHERE_SHAPE_PROXYTYPE : sphere shape\n"\
	"        igeBullet.CAPSULE_SHAPE_PROXYTYPE : capsule shape\n"\
	"        igeBullet.CONE_SHAPE_PROXYTYPE : cone shape\n"\
	"        igeBullet.CYLINDER_SHAPE_PROXYTYPE : cylinder shape\n"\
	"        igeBullet.STATIC_PLANE_PROXYTYPE static plane shape\n"\
	"        igeBullet.COMPOUND_SHAPE_PROXYTYPE compound shape\n"\
	"    radius\n"\
	"        radius of sphere or capsule or cone\n"\
	"    height\n"\
	"        height of capsule or cone\n"\
	"    halfExtents\n"\
	"        half length of each side x,y,z\n"\
	"    normal\n"\
	"        normal of plane\n"\
	"    constant\n"\
	"        plane position along normal\n"\
	"    axis\n"\
	"        the value indicating the vertical direction of the shape	\n"\
	"        0:X,  1:Y,  2:Z (default is Y) ");

PyDoc_STRVAR(getMeshData_doc,
	"get rendering data\n"\
	"\n"\
	"pos, nom, uv, idx = shape.getMeshData()\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    pos\n"\
	"        list of vertex positions (x,y,z, x,y,z, ...)\n"\
	"    nom\n"\
	"        list of vertex normals (x,y,z, x,y,z, ...)\n"\
	"    uv\n"\
	"        list of vertex uvs (u,v, u,v, ...)\n"\
	"    idx\n"\
	"        list of triangle indices\n");

PyDoc_STRVAR(addChildShape_doc,
	"Use this method for adding children.\n"\
	"Only Convex shapes are allowed.\n"\
	"\n"\
	"shape.addChildShape(shape, pos, rot)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    shape : igeBullet.shape\n"\
	"        shape object\n"\
	"    pos : tuple of float (x,y,z)\n"\
	"        offset location of object\n"\
	"    rot : tuple of float (x,y,z,w)\n"\
	"        offset orientation of object\n");

/////////////////////////////////////
/////////////////////////////////////
PyDoc_STRVAR(rigidbody_doc,
	"3d physics rigid body\n"\
	"\n"\
	"igeBullet.rigidBody(shape, mass, pos, rot, activate)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    shape : igeBullet.shape\n"\
	"        shape object\n"\
	"    mass : float\n"\
	"        mass of object\n"\
	"    pos : tuple of float (x,y,z)\n"\
	"        start location of object\n"\
	"    rot : tuple of float (x,y,z,w)\n"\
	"        start orientation of object\n"\
	"    activate : bool\n"\
	"        Whether the physics calculation is active.\n"\
	"        Do not calculate unless external force is applied\n");

PyDoc_STRVAR(rigidbody_position_doc,
	"rigit body position\n"\
	"\n"\
	"	type :  tuple of float (x,y,z)\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_rotation_doc,
	"rigit body position\n"\
	"\n"\
	"	type :  tuple of float(x,y,z,w)\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_friction_doc,
	"rigit body friction\n"\
	"\n"\
	"	type :  float\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_restitution_doc,
	"rigit body restitution\n"\
	"\n"\
	"	type :  float\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_shape_doc,
	"shape object\n"\
	"\n"\
	"	type :  igeBullet.shape\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_enableCollisionCallback_doc,
	"Whether collision callback is enabled\n"\
	"\n"\
	"	type :  bool\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_enableContactResponse_doc,
	"Whether contact response is enabled\n"\
	"\n"\
	"	type :  bool\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_collisionGroupBit_doc,
	"Own collision filter bit\n"\
	"\n"\
	"	type :  int\n"\
	"	(1, 2, 4, 8, 16...16384)\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_collisionGroupMask_doc,
	"Collision filter bit for which you want to enable collision\n"\
	"\n"\
	"	type :  int\n"\
	"	(1, 2, 4, 8, 16...16384)\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_linearDamping_doc,
	"rigid body linear damping\n"\
	"\n"\
	"	type :  float\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_angularDamping_doc,
	"rigid body angular damping\n"\
	"\n"\
	"	type :  float\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_linearVelocity_doc,
	"rigid body linear velocity\n"\
	"\n"\
	"	type :  tuple of float(x,y,z)\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_angularVelocity_doc,
	"rigid body angular velocity\n"\
	"\n"\
	"	type :  tuple of float(x,y,z)\n"\
	"	read / write");

PyDoc_STRVAR(rigidbody_angularSleepingThreshold_doc,
	"The maximum amount of rotation that rigid body can go to sleep.\n"\
	"If the amount of rotation is less than this value, I think it will go to sleep.\n"\
	"\n"\
	"	type :  float  (read / write)");
PyDoc_STRVAR(rigidbody_linearSleepingThreshold_doc,
	"The maximum amount of movement that rigid body can go to sleep.\n"\
	"If the amount of movement is less than this value, I think it will go to sleep.\n"\
	"\n"\
	"	type :  float (read / write)");

PyDoc_STRVAR(rigidbody_deactivationTime_doc,
	"The time after which a resting rigidbody gets deactived.\n"\
	"\n"\
	"	type :  float (read / write)");

PyDoc_STRVAR(rigidbody_activationState_doc,
	"Whether rigidbody is active.\n"\
	"Setting False will clear the Force.\n"\
	"\n"\
	"	type :  bool (read / write)");


PyDoc_STRVAR(applyTorque_doc,
	" Applies a torque on a rigid body.\n"\
	"\n"\
	"digidBody.applyTorque(torque)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    torque : tuple of float(x,y,z)\n");

PyDoc_STRVAR(applyForce_doc,
	"Applies a force on a rigid body.\n"\
	"If position is not specified, force is applied to the center.\n"\
	"\n"\
	"digidBody.applyForce(torque, position)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    force : tuple of float(x,y,z)\n"\
	"    position : tuple of float(x,y,z)  (optional)\n");

PyDoc_STRVAR(applyImpulse_doc,
	" Applies a impulse on a rigid body.\n"\
	"If position is not specified, force is applied to the center.\n"\
	"\n"\
	"digidBody.applyImpulse(impulse)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    impulse : tuple of float(x,y,z)\n"\
	"    position : tuple of float(x,y,z)  (optional)\n");

PyDoc_STRVAR(clearForces_doc,
	"The forces on each rigidbody is accumulating together with gravity.\n"\
	"clear this after each timestep.\n"\
	"\n"\
	"digidBody.clearForces()");

PyDoc_STRVAR(setMass_doc,
	"Change the mass of rigid body.\n"\
	"\n"\
	"	To update correctly\n"\
	"	world.rerease(body)\n"\
	"	body.setMass(mass)\n"\
	"	world.add(body)\n"\
	"	will do\n"\
	"\n"\
	"	digidBody.setMass(mass)\n"\
	"Parameters\n"\
	"----------\n"\
	"	mass : float\n");


/////////////////////////////////////
/////////////////////////////////////
PyDoc_STRVAR(dynworld_doc,
	"3d physics world\n");

PyDoc_STRVAR(gravity_doc,
	"gravity vector\n"\
	"\n"\
	"    type :  tuple of float(x,y,z)\n"\
	"        read / write");


PyDoc_STRVAR(add_doc,
	"Add rigidbody or constarain to world\n"\
	"\n"\
	"world.add(object)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    object : rigidBody or constrain\n"\
	"        rigidBody or constrain objecrt add to world.");

PyDoc_STRVAR(remove_doc,
	"Remove rigidbody or constarain from world\n"\
	"\n"\
	"world.remove(object)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    object : rigidBody or constrain\n"\
	"        rigidBody or constrain objecrt remove from world.");

PyDoc_STRVAR(clear_doc,
	"Clear all added rigidbody and constarain\n"\
	"\n"\
	"world.clear()\n"\
	"\n");

PyDoc_STRVAR(step_doc,
	"step simulation\n"\
	"\n"\
	"world.step()\n"\
	"\n");

PyDoc_STRVAR(wait_doc,
	"wait until async simultion is end\n"\
	"\n"\
	"world.wait()\n"\
	"\n");


PyDoc_STRVAR(getNumCollisionObjects_doc,
	"get number of collision objects in the world\n"\
	"\n"\
	"num = world.getNumCollisionObjects()\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    num : int\n"\
	"        number of collision objects");


PyDoc_STRVAR(getRigidBody_doc,
	"get collision object\n"\
	"\n"\
	"obj = world.getRigidBody(index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    index : int\n"\
	"        index of added rigidBody(Order added)\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    obj : rigidBody\n"\
	"        rigidBody object");

PyDoc_STRVAR(rayTestOne_doc,
	"Find most nearest Intersection between \n"\
	"line segment(start-end)and a collision object in the world.\n"\
	"\n"\
	"result = world.rayTestOne(start, end, mask)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    start : tuple of float(x,y,z)\n"\
	"        start position of ray line segment\n"\
	"    end : tuple of float(x,y,z)\n"\
	"        end position of ray line segment\n"\
	"    mask : int  (optional)\n"\
	"        Collision filter mask (default -1 (all objects))\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    result\n"\
	"        dictionary of contact point infomation\n"\
	"        {'collisionObject' : igeBullet.rigidbody,\n"\
	"         'hitPosition': tuple of float(x,y,z),\n"\
	"         'hitNormal' : tuple of float(x,y,z),\n"\
	"         'index' : int}");


PyDoc_STRVAR(rayTestAll_doc,
	"Find all Intersection between \n"\
	"line segment(start-end)and a collision object in the world.\n"\
	"\n"\
	"result = world.rayTestOne(start, end, mask)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    start : tuple of float(x,y,z)\n"\
	"        start position of ray line segment\n"\
	"    end : tuple of float(x,y,z)\n"\
	"        end position of ray line segment\n"\
	"    mask : int  (optional)\n"\
	"        Collision filter mask (default -1 (all objects))\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    result\n"\
	"        tuple of all dictionary of contact point infomation\n"\
	"        ({'collisionObject' : igeBullet.rigidbody,\n"\
	"         'hitPosition': tuple of float(x,y,z),\n"\
	"         'hitNormal' : tuple of float(x,y,z),\n"\
	"         'index' : int},\n"\
	"         {},{}...)");

PyDoc_STRVAR(contactTest_doc,
	"Collision between specified object and other objects in the world\n"\
	"\n"\
	"result = world.contactTest(object, mask)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    object : igeBullet.rigidBody\n"\
	"        Object that you want to detect collision\n"\
	"    mask : int  (optional)\n"\
	"        Collision filter mask (default -1 (all objects))\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    result\n"\
	"    tuple of dictionary of contact infomation\n"\
	"    ({'objectA' : igeBullet.rigidBody,\n"\
	"      'objectB' : igeBullet.rigidBody,\n"\
	"      'localPosA' : tuple of float(x,y,z),\n"\
	"      'localPosB' : tuple of float(x,y,z),\n"\
	"      'worldPosA' : tuple of float(x,y,z),\n"\
	"      'worldPosB' : tuple of float(x,y,z),\n"\
	"      'normal' : tuple of float(x,y,z)}, {}, {},...)\n");

PyDoc_STRVAR(contactPairTest_doc,
	"Collision detection between two objects\n"\
	"\n"\
	"result = world.contactPairTest(objectA,objectB, mask)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    objectA : igeBullet.rigidBody\n"\
	"        Object that you want to detect collision\n"\
	"    objectB : igeBullet.rigidBody\n"\
	"        Object that you want to detect collision\n"\
	"    mask : int  (optional)\n"\
	"        Collision filter mask (default -1 (all objects))\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    result\n"\
	"    tuple of dictionary of contact infomation\n"\
	"    ({'objectA' : igeBullet.rigidBody,\n"\
	"      'objectB' : igeBullet.rigidBody,\n"\
	"      'localPosA' : tuple of float(x,y,z),\n"\
	"      'localPosB' : tuple of float(x,y,z),\n"\
	"      'worldPosA' : tuple of float(x,y,z),\n"\
	"      'worldPosB' : tuple of float(x,y,z),\n"\
	"      'normal' : tuple of float(x,y,z)}, {}, {},...)\n");

PyDoc_STRVAR(convexSweepTest_doc, "");

