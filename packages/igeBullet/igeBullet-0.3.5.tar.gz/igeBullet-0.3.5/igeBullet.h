#include <Python.h>

typedef struct {
	PyObject_HEAD
		void* btVehicle;
		void* btTuning;
		void* btVehicleRayCaster;
} vehicle_obj;


typedef struct {
	PyObject_HEAD
		void* btconstraint;
} constraint_obj;

typedef struct {
	PyObject_HEAD
		void* btshape;
} shape_obj;

typedef struct {
	PyObject_HEAD
		void* btbody;
		PyObject* world;
		short collisionGroup;
		short collisionMask;
} rigidbody_obj;

typedef struct {
	PyObject_HEAD
		void* broadphase;
		void* dispatcher;
		void* solver;
		void* ghostPairCallback;
		void* collisionConfiguration;
		void* btworld;
		void* vehicles;
#if defined _WIN32
		__int64 freq;
#endif
		double lasttime;
} world_obj;
