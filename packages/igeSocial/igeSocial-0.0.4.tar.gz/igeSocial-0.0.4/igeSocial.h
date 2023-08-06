#include <Python.h>
#include "Social.h"
#include "GamesSharing.h"

typedef struct {
	PyObject_HEAD
		Social* social;
} social_obj;


typedef struct {
	PyObject_HEAD
		GamesSharing* gamesSharing;
} gamesSharing_obj;


extern PyTypeObject SocialType;
extern PyTypeObject GamesSharingType;
