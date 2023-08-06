//social init
PyDoc_STRVAR(socialInit_doc,
	"init the social system \n"\
	"\n"\
	"social.init()");

//social release
PyDoc_STRVAR(socialRelease_doc,
	"release the social system\n"\
	"\n"\
	"social.release()");

//social GamesSharing init
PyDoc_STRVAR(socialGamesSharingInit_doc,
	"init the social gamesSharing system \n"\
	"\n"\
	"gamesSharing.init(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)");

//social GamesSharing release
PyDoc_STRVAR(socialGamesSharingRelease_doc,
	"release the social gamesSharing system\n"\
	"\n"\
	"gamesSharing.release(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)");

//social GamesSharing sign in
PyDoc_STRVAR(socialGamesSharingSignIn_doc,
	"the social gamesSharing sign in\n"\
	"\n"\
	"gamesSharing.signIn(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)");

//social GamesSharing sign out
PyDoc_STRVAR(socialGamesSharingSignOut_doc,
	"the social gamesSharing sign out\n"\
	"\n"\
	"gamesSharing.signOut(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)");

//social GamesSharing is signed in
PyDoc_STRVAR(socialGamesSharingIsSignedIn_doc,
	"the social gamesSharing is signed in\n"\
	"\n"\
	"gamesSharing.isSignedIn(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)\n"\
	"Returns\n"\
	"-------\n"\
	"    result : bool");

//social GamesSharing share
PyDoc_STRVAR(socialGamesSharingShare_doc,
	"social sharing\n"\
	"\n"\
	"gamesSharing.share(value, sns, share)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    value : string\n"\
	"        the link to share\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)\n"\
	"    share : int (optional)\n"\
	"        the share type (Link = 0, Photo = 1)");

//social GamesSharing get profile id
PyDoc_STRVAR(socialGamesSharingGetProfileID_doc,
	"get user profile id\n"\
	"\n"\
	"gamesSharing.getProfileID(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)\n"\
	"Returns\n"\
	"-------\n"\
	"    result : string");

//social GamesSharing get profile name
PyDoc_STRVAR(socialGamesSharingGetProfileName_doc,
	"get user profile name\n"\
	"\n"\
	"gamesSharing.getProfileName(sns)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    sns : int (optional)\n"\
	"        the sns type (Facebook = 0)\n"\
	"Returns\n"\
	"-------\n"\
	"    result : string");

//social GamesSharing is available
PyDoc_STRVAR(socialGamesSharingAvailable_doc,
    "the social gamesSharing is available\n"\
    "\n"\
    "gamesSharing.available(sns)\n"\
    "\n"\
    "Parameters\n"\
    "----------\n"\
    "    sns : int (optional)\n"\
    "        the sns type (Facebook = 0)\n"\
    "Returns\n"\
    "-------\n"\
    "    result : bool");
