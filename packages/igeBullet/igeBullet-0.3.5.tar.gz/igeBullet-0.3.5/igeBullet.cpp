#include <Python.h>
#include <stdio.h>
#include "igeBullet_doc_en.h"
#include "igeBullet.h"
#include <vector>

#include "btBulletDynamicsCommon.h"
#include "BulletCollision/CollisionDispatch/btGhostObject.h"
#include "BulletDynamics/Character/btKinematicCharacterController.h"

#if defined _WIN32             //WIN32
#   include <time.h>
#   include <Windows.h>
#elif defined __APPLE__
#   include "TargetConditionals.h"
#   if TARGET_OS_IPHONE        //iOS
#       include <sys/types.h>
#   else                       //OSX
#       include <time.h>
#   endif
#	include <mach/mach_time.h>
#elif defined __ANDROID__      //Android
#   include <sys/time.h>
#   include <time.h>
#endif

static PyTypeObject* Vec2Type = nullptr;
static PyTypeObject* Vec3Type = nullptr;
static PyTypeObject* Vec4Type = nullptr;
static PyTypeObject* QuatType = nullptr;
static PyTypeObject* Mat22Type = nullptr;
static PyTypeObject* Mat33Type = nullptr;
static PyTypeObject* Mat44Type = nullptr;
typedef struct {
	PyObject_HEAD
		float v[4];
	int d;
} vec_obj;

typedef struct {
	PyObject_HEAD
		float m[16];
	int d;
} mat_obj;

typedef struct {
	PyObject_HEAD
		float min[4];
	float max[4];
	int d;
} aabb_obj;

#if defined(__APPLE__)
	mach_timebase_info_data_t base;
#endif

PyObject* createCollisionShapeGraphicsObject(btCollisionShape* collisionShape);

bool pyObjToVector(PyObject* obj, btVector3& v) {

	if (obj) {
		int d;
		v.m_floats[0] = v.m_floats[1] = v.m_floats[2] = v.m_floats[3] = 0.0f;
		if (obj->ob_type == Vec3Type || obj->ob_type == Vec4Type || obj->ob_type == QuatType) {
			d = ((vec_obj*)(obj))->d;
			for (int j = 0; j < d; j++) {
				v.m_floats[j] = ((vec_obj*)(obj))->v[j];
			}
			return true;
		}
		else if (PyTuple_Check(obj)) {
			d = (int)PyTuple_Size(obj);
			if (d > 4) d = 4;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyTuple_GET_ITEM(obj, j);
				v.m_floats[j] = (float)PyFloat_AsDouble(val);
			}
			return true;
		}
		else if (PyList_Check(obj)) {
			d = (int)PyList_Size(obj);
			if (d > 4) d = 4;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyList_GET_ITEM(obj, j);
				v.m_floats[j] = (float)PyFloat_AsDouble(val);
			}
			return true;
		}
	}
	PyErr_SetString(PyExc_ValueError, "invalid arguments");
	return  false;
}
bool pyObjToTransform(PyObject* obj, btTransform& t) {

	btQuaternion q;

	if (obj) {
		if (PyTuple_Check(obj)) {
			if (PyTuple_Size(obj) != 2) goto error;
			if (!pyObjToVector(PyTuple_GET_ITEM(obj, 0), t.getOrigin())) goto error;
			if (!pyObjToVector(PyTuple_GET_ITEM(obj, 1), *((btVector3*)&q))) goto error;
			t.setRotation(q);
			return true;
		}
		else if (PyList_Check(obj)) {
			if (PyList_Size(obj) != 2) goto error;
			if (!pyObjToVector(PyList_GET_ITEM(obj, 0), t.getOrigin())) goto error;
			if (!pyObjToVector(PyList_GET_ITEM(obj, 1), *((btVector3*)& q))) goto error;
			t.setRotation(q);
			return true;
		}
	}
error:
	PyErr_SetString(PyExc_ValueError, "invalid arguments");
	return  false;
}


//////////////////////////////////////////////////////////////////////
//Vehicle
//////////////////////////////////////////////////////////////////////
#if true

PyObject* vehicle_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "world","rigidBody",NULL };
	world_obj* world = nullptr;
	rigidbody_obj* body = nullptr;
	if (!PyArg_ParseTupleAndKeywords(args, kw, "OO", kwlist,&world,&body))
		return NULL;

	vehicle_obj* self = (vehicle_obj*)type->tp_alloc(type, 0);
	if (!self) return NULL;

	self->btTuning = new btRaycastVehicle::btVehicleTuning;
	self->btVehicleRayCaster = new btDefaultVehicleRaycaster((btDynamicsWorld*)(world->btworld));
	self->btVehicle = new btRaycastVehicle(*((btRaycastVehicle::btVehicleTuning*)(self->btTuning)), (btRigidBody*)(body->btbody), (btDefaultVehicleRaycaster*)(self->btVehicleRayCaster));
	((btRaycastVehicle*)(self->btVehicle))->setCoordinateSystem(0, 1, 2);

	///never deactivate the vehicle
	((btRigidBody*)(body->btbody))->setActivationState(DISABLE_DEACTIVATION);
	Py_INCREF(body);

	return (PyObject*)self;
}

void vehicle_dealloc(vehicle_obj* self)
{
	rigidbody_obj* bodyObj = (rigidbody_obj*)((btRaycastVehicle*)self->btVehicle)->getRigidBody()->getUserPointer();
	Py_DECREF(bodyObj);
	if (self->btVehicle) delete (btRaycastVehicle*)(self->btVehicle);
	if (self->btTuning) delete (btRaycastVehicle::btVehicleTuning*)(self->btTuning);
	if (self->btVehicleRayCaster) delete (btDefaultVehicleRaycaster*)(self->btVehicleRayCaster);

	Py_TYPE(self)->tp_free(self);
}

PyObject* vehicle_str(vehicle_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics vehicle object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* vehicle_addWheel(vehicle_obj* self, PyObject* args, PyObject* kw) 
{
	static char* kwlist[] = { "connectionPointCS","wheelDirectionCS0","wheelAxleCS","suspensionRestLength","wheelRadius","isFrontWheel",NULL };
	PyObject* connectionPointCS_o = nullptr;
	PyObject* wheelDirectionCS0_o = nullptr;
	PyObject* wheelAxleCS_o = nullptr;
	float suspensionRestLength = 1.0f;
	float wheelRadius = 1.0f;
	int isFrontWheel = true;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "O|OOffi", kwlist, 
		&connectionPointCS_o, &wheelDirectionCS0_o, &wheelAxleCS_o, &suspensionRestLength, &wheelRadius, &isFrontWheel))
		return NULL;

	btVector3 connectionPointCS;
	btVector3 wheelDirectionCS0(0, -1, 0);
	btVector3 wheelAxleCS(-1, 0, 0);
	if (connectionPointCS_o) {
		if (!pyObjToVector(connectionPointCS_o, connectionPointCS)) return NULL;
	}
	if (wheelDirectionCS0_o) {
		if (!pyObjToVector(wheelDirectionCS0_o, wheelDirectionCS0)) return NULL;
	}
	if (wheelAxleCS_o) {
		if (!pyObjToVector(wheelAxleCS_o, wheelAxleCS)) return NULL;
	}

	((btRaycastVehicle*)self->btVehicle)->addWheel(
		connectionPointCS, wheelDirectionCS0, wheelAxleCS, 
		suspensionRestLength, wheelRadius, *((btRaycastVehicle::btVehicleTuning*)(self->btTuning)),  (bool)isFrontWheel);

	int idx = ((btRaycastVehicle*)self->btVehicle)->getNumWheels() -1;
	btWheelInfo& wheel = ((btRaycastVehicle*)self->btVehicle)->getWheelInfo(idx);
	wheel.m_suspensionStiffness = 20.f;
	wheel.m_wheelsDampingRelaxation = 2.3f;
	wheel.m_wheelsDampingCompression = 4.4f;
	wheel.m_frictionSlip = 1000;
	wheel.m_rollInfluence = 0.1f;

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* vehicle_setSteeringValue(vehicle_obj* self, PyObject* args) 
{
	float steering;
	int wheel;
	if (!PyArg_ParseTuple(args, "fi", &steering, &wheel)) {
		return NULL;
	}
	((btRaycastVehicle*)self->btVehicle)->setSteeringValue(steering, wheel);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* vehicle_applyEngineForce(vehicle_obj* self, PyObject* args)
{
	float force;
	int wheel;
	if (!PyArg_ParseTuple(args, "fi", &force, &wheel)) {
		return NULL;
	}
	((btRaycastVehicle*)self->btVehicle)->applyEngineForce(force, wheel);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* vehicle_setBrake(vehicle_obj* self, PyObject* args)
{
	float brake;
	int wheel;
	if (!PyArg_ParseTuple(args, "fi", &brake, &wheel)) {
		return NULL;
	}
	((btRaycastVehicle*)self->btVehicle)->setBrake(brake, wheel);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* vehicle_getWheelPosition(vehicle_obj* self, PyObject* args)
{
	int wheel;
	if (!PyArg_ParseTuple(args, "i", &wheel)) {
		return NULL;
	}
	btVector3& pos = ((btRaycastVehicle*)self->btVehicle)->getWheelInfo(wheel).m_worldTransform.getOrigin();
	return Py_BuildValue("(fff)", pos.getX(), pos.getY(), pos.getZ());	
}

static PyObject* vehicle_getWheelRotation(vehicle_obj* self, PyObject* args)
{
	int wheel;
	if (!PyArg_ParseTuple(args, "i", &wheel)) {
		return NULL;
	}
	btQuaternion rot = ((btRaycastVehicle*)self->btVehicle)->getWheelInfo(wheel).m_worldTransform.getRotation();
	return Py_BuildValue("(ffff)", rot.getX(), rot.getY(), rot.getZ(), rot.getW());	
}

PyMethodDef vehicle_methods[] = {
	{ "addWheel", (PyCFunction)vehicle_addWheel, METH_VARARGS | METH_KEYWORDS, addWheel_doc},
	{ "setSteeringValue", (PyCFunction)vehicle_setSteeringValue, METH_VARARGS, setSteeringValue_doc},
	{ "applyEngineForce", (PyCFunction)vehicle_applyEngineForce, METH_VARARGS, applyEngineForce_doc},
	{ "setBrake", (PyCFunction)vehicle_setBrake, METH_VARARGS, setBrake_doc},
	{ "getWheelPosition", (PyCFunction)vehicle_getWheelPosition, METH_VARARGS, getWheelPosition_doc},
	{ "getWheelRotation", (PyCFunction)vehicle_getWheelRotation, METH_VARARGS, getWheelRotation_doc},


	{ NULL,	NULL }
};

PyGetSetDef vehicle_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject VehicleType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.vehicle",				/* tp_name */
	sizeof(vehicle_obj),                /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)vehicle_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)vehicle_str,             /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	vehicle_doc,						/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	vehicle_methods,					/* tp_methods */
	0,                                  /* tp_members */
	vehicle_getsets,                   /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	vehicle_new,						/* tp_new */
	0,									/* tp_free */
};



#endif

//////////////////////////////////////////////////////////////////////
//Constraint
//////////////////////////////////////////////////////////////////////
#if true

/*
POINT2POINT_CONSTRAINT_TYPE = 3,
HINGE_CONSTRAINT_TYPE,
CONETWIST_CONSTRAINT_TYPE,
D6_CONSTRAINT_TYPE,
SLIDER_CONSTRAINT_TYPE,
CONTACT_CONSTRAINT_TYPE,
D6_SPRING_CONSTRAINT_TYPE,
GEAR_CONSTRAINT_TYPE,
FIXED_CONSTRAINT_TYPE,
D6_SPRING_2_CONSTRAINT_TYPE,
*/

PyObject* constraint_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "type", "bodyA","bodyB","pivotA","pivotB","axisA","axisB","frameA","frameB", "anchor", "useReferenceFrameA","ratio","rotOrder",NULL };

	int constrainttype = -1;
	rigidbody_obj* o_bodyA = nullptr;
	rigidbody_obj* o_bodyB = nullptr;
	PyObject* o_pivotA = nullptr;
	PyObject* o_pivotB = nullptr;
	PyObject* o_axisA = nullptr;
	PyObject* o_axisB = nullptr;
	PyObject* o_frameA = nullptr;
	PyObject* o_frameB = nullptr;
	PyObject* o_anchor = nullptr;
	int useReferenceFrameA = false;
	float ratio = 1.0f;
	int rotOrder = RO_XYZ;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "i|OOOOOOOOOpfi", kwlist,
		&constrainttype, 
		&o_bodyA, &o_bodyB, &o_pivotA, &o_pivotB, &o_axisA, &o_axisB, &o_frameA, &o_frameB, &o_anchor, 
		&useReferenceFrameA,&ratio,&rotOrder))
		return NULL;

	btRigidBody* bodyA;
	btRigidBody* bodyB;
	btVector3 pivotA, pivotB, axisA, axisB, anchor;
	btTransform frameA, frameB;

	if (o_bodyA) bodyA = (btRigidBody*)o_bodyA->btbody;
	if (o_bodyB) bodyB = (btRigidBody*)o_bodyB->btbody;
	if (o_pivotA)
		if (!pyObjToVector(o_pivotA, pivotA)) return NULL;
	if (o_pivotB)
		if (!pyObjToVector(o_pivotB, pivotB)) return NULL;
	if (o_axisA)
		if (!pyObjToVector(o_axisA, axisA)) return NULL;
	if (o_axisB)
		if (!pyObjToVector(o_axisB, axisB)) return NULL;
	if (o_frameA)
		if (!pyObjToTransform(o_frameA, frameA)) return NULL;
	if (o_frameB)
		if (!pyObjToTransform(o_frameB, frameB)) return NULL;
	if (o_anchor)
		if (!pyObjToVector(o_anchor, anchor)) return NULL;

	btTypedConstraint* constraint = nullptr;
	switch (constrainttype) {
	case HINGE_CONSTRAINT_TYPE: 				//btHingeConstraint
		if (o_bodyA) {
			if (o_bodyB) {
				if (o_frameA && o_frameB)
					constraint = new btHingeConstraint(*bodyA, *bodyB, frameA, frameB, useReferenceFrameA);
				else if (o_pivotA && o_pivotB && o_axisA && o_axisB)
					constraint = new btHingeConstraint(*bodyA, *bodyB, pivotA, pivotB, axisA, axisB, useReferenceFrameA);
			}
			else {
				if (o_frameA)
					constraint = new btHingeConstraint(*bodyA, frameA, useReferenceFrameA);
				else if (o_pivotA && o_axisA)
					constraint = new btHingeConstraint(*bodyA, pivotA, axisA, useReferenceFrameA);
			}
		}
		break;
	//case HINGE2_CONSTRAINTTYPE:				//btHinge2Constraint
	//	if (o_bodyA && o_bodyB && o_anchor && o_axisA && o_axisB) {
	//		constraint = new btHinge2Constraint(*bodyA, *bodyB, anchor, axisA, axisB);
	//	}
	//	break;
	case GEAR_CONSTRAINT_TYPE:				//btGearConstraint
		if (o_bodyA && o_bodyB && o_axisA && o_axisB) {
			constraint = new btGearConstraint(*bodyA, *bodyB, axisA, axisB, ratio);
		}
		break;
	case POINT2POINT_CONSTRAINT_TYPE:		//btPoint2PointConstraint
		if (o_bodyA && o_pivotA) {
			if (o_bodyB && o_pivotB) {
				constraint = new btPoint2PointConstraint(*bodyA, *bodyB, pivotA, pivotB);
			}
			else {
				constraint = new btPoint2PointConstraint(*bodyA, pivotA);
			}
		}
		break;
	case SLIDER_CONSTRAINT_TYPE:				//btSliderConstraint
		if (o_bodyB && o_frameB) {
			if (o_bodyA && o_frameA) {
				constraint = new btSliderConstraint(*bodyA, *bodyB, frameA, frameB, useReferenceFrameA);
			}
			else {
				constraint = new btSliderConstraint(*bodyB, frameB, useReferenceFrameA);
			}
		}
		break;
	case D6_CONSTRAINT_TYPE:		//btGeneric6DofConstraint
		if (o_bodyB && o_frameB) {
			if (o_bodyA && o_frameA) {
				constraint = new btGeneric6DofConstraint(*bodyA, *bodyB, frameA, frameB, useReferenceFrameA);
			}
			else {
				constraint = new btGeneric6DofConstraint(*bodyB, frameB, useReferenceFrameA);
			}
			break;
	case CONETWIST_CONSTRAINT_TYPE:			//btConeTwistConstraint
		if (o_bodyA && o_frameA) {
			if (o_bodyB && o_frameB) {
				constraint = new btConeTwistConstraint(*bodyA, *bodyB, frameA, frameB);
			}
			else {
				constraint = new btConeTwistConstraint(*bodyA, frameA);
			}
		}
		break;
	//case UNIVERSAL_CONSTRAINTTYPE:			//btUniversalConstraint
	//	if (o_bodyA && o_bodyB && o_anchor && o_axisA && o_axisB) {
	//		constraint = new btUniversalConstraint(*bodyA, *bodyB, anchor, axisA, axisB);
	//	}
	//	break;
	case FIXED_CONSTRAINT_TYPE:				//btFixedConstraint
		if (o_bodyA && o_bodyB && o_frameA && o_frameB) {
			constraint = new btFixedConstraint(*bodyA, *bodyB, frameA, frameB);
		}
		break;
	case D6_SPRING_CONSTRAINT_TYPE:
		if (o_bodyA && o_frameA) {
			if (o_bodyB && o_frameB) {
				constraint = new btGeneric6DofSpringConstraint(*bodyA, *bodyB, frameA, frameB, useReferenceFrameA);
			}
			else {
				constraint = new btGeneric6DofSpringConstraint(*bodyB, frameB, useReferenceFrameA);
			}
		}
		break;
	case D6_SPRING_2_CONSTRAINT_TYPE:	//btGeneric6DofSpring2Constraint
		if (o_bodyA && o_frameA) {
			if (o_bodyB && o_frameB) {
				constraint = new btGeneric6DofSpring2Constraint(*bodyA, *bodyB, frameA, frameB, (RotateOrder)rotOrder);
			}
			else {
				constraint = new btGeneric6DofSpring2Constraint(*bodyB, frameB, (RotateOrder)rotOrder);
			}
		}
		break;
		}
	}

	if (!constraint) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}

	constraint_obj* self = (constraint_obj*)type->tp_alloc(type, 0);
	if (!self) return NULL;
	constraint->setUserConstraintPtr(self);
	self->btconstraint = constraint;

	return (PyObject*)self;
}

void  constraint_dealloc(constraint_obj* self)
{
	if(self->btconstraint) delete ((btTypedConstraint*)self->btconstraint);
	Py_TYPE(self)->tp_free(self);
}

PyObject* constraint_str(constraint_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics constrain object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* constraint_setLimit(constraint_obj* self, PyObject* args) {

	btScalar low;
	btScalar high;
	int axis = 0;
	btScalar _softness = 1.f;
	btScalar _biasFactor = 0.3f;
	btScalar _relaxationFactor = 1.0f;


	switch (((btTypedConstraint*)(self->btconstraint))->getConstraintType()) {
	case HINGE_CONSTRAINT_TYPE: 		//btHingeConstraint
		_softness = 0.9f;
		if (!PyArg_ParseTuple(args, "ff|fff", &low, &high, &_softness, &_biasFactor, &_relaxationFactor)) return NULL;
		((btHingeConstraint*)(self->btconstraint))->setLimit(low, high, _softness, _biasFactor, _relaxationFactor);
		break;
	case GEAR_CONSTRAINT_TYPE:			//btGearConstraint
		break;
	case POINT2POINT_CONSTRAINT_TYPE:	//btPoint2PointConstraint
		break;
	case SLIDER_CONSTRAINT_TYPE:		//btSliderConstraint
		break;
	case D6_CONSTRAINT_TYPE:			//btGeneric6DofConstraint
		if (!PyArg_ParseTuple(args, "iff", &axis, &low, &high)) return NULL;
		((btGeneric6DofConstraint*)(self->btconstraint))->setLimit(axis, low, high);
		break;
	case CONETWIST_CONSTRAINT_TYPE:		//btConeTwistConstraint
	{
		PyObject* arg1;
		btScalar val2;
		btScalar val3 = FLT_MAX;
		if (!PyArg_ParseTuple(args, "Of|ffff", &arg1, &val2, &val3, &_softness, &_biasFactor, &_relaxationFactor)) return NULL;
		if (val3 == FLT_MAX) {
			int limitIndex = (int)PyLong_AsLong(arg1);
			((btConeTwistConstraint*)(self->btconstraint))->setLimit(limitIndex, val2);
		}
		else {
			btScalar val1 = (btScalar)PyFloat_AsDouble(arg1);
			((btConeTwistConstraint*)(self->btconstraint))->setLimit(val1, val2, val3, _softness, _biasFactor, _relaxationFactor);
		}
	}
		break;
	case FIXED_CONSTRAINT_TYPE:			//btFixedConstraint
		if (!PyArg_ParseTuple(args, "iff", &axis, &low, &high)) return NULL;
		((btFixedConstraint*)(self->btconstraint))->setLimit(axis, low, high);
		break;
	case D6_SPRING_CONSTRAINT_TYPE:		//btGeneric6DofSpringConstraint
		if (!PyArg_ParseTuple(args, "iff", &axis, &low, &high)) return NULL;
		((btGeneric6DofSpringConstraint*)(self->btconstraint))->setLimit(axis, low, high);
		break;
	case D6_SPRING_2_CONSTRAINT_TYPE:	//btGeneric6DofSpring2Constraint
		if (!PyArg_ParseTuple(args, "iff", &axis, &low, &high)) return NULL;
		((btGeneric6DofSpring2Constraint*)(self->btconstraint))->setLimit(axis, low, high);
		break;
	}

	Py_INCREF(Py_None);
	return Py_None;

}


PyMethodDef constraint_methods[] = {
	{ "setLimit", (PyCFunction)constraint_setLimit, METH_VARARGS, setLimit_doc},
	{ NULL,	NULL }
};

PyGetSetDef constraint_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject ConstraintType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.constraint",				/* tp_name */
	sizeof(constraint_obj),             /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)constraint_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)constraint_str,           /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	constraint_doc,						/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	constraint_methods,					/* tp_methods */
	0,                                  /* tp_members */
	constraint_getsets,                 /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	constraint_new,						/* tp_new */
	0,									/* tp_free */
};



#endif

//////////////////////////////////////////////////////////////////////
//Shape
//////////////////////////////////////////////////////////////////////
#if true

PyObject* shape_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "type","radius","height","halfExtents","normal","constant", "axis", NULL };
	int shapetype;
	float radius=1.0f;
	float height = 1.0f;
	PyObject* halfExtents = nullptr;
	PyObject* normal = nullptr;
	float constant = 0.0f;
	int axis = 1;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "i|ffOOfi", kwlist,
		&shapetype, &radius, &height, &halfExtents, &normal, &constant, &axis))
		return NULL;

	btVector3 v;
	btScalar f;
	btCollisionShape* shape=nullptr;

	switch (shapetype) {
	case BOX_SHAPE_PROXYTYPE:
		if (!pyObjToVector(halfExtents, v)) return NULL;
		shape = new btBoxShape(v);
		break;
	case SPHERE_SHAPE_PROXYTYPE:
		shape = new btSphereShape(radius);
		break;
	case CAPSULE_SHAPE_PROXYTYPE:
		if (axis == 0)
			shape = new btCapsuleShapeX(radius, height);
		else if (axis == 1)
			shape = new btCapsuleShape(radius, height);
		else if (axis == 2)
			shape = new btCapsuleShapeZ(radius, height);
		break;
	case CONE_SHAPE_PROXYTYPE:
		if (axis == 0)
			shape = new btConeShapeX(radius, height);
		else if (axis == 1)
			shape = new btConeShape(radius, height);
		else if (axis == 2)
			shape = new btConeShapeZ(radius, height);
		break;
	case CYLINDER_SHAPE_PROXYTYPE:
		if (!pyObjToVector(halfExtents, v)) return NULL;
		if (axis == 0)
			shape = new btCylinderShapeX(v);
		else if (axis == 1)
			shape = new btCylinderShape(v);
		else if (axis == 2)
			shape = new btCylinderShapeZ(v);
		break;
	case STATIC_PLANE_PROXYTYPE:
		if (!pyObjToVector(normal, v)) return NULL;
		shape = new btStaticPlaneShape(v, constant);
		break;
	case COMPOUND_SHAPE_PROXYTYPE:
		shape = new btCompoundShape();
		break;
	//case TRIANGLE_SHAPE_PROXYTYPE:
	//	shape = new btTriangleShape
	//	break;
	//case TETRAHEDRAL_SHAPE_PROXYTYPE:
	//	break;
	//case CONVEX_TRIANGLEMESH_SHAPE_PROXYTYPE:
	//	break;
	case CONVEX_HULL_SHAPE_PROXYTYPE:
		break;
	case CONVEX_POINT_CLOUD_SHAPE_PROXYTYPE:
		break;
	case CUSTOM_POLYHEDRAL_SHAPE_TYPE:
		break;
	case MULTI_SPHERE_SHAPE_PROXYTYPE:
		break;
	case CONVEX_SHAPE_PROXYTYPE:
		break;
	case UNIFORM_SCALING_SHAPE_PROXYTYPE:
		break;
	case MINKOWSKI_SUM_SHAPE_PROXYTYPE:
		break;
	case MINKOWSKI_DIFFERENCE_SHAPE_PROXYTYPE:
		break;
	case BOX_2D_SHAPE_PROXYTYPE:
		break;
	case TRIANGLE_MESH_SHAPE_PROXYTYPE:
		break;
	case SCALED_TRIANGLE_MESH_SHAPE_PROXYTYPE:
		break;
	case TERRAIN_SHAPE_PROXYTYPE:
		break;
	case GIMPACT_SHAPE_PROXYTYPE:
		break;
	case MULTIMATERIAL_TRIANGLE_MESH_PROXYTYPE:
		break;
	case SOFTBODY_SHAPE_PROXYTYPE:
		break;
	case HFFLUID_SHAPE_PROXYTYPE:
		break;
	case HFFLUID_BUOYANT_CONVEX_SHAPE_PROXYTYPE:
		break;



	}
	shape_obj* self = (shape_obj*)type->tp_alloc(type, 0);
	if (!self) return NULL;
	self->btshape = shape;

	shape->setUserPointer(self);

	return (PyObject*)self;
}

void  shape_dealloc(shape_obj* self)
{
	if (((btCollisionShape*)(self->btshape))->getShapeType() == COMPOUND_SHAPE_PROXYTYPE) {
		for (int i = 0; i < ((btCompoundShape*)(self->btshape))->getNumChildShapes(); i++) {
			btCollisionShape* child = ((btCompoundShape*)(self->btshape))->getChildShape(i);
			shape_obj* childShape = (shape_obj*)child->getUserPointer();
			Py_DECREF(childShape);
		}
	}
	if(self->btshape) delete ((btCollisionShape*)(self->btshape));
	Py_TYPE(self)->tp_free(self);
}

PyObject* shape_str(shape_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics shape object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* shape_getMeshData(shape_obj* self) {
	return createCollisionShapeGraphicsObject((btCollisionShape*)self->btshape);
}

static PyObject* shape_addChildShape(shape_obj* self, PyObject* args) {

	if (((btCollisionShape*)self->btshape)->getShapeType() != COMPOUND_SHAPE_PROXYTYPE) {
		PyErr_SetString(PyExc_TypeError, "This function can only be used for COMPOUND_SHAPE_PROXYTYPE.");
		return NULL;
	}

	shape_obj* shape_o = nullptr;
	PyObject* pos_o = nullptr;
	PyObject* rot_o = nullptr;
	if (!PyArg_ParseTuple(args, "OOO", &shape_o, &pos_o, &rot_o)) {
		return NULL;
	}

	btTransform transform;
	transform.setIdentity();
	if (pos_o) {
		if (!pyObjToVector(pos_o, transform.getOrigin())) return NULL;
	}
	if (rot_o) {
		btQuaternion q;
		if (!pyObjToVector(rot_o, *((btVector3*)(&q)))) return NULL;
		transform.setRotation(q);
	}
	((btCompoundShape*)self->btshape)->addChildShape(transform, (btCollisionShape*)(shape_o->btshape));

	Py_INCREF(shape_o);


	Py_INCREF(Py_None);
	return Py_None;
}


PyMethodDef shape_methods[] = {
	{ "getMeshData", (PyCFunction)shape_getMeshData, METH_NOARGS, getMeshData_doc},
	{ "addChildShape", (PyCFunction)shape_addChildShape, METH_VARARGS, addChildShape_doc},
	{ NULL,	NULL }
};

PyGetSetDef shape_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject ShapeType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.shape",					/* tp_name */
	sizeof(shape_obj),                  /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)shape_dealloc,			/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)shape_str,                /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	shape_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	shape_methods,						/* tp_methods */
	0,                                  /* tp_members */
	shape_getsets,                      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	shape_new,							/* tp_new */
	0,									/* tp_free */
};
#endif

//////////////////////////////////////////////////////////////////////
//Rigidbody
//////////////////////////////////////////////////////////////////////
#if true
int rigidbody_setshape(rigidbody_obj* self, PyObject* value);

PyObject* rigidbody_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "shape","mass","pos","rot","activate", NULL };

	shape_obj* shape_o = nullptr;
	PyObject* mass_o = nullptr;
	PyObject* pos_o = nullptr;
	PyObject* rot_o = nullptr;
	int activate = 1;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "OO|OOi", kwlist,
		&shape_o, &mass_o, &pos_o, &rot_o, &activate))
		return NULL;


	btCollisionShape* shape = nullptr;

	btTransform transform;
	transform.setIdentity();

	if (pos_o) {
		if (!pyObjToVector(pos_o, transform.getOrigin())) return NULL;
	}
	if (rot_o) {
		btQuaternion q;
		if (!pyObjToVector(rot_o, *((btVector3*)(&q)))) return NULL;
		transform.setRotation(q);
	}
	float mass = (float)PyFloat_AsDouble(mass_o);
	bool isDynamic = (mass != 0.f);

	btVector3 localInertia(0, 0, 0);
	if (isDynamic) ((btCollisionShape*)(shape_o->btshape))->calculateLocalInertia(mass, localInertia);

	btDefaultMotionState* motionState = new btDefaultMotionState(transform);
	btRigidBody::btRigidBodyConstructionInfo rbInfo(mass, motionState, ((btCollisionShape*)(shape_o->btshape)), localInertia);
	rbInfo.m_restitution = 0.0f;
	rbInfo.m_friction = 0.5f;
	rbInfo.m_linearDamping = 0.03f;
	rbInfo.m_angularDamping = 0.03f;

	btRigidBody* body = new btRigidBody(rbInfo);

	if(!activate)
		body->forceActivationState(WANTS_DEACTIVATION);

	body->setContactProcessingThreshold(BT_LARGE_FLOAT);
	if (!isDynamic) body->setCollisionFlags(body->getCollisionFlags() | btCollisionObject::CF_STATIC_OBJECT);

	rigidbody_obj* self = (rigidbody_obj*)type->tp_alloc(type, 0);

	self->btbody = body;
	
	if (isDynamic) {
		self->collisionGroup = 1;
		self->collisionMask = -1;
	}
	else {
		self->collisionGroup = 2;
		self->collisionMask = 3;
	}
	if (body->getBroadphaseHandle()) {
		body->getBroadphaseHandle()->m_collisionFilterGroup = self->collisionGroup;
		body->getBroadphaseHandle()->m_collisionFilterMask = self->collisionMask;
	}
	
	rigidbody_setshape(self, (PyObject*)shape_o);
		
	body->setUserPointer(self);



	return (PyObject*)self;
}

void  rigidbody_dealloc(rigidbody_obj* self)
{
	if (self->btbody) {
		btCollisionShape* shape = ((btRigidBody*)(self->btbody))->getCollisionShape();
		shape_obj* shapeobj = (shape_obj*)shape->getUserPointer();
		Py_DECREF(shapeobj);

		auto ms = ((btRigidBody*)(self->btbody))->getMotionState();
		delete ms;

		int constraintRefCount = ((btRigidBody*)(self->btbody))->getNumConstraintRefs();
		for (int i = 0; i < constraintRefCount; i++) {
			((btRigidBody*)(self->btbody))->removeConstraintRef(((btRigidBody*)(self->btbody))->getConstraintRef(i));
		}

		delete ((btRigidBody*)(self->btbody));
		self->btbody = nullptr;
	}
	Py_TYPE(self)->tp_free(self);
}

PyObject* rigidbody_str(rigidbody_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics rigidbody object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

PyObject* rigidbody_getposition(rigidbody_obj* self)
{
	btVector3& pos = ((btRigidBody*)self->btbody)->getWorldTransform().getOrigin();
	return Py_BuildValue("(fff)", pos.getX(), pos.getY(), pos.getZ());
}

int rigidbody_setposition(rigidbody_obj* self, PyObject* value)
{
	btVector3 v;
	if (!pyObjToVector(value, v)) return NULL;
	btTransform& trans = ((btRigidBody*)self->btbody)->getWorldTransform();
	trans.setOrigin(v);
	//if (world) world->GetWorld()->updateSingleAabb(object);
	return 0;
}

PyObject* rigidbody_getrotation(rigidbody_obj* self)
{
	btQuaternion rot = ((btRigidBody*)self->btbody)->getWorldTransform().getRotation();
	return Py_BuildValue("(ffff)", rot.getX(), rot.getY(), rot.getZ(), rot.getW());
}

int rigidbody_setrotation(rigidbody_obj* self, PyObject* value)
{
	btQuaternion q;
	if (!pyObjToVector(value, *((btVector3*)&q))) return NULL;
	btTransform& trans = ((btRigidBody*)self->btbody)->getWorldTransform();
	trans.setRotation(q);
	//if (world) world->GetWorld()->updateSingleAabb(object);
	return 0;
}

PyObject* rigidbody_getfriction(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getFriction());
}

int rigidbody_setfriction(rigidbody_obj* self, PyObject* value) {
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to friction.");
		return -1;
	}
	((btRigidBody*)self->btbody)->setFriction((float)PyFloat_AsDouble(value));
	return 0;
}

PyObject* rigidbody_getrestitution(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getRestitution());
}

int rigidbody_setrestitution(rigidbody_obj* self, PyObject* value) {
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to restitution.");
		return -1;
	}
	((btRigidBody*)self->btbody)->setRestitution((float)PyFloat_AsDouble(value));
	return 0;
}


PyObject* rigidbody_getshape(rigidbody_obj* self)
{
	auto btshape = ((btRigidBody*)self->btbody)->getCollisionShape();
	return (PyObject*)btshape->getUserPointer();
}

int rigidbody_setshape(rigidbody_obj* self, PyObject* value) 
{
	if (value->ob_type != &ShapeType) {
		PyErr_SetString(PyExc_TypeError, "Only igeBullet.shape can be assigned to shape .");
		return -1;
	}

	((btCollisionShape*)(((shape_obj*)value)->btshape))->setUserPointer(value);
	Py_INCREF(value);

	((btRigidBody*)self->btbody)->setCollisionShape((btCollisionShape*)(((shape_obj*)value)->btshape));
	return 0;
}

PyObject* rigidbody_getenableCollisionCallback(rigidbody_obj* self)
{
	int flag = ((btRigidBody*)self->btbody)->getCollisionFlags();
	int f = (flag & btCollisionObject::CF_CUSTOM_MATERIAL_CALLBACK) ? true : false;
	return PyLong_FromLong(f);
}

int rigidbody_setenableCollisionCallback(rigidbody_obj* self, PyObject* value) 
{
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only int value can be set to enableCollisionCallback.");
		return -1;
	}
	int f = PyLong_AsLong(value);
	int flag = ((btRigidBody*)self->btbody)->getCollisionFlags();
	if (f)	flag |= btCollisionObject::CF_CUSTOM_MATERIAL_CALLBACK;
	else	flag &= (~btCollisionObject::CF_CUSTOM_MATERIAL_CALLBACK);
	((btRigidBody*)self->btbody)->setCollisionFlags(flag);
	return 0;
}

PyObject* rigidbody_getenableContactResponse(rigidbody_obj* self)
{
	int flag = ((btRigidBody*)self->btbody)->getCollisionFlags();
	int f = (flag & btCollisionObject::CF_NO_CONTACT_RESPONSE) ? false : true;
	return PyLong_FromLong(f);
}

int rigidbody_setenableContactResponse(rigidbody_obj* self, PyObject* value) 
{
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only int value can be set to enableContactResponse.");
		return -1;
	}
	int f = PyLong_AsLong(value);
	int flag = ((btRigidBody*)self->btbody)->getCollisionFlags();
	if (!f)	flag |= btCollisionObject::CF_NO_CONTACT_RESPONSE;
	else	flag &= (~btCollisionObject::CF_NO_CONTACT_RESPONSE);
	((btRigidBody*)self->btbody)->setCollisionFlags(flag);
	return 0;
}

PyObject* rigidbody_getcollisionGroupBit(rigidbody_obj* self)
{
	return PyLong_FromLong(self->collisionGroup);
}

int rigidbody_setcollisionGroupBit(rigidbody_obj* self, PyObject* value) {
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only int value can be set to collisionGroupBit.");
		return -1;
	}
	self->collisionGroup = PyLong_AsLong(value);
	if (((btRigidBody*)self->btbody)->getBroadphaseHandle() != NULL)
		((btRigidBody*)self->btbody)->getBroadphaseHandle()->m_collisionFilterGroup = self->collisionGroup;

	return 0;
}

PyObject* rigidbody_getcollisionGroupMask(rigidbody_obj* self)
{
	return PyLong_FromLong(self->collisionMask);
}

int rigidbody_setcollisionGroupMask(rigidbody_obj* self, PyObject* value) {
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only int value can be set to collisionGroupMask.");
		return -1;
	}
	self->collisionMask = PyLong_AsLong(value);
	if (((btRigidBody*)self->btbody)->getBroadphaseHandle() != NULL)
		((btRigidBody*)self->btbody)->getBroadphaseHandle()->m_collisionFilterMask = self->collisionMask;

	return 0;

}

PyObject* rigidbody_getlinearDamping(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getLinearDamping());
}
int rigidbody_setlinearDamping(rigidbody_obj* self, PyObject* value) {
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to linearDamping.");
		return -1;
	}
	btScalar ld = (btScalar)PyFloat_AsDouble(value);
	btScalar ad = ((btRigidBody*)self->btbody)->getAngularDamping();
	((btRigidBody*)self->btbody)->setDamping(ld, ad);
	return 0;
}


PyObject* rigidbody_getangularDamping(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getAngularDamping());
}
int rigidbody_setangularDamping(rigidbody_obj* self, PyObject* value) {
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to angularDamping.");
		return -1;
	}
	btScalar ld = ((btRigidBody*)self->btbody)->getLinearDamping();
	btScalar ad = (btScalar)PyFloat_AsDouble(value);
	((btRigidBody*)self->btbody)->setDamping(ld, ad);
	return 0;
}


PyObject* rigidbody_getlinearVelocity(rigidbody_obj* self)
{
	const btVector3& vel = ((btRigidBody*)self->btbody)->getLinearVelocity();
	return Py_BuildValue("(fff)", vel.getX(), vel.getY(), vel.getZ());
}

int rigidbody_setlinearVelocity(rigidbody_obj* self, PyObject* value)
{
	btVector3 v;
	if (!pyObjToVector((PyObject*)value, v)) return -1;
	((btRigidBody*)self->btbody)->setLinearVelocity(v);
	return 0;
}

PyObject* rigidbody_getangularVelocity(rigidbody_obj* self)
{
	const btVector3& vel = ((btRigidBody*)self->btbody)->getAngularVelocity();	
	return Py_BuildValue("(fff)", vel.getX(), vel.getY(), vel.getZ());;
}

int rigidbody_setangularVelocity(rigidbody_obj* self, PyObject* value)
{
	btVector3 v;
	if (!pyObjToVector((PyObject*)value, v)) return -1;
	((btRigidBody*)self->btbody)->setAngularVelocity(v);
	return 0;
}


PyObject* rigidbody_getangularSleepingThreshold(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getAngularSleepingThreshold());
}
int rigidbody_setangularSleepingThreshold(rigidbody_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to angularSleepingThreshol.");
		return -1;
	}
	btScalar l = ((btRigidBody*)self->btbody)->getLinearSleepingThreshold();
	btScalar a = (btScalar)PyFloat_AsDouble(value);
	((btRigidBody*)self->btbody)->setSleepingThresholds(l, a);
	return 0;
}

PyObject* rigidbody_getlinearSleepingThreshold(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getLinearSleepingThreshold());
}
int rigidbody_setlinearSleepingThreshold(rigidbody_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to angularSleepingThreshol.");
		return -1;
	}
	btScalar l = (btScalar)PyFloat_AsDouble(value);
	btScalar a = ((btRigidBody*)self->btbody)->getAngularSleepingThreshold();
	((btRigidBody*)self->btbody)->setSleepingThresholds(l, a);
	return 0;
}

PyObject* rigidbody_getdeactivationTime(rigidbody_obj* self)
{
	return PyFloat_FromDouble(((btRigidBody*)self->btbody)->getDeactivationTime());
}
int rigidbody_setdeactivationTime(rigidbody_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to deactivationTime.");
		return -1;
	}
	btScalar l = (btScalar)PyFloat_AsDouble(value);
	((btRigidBody*)self->btbody)->setDeactivationTime(l);
	return 0;
}

PyObject* rigidbody_getactivationState(rigidbody_obj* self)
{
	return PyLong_FromLong(((btRigidBody*)self->btbody)->isActive());
}

int rigidbody_setactivationState(rigidbody_obj* self, PyObject* value)
{
	if (!PyLong_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "Only boolean value can be set to activate.");
		return -1;
	}
	int active = (PyLong_AsLong(value) != 0) ? ACTIVE_TAG : WANTS_DEACTIVATION;

	if (active == WANTS_DEACTIVATION) {
		((btRigidBody*)self->btbody)->clearForces();
	}
	((btRigidBody*)self->btbody)->forceActivationState(active);
	return 0;
}






static PyObject* rigidbody_applyTorque(rigidbody_obj* self, PyObject* args) 
{
	PyObject* arg = nullptr;
	if (!PyArg_ParseTuple(args, "O", &arg)) {
		return NULL;
	}
	btVector3 v;
	if (!pyObjToVector(arg, v)) return NULL;
	((btRigidBody*)self->btbody)->applyTorque(v);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* rigidbody_applyForce(rigidbody_obj* self, PyObject* args)
{
	PyObject* arg1 = nullptr;
	PyObject* arg2 = nullptr;
	if (!PyArg_ParseTuple(args, "O|O", &arg1, &arg2)) {
		return NULL;
	}
	btVector3 v1;
	if (!pyObjToVector(arg1, v1)) return NULL;
	if (!arg2) {
		((btRigidBody*)self->btbody)->applyCentralForce(v1);
	}
	else {
		btVector3 v2;
		if (!pyObjToVector(arg2, v2)) return NULL;
		((btRigidBody*)self->btbody)->applyForce(v1, v2);
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* rigidbody_applyImpulse(rigidbody_obj* self, PyObject* args)
{
	PyObject* arg1 = nullptr;
	PyObject* arg2 = nullptr;
	if (!PyArg_ParseTuple(args, "O|O", &arg1, &arg2)) {
		return NULL;
	}
	btVector3 v1;
	if (!pyObjToVector(arg1, v1)) return NULL;

	if (!arg2) {
		((btRigidBody*)self->btbody)->applyCentralImpulse(v1);
	}
	else {
		btVector3 v2;
		if (!pyObjToVector(arg2, v2)) return NULL;
		((btRigidBody*)self->btbody)->applyImpulse(v1, v2);
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* rigidbody_clearForces(rigidbody_obj* self)
{
	((btRigidBody*)self->btbody)->clearForces();
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* rigidbody_setMass(rigidbody_obj* self, PyObject* args)
{
	float mass;
	if (!PyArg_ParseTuple(args, "f", &mass)) {
		return NULL;
	}
	btVector3 inertia;
	((btRigidBody*)self->btbody)->getCollisionShape()->calculateLocalInertia(mass, inertia);
	((btRigidBody*)self->btbody)->setMassProps(mass, inertia);
	((btRigidBody*)self->btbody)->updateInertiaTensor();

	Py_INCREF(Py_None);
	return Py_None;
}


PyMethodDef rigidbody_methods[] = {
	{ "applyTorque", (PyCFunction)rigidbody_applyTorque, METH_VARARGS, applyTorque_doc},
	{ "applyForce", (PyCFunction)rigidbody_applyForce, METH_VARARGS, applyForce_doc},
	{ "applyImpulse", (PyCFunction)rigidbody_applyImpulse, METH_VARARGS, applyImpulse_doc},
	{ "clearForces", (PyCFunction)rigidbody_clearForces, METH_NOARGS, clearForces_doc},
	{ "setMass", (PyCFunction)rigidbody_setMass, METH_VARARGS, setMass_doc},
	{ NULL,	NULL }
};

PyGetSetDef rigidbody_getsets[] = {
	{ const_cast<char*>("position"), (getter)rigidbody_getposition, (setter)rigidbody_setposition,rigidbody_position_doc, NULL },
	{ const_cast<char*>("rotation"), (getter)rigidbody_getrotation, (setter)rigidbody_setrotation,rigidbody_rotation_doc, NULL },
	{ const_cast<char*>("friction"), (getter)rigidbody_getfriction, (setter)rigidbody_setfriction,rigidbody_friction_doc, NULL },
	{ const_cast<char*>("restitution"), (getter)rigidbody_getrestitution, (setter)rigidbody_setrestitution,rigidbody_restitution_doc, NULL },
	{ const_cast<char*>("shape"), (getter)rigidbody_getshape, (setter)rigidbody_setshape, rigidbody_shape_doc, NULL },
	{ const_cast<char*>("enableCollisionCallback"), (getter)rigidbody_getenableCollisionCallback, (setter)rigidbody_setenableCollisionCallback, rigidbody_enableCollisionCallback_doc, NULL },
	{ const_cast<char*>("enableContactResponse"), (getter)rigidbody_getenableContactResponse, (setter)rigidbody_setenableContactResponse, rigidbody_enableContactResponse_doc, NULL },
	{ const_cast<char*>("collisionGroupBit"), (getter)rigidbody_getcollisionGroupBit, (setter)rigidbody_setcollisionGroupBit, rigidbody_collisionGroupBit_doc, NULL },
	{ const_cast<char*>("collisionGroupMask"), (getter)rigidbody_getcollisionGroupMask, (setter)rigidbody_setcollisionGroupMask, rigidbody_collisionGroupMask_doc, NULL },

	{ const_cast<char*>("linearDamping"), (getter)rigidbody_getlinearDamping, (setter)rigidbody_setlinearDamping, rigidbody_linearDamping_doc, NULL },
	{ const_cast<char*>("angularDamping"), (getter)rigidbody_getangularDamping, (setter)rigidbody_setangularDamping, rigidbody_angularDamping_doc, NULL },
	{ const_cast<char*>("linearVelocity"), (getter)rigidbody_getlinearVelocity, (setter)rigidbody_setlinearVelocity, rigidbody_linearVelocity_doc, NULL },
	{ const_cast<char*>("angularVelocity"), (getter)rigidbody_getangularVelocity, (setter)rigidbody_setangularVelocity, rigidbody_angularVelocity_doc, NULL },
	{ const_cast<char*>("angularSleepingThreshold"), (getter)rigidbody_getangularSleepingThreshold, (setter)rigidbody_setangularSleepingThreshold, rigidbody_angularSleepingThreshold_doc, NULL },
	{ const_cast<char*>("linearSleepingThreshold"), (getter)rigidbody_getlinearSleepingThreshold, (setter)rigidbody_setlinearSleepingThreshold, rigidbody_linearSleepingThreshold_doc, NULL },
	{ const_cast<char*>("deactivationTime"), (getter)rigidbody_getdeactivationTime, (setter)rigidbody_setdeactivationTime, rigidbody_deactivationTime_doc, NULL },
	{ const_cast<char*>("activationState"), (getter)rigidbody_getactivationState, (setter)rigidbody_setactivationState, rigidbody_activationState_doc, NULL },




{ NULL, NULL }
};




PyTypeObject RigidBodyType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.rigidBody",				/* tp_name */
	sizeof(rigidbody_obj),              /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)rigidbody_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)rigidbody_str,            /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	rigidbody_doc,						/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	rigidbody_methods,					/* tp_methods */
	0,                                  /* tp_members */
	rigidbody_getsets,                  /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	rigidbody_new,						/* tp_new */
	0,									/* tp_free */
};


#endif

//////////////////////////////////////////////////////////////////////
//World
//////////////////////////////////////////////////////////////////////
#if true
PyObject* dynworld_new(PyTypeObject* type, PyObject* args, PyObject* kw) {


	btBroadphaseInterface* broadphase = nullptr;
	btCollisionDispatcher* dispatcher = nullptr;
	btGhostPairCallback* ghostPairCallback = nullptr;
	btConstraintSolver* solver = nullptr;
	btDefaultCollisionConfiguration* collisionConfiguration = nullptr;
	btDiscreteDynamicsWorld* world = nullptr;

	///collision configuration contains default setup for memory, collision setup
	btDefaultCollisionConstructionInfo ci;
	//ci.m_defaultStackAllocatorSize = 256 * 1024;
	//ci.m_defaultMaxPersistentManifoldPoolSize = 512;
	//ci.m_defaultMaxCollisionAlgorithmPoolSize = 512;

	collisionConfiguration = new btDefaultCollisionConfiguration(ci);
	//collisionConfiguration->setConvexConvexMultipointIterations();

	///use the default collision dispatcher. For parallel processing you can use a diffent dispatcher (see Extras/BulletMultiThreaded)
	dispatcher = new btCollisionDispatcher(collisionConfiguration);

	//broadphase = _new btAxisSweep3(btVector3(-100,-10,-100),btVector3(100,10,100));
	broadphase = new btDbvtBroadphase();
	ghostPairCallback = new btGhostPairCallback();
	broadphase->getOverlappingPairCache()->setInternalGhostPairCallback(ghostPairCallback);

	solver = new btSequentialImpulseConstraintSolver;

	world = new btDiscreteDynamicsWorld(dispatcher,broadphase,solver,collisionConfiguration);
	btContactSolverInfo& info = world->getSolverInfo();
	info.m_numIterations = 4;


	world_obj* self = (world_obj*)type->tp_alloc(type, 0);
	self->broadphase = broadphase;
	self->dispatcher = dispatcher;
	self->solver = solver;
	self->ghostPairCallback = ghostPairCallback;
	self->collisionConfiguration = collisionConfiguration;
	self->btworld = world;
	self->vehicles = nullptr;


#if defined _WIN32
	QueryPerformanceFrequency((LARGE_INTEGER*) & (self->freq));
#elif defined __ANDROID__
#else
	mach_timebase_info(&base);
#endif
	return (PyObject*)self;
}

static PyObject* dynworld_clear(world_obj* self);
void  dynworld_dealloc(world_obj* self)
{
	dynworld_clear(self);
	if (self->collisionConfiguration) delete ((btDefaultCollisionConfiguration*)(self->collisionConfiguration));
	if (self->dispatcher) delete ((btCollisionDispatcher*)(self->dispatcher));
	if (self->broadphase) delete ((btDbvtBroadphase*)(self->broadphase));
	if (self->ghostPairCallback) delete ((btGhostPairCallback*)(self->ghostPairCallback));
	if (self->solver) delete ((btSequentialImpulseConstraintSolver*)(self->solver));
	if (self->btworld) delete ((btDiscreteDynamicsWorld*)(self->btworld));
	Py_TYPE(self)->tp_free(self);
}

PyObject* dynworld_str(world_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics world object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* dynworld_add(world_obj* self, PyObject* args) {
	PyObject* obj;
	int disableCollisionsBetweenLinkedBodies = 0;
	if (!PyArg_ParseTuple(args, "O|p", &obj, &disableCollisionsBetweenLinkedBodies))return NULL;

	if (obj->ob_type == &RigidBodyType) {
		rigidbody_obj* bodyObj = (rigidbody_obj*)obj;
		((btDiscreteDynamicsWorld*)self->btworld)->addRigidBody((btRigidBody*)(bodyObj->btbody), bodyObj->collisionGroup,bodyObj->collisionMask);
		Py_INCREF(obj);
	}
	else if (obj->ob_type == &ConstraintType) {
		constraint_obj* constraintObj = (constraint_obj*)obj;
		((btDiscreteDynamicsWorld*)self->btworld)->addConstraint((btTypedConstraint*)constraintObj->btconstraint, disableCollisionsBetweenLinkedBodies);
		Py_INCREF(obj);
	}
	else if (obj->ob_type == &VehicleType) {
		vehicle_obj* vehicleObj = (vehicle_obj*)obj;
		((btDiscreteDynamicsWorld*)self->btworld)->addVehicle((btActionInterface*)(vehicleObj->btVehicle));
		Py_INCREF(obj);
		if (!self->vehicles)
			self->vehicles = new std::vector<vehicle_obj*>;
		((std::vector<vehicle_obj*>*)self->vehicles)->push_back(vehicleObj);

	}
	else {
		PyErr_SetString(PyExc_TypeError, "parameter error.");
		return NULL;
	}
	Py_INCREF(Py_None);
	return Py_None;
}
static PyObject* dynworld_remove(world_obj* self, PyObject* args) {
	PyObject* obj;
	if (!PyArg_ParseTuple(args, "O", &obj))return NULL;

	if (obj->ob_type == &RigidBodyType) {
		((btDiscreteDynamicsWorld*)self->btworld)->removeRigidBody((btRigidBody*)(((rigidbody_obj*)obj)->btbody));
		Py_DECREF(obj);
	}
	else if (obj->ob_type == &ConstraintType) {
		constraint_obj* constraintObj = (constraint_obj*)obj;
		((btDiscreteDynamicsWorld*)self->btworld)->removeConstraint((btTypedConstraint*)constraintObj->btconstraint);
		Py_DECREF(obj);
	}
	else if (obj->ob_type == &VehicleType) {
		vehicle_obj* vehicleObj = (vehicle_obj*)obj;
		((btDiscreteDynamicsWorld*)self->btworld)->removeVehicle((btActionInterface*)(vehicleObj->btVehicle));
		Py_DECREF(obj);
	}
	else {
		PyErr_SetString(PyExc_TypeError, "parameter error.");
		return NULL;
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* dynworld_step(world_obj* self, PyObject* args) {

	double cpuTime;
#if defined _WIN32
	static LARGE_INTEGER	cuurentTime;
	QueryPerformanceCounter(&cuurentTime);
	LARGE_INTEGER* freq = (LARGE_INTEGER*) & (self->freq);
	cpuTime = (double)cuurentTime.QuadPart / (double)freq->QuadPart;
#elif defined __ANDROID__
	struct timespec tv;
	clock_gettime(CLOCK_MONOTONIC, &tv);
	cpuTime = (double)tv.tv_sec + (double)tv.tv_nsec / 1000000000.0;
#else
	uint64_t t = mach_absolute_time();
	cpuTime = (double)t * (double)base.numer / (double)base.denom / 1000000000.0;
#endif
	double elapsedTime = cpuTime - self->lasttime;
	self->lasttime = cpuTime;
	if (elapsedTime > 0.333333333333)elapsedTime = 0.333333333333;

	((btDiscreteDynamicsWorld*)self->btworld)->stepSimulation((btScalar)elapsedTime);

	Py_INCREF(Py_None);
	return Py_None;
}
static PyObject* dynworld_wait(world_obj* self) {
	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* dynworld_getgravity(world_obj* self)
{
	btVector3 vec = ((btDiscreteDynamicsWorld*)self->btworld)->getGravity();
	return Py_BuildValue("(fff)", vec.getX(), vec.getY(), vec.getZ());
}

int dynworld_setgravity(world_obj* self, PyObject* value)
{
	btVector3 v;
	if (!pyObjToVector(value, v)) return -1;
	((btDiscreteDynamicsWorld*)self->btworld)->setGravity(v);
	return 0;
}

static PyObject* dynworld_clear(world_obj* self) {
	auto world = ((btDiscreteDynamicsWorld*)self->btworld);
	for (int i = world->getNumCollisionObjects() - 1; i >= 0; i--)
	{
		auto obj = world->getCollisionObjectArray()[i];
		world->removeCollisionObject(obj);
		PyObject* pyobj = (PyObject*)obj->getUserPointer();
		Py_DECREF(pyobj);
	}
	for (int i = world->getNumConstraints() - 1; i >= 0; i--)
	{
		auto obj = world->getConstraint(i);
		world->removeConstraint(obj);
		PyObject* pyobj = (PyObject*)obj->getUserConstraintPtr();
		Py_DECREF(pyobj);
	}
	if (self->vehicles) {
		for (auto it = ((std::vector<vehicle_obj*>*)self->vehicles)->begin(); it != ((std::vector<vehicle_obj*>*)self->vehicles)->end(); it++) {
			world->removeVehicle((btRaycastVehicle*)((*it)->btVehicle));
			Py_DECREF(*it);
		}
		delete ((std::vector<vehicle_obj*>*)self->vehicles);
		self->vehicles = nullptr;
	}
	return Py_None;
}

static PyObject* dynworld_getNumCollisionObjects(world_obj* self) {
	return PyLong_FromLong(((btDiscreteDynamicsWorld*)self->btworld)->getNumCollisionObjects());
}

static PyObject* dynworld_getRigidBody(world_obj* self, PyObject* args) {
	int index;
	if (!PyArg_ParseTuple(args, "i", &index))return NULL;
	btCollisionObject* obj = ((btDiscreteDynamicsWorld*)self->btworld)->getCollisionObjectArray()[index];
	return (PyObject*)obj->getUserPointer();
}


struct	MyClosestRayResultCallback : public btCollisionWorld::ClosestRayResultCallback
{
	int index;
	MyClosestRayResultCallback(const btVector3& rayFromWorld, const btVector3& rayToWorld)
		: ClosestRayResultCallback(rayFromWorld, rayToWorld)
		, index(0) {}
	virtual	btScalar addSingleResult(btCollisionWorld::LocalRayResult& rayResult, bool normalInWorldSpace) {
		if (rayResult.m_localShapeInfo) index = rayResult.m_localShapeInfo->m_triangleIndex;
		return ClosestRayResultCallback::addSingleResult(rayResult, normalInWorldSpace);
	}
};


static PyObject* dynworld_rayTestOne(world_obj* self, PyObject* args) 
{
	PyObject* startObj;
	PyObject* endObj;
	int mask = -1;
	int group = 1;
	if (!PyArg_ParseTuple(args, "OO|ii", &startObj, &endObj, &mask, &group)) return NULL;

	btVector3 s, e;
	if (!pyObjToVector(startObj, s)) return NULL;
	if (!pyObjToVector(endObj, e)) return NULL;
	MyClosestRayResultCallback cb(s, e);
	cb.m_collisionFilterMask = mask;
	cb.m_collisionFilterGroup = group;
	((btDiscreteDynamicsWorld*)self->btworld)->rayTest(s, e, cb);
	if (!cb.hasHit()) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* outpos = Py_BuildValue("(fff)", cb.m_hitPointWorld.x(), cb.m_hitPointWorld.y(), cb.m_hitPointWorld.z());
	PyObject* outnom = Py_BuildValue("(fff)", cb.m_hitNormalWorld.x(), cb.m_hitNormalWorld.y(), cb.m_hitNormalWorld.z());

	PyObject* _res =
		Py_BuildValue(
			"{s:O,s:O,s:O,s:i}",
			"collisionObject", (PyObject*)((btCollisionObject*)cb.m_collisionObject->getUserPointer()),
			"hitPosition", outpos,
			"hitNormal", outnom,
			"index", cb.index);

	Py_DECREF(outpos);
	Py_DECREF(outnom);

	return _res;
}


struct	MyAllHitsRayResultCallback : public btCollisionWorld::AllHitsRayResultCallback
{
	btAlignedObjectArray<int> indices;
	MyAllHitsRayResultCallback(const btVector3& rayFromWorld, const btVector3& rayToWorld)
		: AllHitsRayResultCallback(rayFromWorld, rayToWorld) {}
	virtual	btScalar addSingleResult(btCollisionWorld::LocalRayResult& rayResult, bool normalInWorldSpace) {
		int index = 0;
		if (rayResult.m_localShapeInfo) index = rayResult.m_localShapeInfo->m_triangleIndex;
		indices.push_back(index);
		return AllHitsRayResultCallback::addSingleResult(rayResult, normalInWorldSpace);
	}
};

static PyObject* dynworld_rayTestAll(world_obj* self, PyObject* args) 
{
	PyObject* startObj;
	PyObject* endObj;
	int mask = -1;
	int group = 1;
	if (!PyArg_ParseTuple(args, "OO|ii", &startObj, &endObj, &mask, &group))return NULL;

	btVector3 s, e;
	if (!pyObjToVector(startObj, s)) return NULL;
	if (!pyObjToVector(endObj, e)) return NULL;
	MyAllHitsRayResultCallback cb(s, e);
	cb.m_collisionFilterMask = mask;
	cb.m_collisionFilterGroup = group;
	((btDiscreteDynamicsWorld*)self->btworld)->rayTest(s, e, cb);
	if (!cb.hasHit()) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* out = PyTuple_New(cb.m_hitFractions.size());
	for (int i = 0; i < cb.m_hitFractions.size(); i++)
	{
		PyObject* outpos = Py_BuildValue("(fff)", cb.m_hitPointWorld[i].x(), cb.m_hitPointWorld[i].y(), cb.m_hitPointWorld[i].z());
		PyObject* outnom = Py_BuildValue("(fff)", cb.m_hitNormalWorld[i].x(), cb.m_hitNormalWorld[i].y(), cb.m_hitNormalWorld[i].z());

		PyObject* _res =
			Py_BuildValue(
				"{s:O,s:O,s:O,s:i}",
				"collisionObject", (PyObject*)((btCollisionObject*)cb.m_collisionObject->getUserPointer()),
				"hitPosition", outpos,
				"hitNormal", outnom,
				"index", cb.indices[i]);
		PyTuple_SetItem(out, i, _res);

		Py_DECREF(outpos);
		Py_DECREF(outnom);
	}
	return out;
}

struct ContactTestResult
{
	const btCollisionObject* objectA;
	const btCollisionObject* objectB;
	btVector3 localPosA;
	btVector3 localPosB;
	btVector3 worldPosA;
	btVector3 worldPosB;
	btVector3 normalB;
};
struct MyContactResultCallback : public btCollisionWorld::ContactResultCallback
{
	int count;
	std::vector<ContactTestResult>& outResults;
	MyContactResultCallback(std::vector<ContactTestResult>& _outResults)
		:ContactResultCallback(), outResults(_outResults), count(0) {}

	virtual btScalar addSingleResult(btManifoldPoint& cp, 
		const btCollisionObjectWrapper* colObj0Wrap, int partId0, int index0, 
		const btCollisionObjectWrapper* colObj1Wrap, int partId1, int index1){
		ContactTestResult result;
		result.objectA = colObj0Wrap->m_collisionObject;
		result.objectB = colObj1Wrap->m_collisionObject;
		result.worldPosA = cp.m_positionWorldOnA;
		result.worldPosB = cp.m_positionWorldOnB;
		result.localPosA = cp.m_localPointA;
		result.localPosB = cp.m_localPointB;
		result.normalB = cp.m_normalWorldOnB;
		outResults.push_back(result);
		count++;
		return 1.f;
	}
};


static PyObject* dynworld_contactTest(world_obj* self, PyObject* args) {
	///コリジョンテスト
	///特定のオブジェクトと他の全てのオブジェクトとの衝突判定
	///戻り				 : ヒット件数
	//int ContactTest(CollisionObject * colObj, std::vector<ContactTestResult> & outResults, short mask = -1, short group = 1);
	rigidbody_obj* obj;
	int mask = -1;
	int group = 1;
	if (!PyArg_ParseTuple(args, "O|ii", &obj, &mask, &group))return NULL;
	if (obj->ob_base.ob_type != &RigidBodyType) {
		PyErr_SetString(PyExc_TypeError, "1st argument must be rigidBody.");
		return NULL;
	}
	std::vector<ContactTestResult> outResults;
	MyContactResultCallback cb(outResults);
	cb.m_collisionFilterMask = mask;
	cb.m_collisionFilterGroup = group;
	((btDiscreteDynamicsWorld*)self->btworld)->contactTest((btCollisionObject*)obj->btbody, cb);

	if (cb.count == 0) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* out = PyTuple_New(cb.count);
	int i = 0;
	for (auto it = outResults.begin(); it != outResults.end(); it++)
	{
		PyObject*  localPosA = Py_BuildValue("(fff)", it->localPosA.x(), it->localPosA.y(), it->localPosA.z());
		PyObject* localPosB = Py_BuildValue("(fff)", it->localPosB.x(), it->localPosB.y(), it->localPosB.z());
		PyObject* worldPosA = Py_BuildValue("(fff)", it->worldPosA.x(), it->worldPosA.y(), it->worldPosA.z());
		PyObject* worldPosB = Py_BuildValue("(fff)", it->worldPosB.x(), it->worldPosB.y(), it->worldPosB.z());
		PyObject* normal = Py_BuildValue("(fff)", it->normalB.x(), it->normalB.y(), it->normalB.z());

		PyObject* _res =
			Py_BuildValue(
				"{s:O,s:O,s:O,s:O,s:O,s:O,s:O}",
				"objectA", (PyObject*)((btCollisionObject*)it->objectA->getUserPointer()),
				"objectB", (PyObject*)((btCollisionObject*)it->objectB->getUserPointer()),
				"localPosA", localPosA,
				"localPosB", localPosB,
				"worldPosA", worldPosA,
				"worldPosB", worldPosB,
				"normal", normal);
		PyTuple_SetItem(out, i, _res);

		Py_DECREF(localPosA);
		Py_DECREF(localPosB);
		Py_DECREF(worldPosA);
		Py_DECREF(worldPosB);
		Py_DECREF(normal);

		i++;
	}
	return out;
}

static PyObject* dynworld_contactPairTest(world_obj* self, PyObject* args) {
	///ペアコリジョンテスト
	///オブジェクト同士の衝突判定
	///戻り				 : ヒット件数
	//int ContactPairTest(CollisionObject * colObjA, CollisionObject * colObjB, std::vector<ContactTestResult> & outResults, short mask = -1, short group = 1);

	rigidbody_obj* objA;
	rigidbody_obj* objB;
	int mask = -1;
	int group = 1;
	if (!PyArg_ParseTuple(args, "OO|ii", &objA, &objB, &mask, &group))return NULL;
	if (objA->ob_base.ob_type != &RigidBodyType || objB->ob_base.ob_type != &RigidBodyType) {
		PyErr_SetString(PyExc_TypeError, "1st,2nd argument must be rigidBody.");
		return NULL;
	}
	std::vector<ContactTestResult> outResults;
	MyContactResultCallback cb(outResults);
	cb.m_collisionFilterMask = mask;
	cb.m_collisionFilterGroup = group;
	((btDiscreteDynamicsWorld*)self->btworld)->contactPairTest((btCollisionObject*)objA->btbody, (btCollisionObject*)objB->btbody, cb);

	if (cb.count == 0) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* out = PyTuple_New(cb.count);
	int i = 0;
	for (auto it = outResults.begin(); it != outResults.end(); it++)
	{
		PyObject* localPosA = Py_BuildValue("(fff)", it->localPosA.x(), it->localPosA.y(), it->localPosA.z());
		PyObject* localPosB = Py_BuildValue("(fff)", it->localPosB.x(), it->localPosB.y(), it->localPosB.z());
		PyObject* worldPosA = Py_BuildValue("(fff)", it->worldPosA.x(), it->worldPosA.y(), it->worldPosA.z());
		PyObject* worldPosB = Py_BuildValue("(fff)", it->worldPosB.x(), it->worldPosB.y(), it->worldPosB.z());
		PyObject* normal = Py_BuildValue("(fff)", it->normalB.x(), it->normalB.y(), it->normalB.z());

		PyObject* _res =
			Py_BuildValue(
				"{s:O,s:O,s:O,s:O,s:O,s:O,s:O}",
				"objectA", (PyObject*)((btCollisionObject*)it->objectA->getUserPointer()),
				"objectB", (PyObject*)((btCollisionObject*)it->objectB->getUserPointer()),
				"localPosA", localPosA,
				"localPosB", localPosB,
				"worldPosA", worldPosA,
				"worldPosB", worldPosB,
				"normal", normal);
		PyTuple_SetItem(out, i, _res);

		Py_DECREF(localPosA);
		Py_DECREF(localPosB);
		Py_DECREF(worldPosA);
		Py_DECREF(worldPosB);
		Py_DECREF(normal);

		i++;
	}
	return out;
}

static PyObject* dynworld_convexSweepTest(world_obj* self, PyObject* args) {
	///シェイプ遷移テスト
	//int ConvexSweepTest(const CollisionShape * castShape, const Vector3 & fromPos, const Quat & fromRot, const Vector3 & tpPos, const Quat & toRot, short mask = -1);
	//void convexSweepTest (const btConvexShape* castShape, const btTransform& from, const btTransform& to, ConvexResultCallback& resultCallback,  btScalar allowedCcdPenetration = btScalar(0.)) const;
	return 0;

}

PyMethodDef dynworld_methods[] = {
	{ "add", (PyCFunction)dynworld_add, METH_VARARGS, add_doc},
	{ "remove", (PyCFunction)dynworld_remove, METH_VARARGS, remove_doc},
	{ "step", (PyCFunction)dynworld_step, METH_VARARGS, step_doc},
	{ "wait", (PyCFunction)dynworld_wait, METH_NOARGS, wait_doc},
	{ "clear", (PyCFunction)dynworld_clear, METH_NOARGS, clear_doc},
	{ "getNumCollisionObjects", (PyCFunction)dynworld_getNumCollisionObjects, METH_NOARGS, getNumCollisionObjects_doc},
	{ "getRigidBody", (PyCFunction)dynworld_getRigidBody, METH_VARARGS, getRigidBody_doc},
	{ "rayTestOne", (PyCFunction)dynworld_rayTestOne, METH_VARARGS, rayTestOne_doc},
	{ "rayTestAll", (PyCFunction)dynworld_rayTestAll, METH_VARARGS, rayTestAll_doc},
	{ "contactTest", (PyCFunction)dynworld_contactTest, METH_VARARGS, contactTest_doc},
	{ "contactPairTest", (PyCFunction)dynworld_contactPairTest, METH_VARARGS, contactPairTest_doc},
	//{ "convexSweepTest", (PyCFunction)dynworld_convexSweepTest, METH_VARARGS, convexSweepTest_doc},
	{ NULL,	NULL }
};

PyGetSetDef dynworld_getsets[] = {
	{ const_cast<char*>("gravity"), (getter)dynworld_getgravity, (setter)dynworld_setgravity,gravity_doc, NULL },
	{ NULL, NULL }
};

PyTypeObject DynamicsWorldType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.world",					/* tp_name */
	sizeof(world_obj),					/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)dynworld_dealloc,			/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)dynworld_str,			   /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	dynworld_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	dynworld_methods,						/* tp_methods */
	0,                                  /* tp_members */
	dynworld_getsets,				      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	dynworld_new,							/* tp_new */
	0,									/* tp_free */
};

#endif

//////////////////////////////////////////////////////////////////////
//pyxBullet
//////////////////////////////////////////////////////////////////////
static PyMethodDef pyxBullet_methods[] = {
{ nullptr, nullptr, 0, nullptr }
};

static PyModuleDef igeBullet_module = {
	PyModuleDef_HEAD_INIT,
	"igeBullet",								// Module name to use with Python import statements
	"Bullet wrapper for pyxie game engine.",	// Module description
	0,
	pyxBullet_methods							// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeBullet() {
	PyObject* module = PyModule_Create(&igeBullet_module);

	PyObject* vmathmod = PyImport_ImportModule("igeVmath");
	if (!vmathmod) return NULL;
	Vec2Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "vec2");
	Vec3Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "vec3");
	Vec4Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "vec4");
	QuatType = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "quat");
	Mat22Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "mat22");
	Mat33Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "mat33");
	Mat44Type = (PyTypeObject*)PyObject_GetAttrString(vmathmod, "mat44");
	Py_DECREF(vmathmod);

	if (PyType_Ready(&ShapeType) < 0) return NULL;
	if (PyType_Ready(&RigidBodyType) < 0) return NULL;
	if (PyType_Ready(&DynamicsWorldType) < 0) return NULL;
	if (PyType_Ready(&ConstraintType) < 0) return NULL;
	if (PyType_Ready(&VehicleType) < 0) return NULL;

	Py_INCREF(&ShapeType);
	PyModule_AddObject(module, "shape", (PyObject*)& ShapeType);
	Py_INCREF(&RigidBodyType);
	PyModule_AddObject(module, "rigidBody", (PyObject*)& RigidBodyType);
	Py_INCREF(&DynamicsWorldType);
	PyModule_AddObject(module, "world", (PyObject*)& DynamicsWorldType);
	Py_INCREF(&ConstraintType);
	PyModule_AddObject(module, "constraint", (PyObject*)& ConstraintType);
	Py_INCREF(&VehicleType);
	PyModule_AddObject(module, "vehicle", (PyObject*)& VehicleType);

	PyModule_AddIntConstant(module, "BOX_SHAPE_PROXYTYPE", BOX_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "SPHERE_SHAPE_PROXYTYPE", SPHERE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CAPSULE_SHAPE_PROXYTYPE", CAPSULE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CONE_SHAPE_PROXYTYPE", CONE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CYLINDER_SHAPE_PROXYTYPE", CYLINDER_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "STATIC_PLANE_PROXYTYPE", STATIC_PLANE_PROXYTYPE);
	PyModule_AddIntConstant(module, "COMPOUND_SHAPE_PROXYTYPE", COMPOUND_SHAPE_PROXYTYPE);
	
	PyModule_AddIntConstant(module, "TRIANGLE_SHAPE_PROXYTYPE", TRIANGLE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "TETRAHEDRAL_SHAPE_PROXYTYPE", TETRAHEDRAL_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CONVEX_TRIANGLEMESH_SHAPE_PROXYTYPE", CONVEX_TRIANGLEMESH_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CONVEX_HULL_SHAPE_PROXYTYPE", CONVEX_HULL_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CONVEX_POINT_CLOUD_SHAPE_PROXYTYPE", CONVEX_POINT_CLOUD_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CUSTOM_POLYHEDRAL_SHAPE_TYPE", CUSTOM_POLYHEDRAL_SHAPE_TYPE);
	PyModule_AddIntConstant(module, "MULTI_SPHERE_SHAPE_PROXYTYPE", MULTI_SPHERE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "CONVEX_SHAPE_PROXYTYPE", CONVEX_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "UNIFORM_SCALING_SHAPE_PROXYTYPE", UNIFORM_SCALING_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "MINKOWSKI_SUM_SHAPE_PROXYTYPE", MINKOWSKI_SUM_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "MINKOWSKI_DIFFERENCE_SHAPE_PROXYTYPE", MINKOWSKI_DIFFERENCE_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "BOX_2D_SHAPE_PROXYTYPE", BOX_2D_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "TRIANGLE_MESH_SHAPE_PROXYTYPE", TRIANGLE_MESH_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "SCALED_TRIANGLE_MESH_SHAPE_PROXYTYPE", SCALED_TRIANGLE_MESH_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "TERRAIN_SHAPE_PROXYTYPE", TERRAIN_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "GIMPACT_SHAPE_PROXYTYPE", GIMPACT_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "MULTIMATERIAL_TRIANGLE_MESH_PROXYTYPE", MULTIMATERIAL_TRIANGLE_MESH_PROXYTYPE);
	PyModule_AddIntConstant(module, "SOFTBODY_SHAPE_PROXYTYPE", SOFTBODY_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "HFFLUID_SHAPE_PROXYTYPE", HFFLUID_SHAPE_PROXYTYPE);
	PyModule_AddIntConstant(module, "HFFLUID_BUOYANT_CONVEX_SHAPE_PROXYTYPE", HFFLUID_BUOYANT_CONVEX_SHAPE_PROXYTYPE);



	PyModule_AddIntConstant(module, "RO_XYZ", RO_XYZ);
	PyModule_AddIntConstant(module, "RO_XZY", RO_XZY);
	PyModule_AddIntConstant(module, "RO_YXZ", RO_YXZ);
	PyModule_AddIntConstant(module, "RO_YZX", RO_YZX);
	PyModule_AddIntConstant(module, "RO_ZXY", RO_ZXY);
	PyModule_AddIntConstant(module, "RO_ZYX", RO_ZYX);

	PyModule_AddIntConstant(module, "POINT2POINT_CONSTRAINT_TYPE", POINT2POINT_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "HINGE_CONSTRAINT_TYPE", HINGE_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "CONETWIST_CONSTRAINT_TYPE", CONETWIST_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "D6_CONSTRAINT_TYPE", D6_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "SLIDER_CONSTRAINT_TYPE", SLIDER_CONSTRAINT_TYPE);
	//PyModule_AddIntConstant(module, "CONTACT_CONSTRAINT_TYPE", CONTACT_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "D6_SPRING_CONSTRAINT_TYPE", D6_SPRING_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "GEAR_CONSTRAINT_TYPE", GEAR_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "FIXED_CONSTRAINT_TYPE", FIXED_CONSTRAINT_TYPE);
	PyModule_AddIntConstant(module, "D6_SPRING_2_CONSTRAINT_TYPE", D6_SPRING_2_CONSTRAINT_TYPE);

	return module;
}
