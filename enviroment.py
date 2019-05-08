from vrepApi import vrep


class env:
    """Enviroment API.

    Args:

    objects_name(list): list of the objects in the scene to b e considered.
    robots(list): list with name of the robots.

    Attributes:

    self.clientID (int): Indicates Connection with API Server
    self.objects (dict): dictionary conatining information relelvant for every object.
    self.robots (dict):  dictionary conatining information relelvant for every robot.
    self.request (dict): dictionary conatining information about the request in the enviroment
    """

    def __init__(self,objects_name,robots):
        #create the conecction
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
        if self.clientID != 0:
            raise RunTimeError("Not connected")
        else:
            print('Connected')
        self.objects = {}
        self.robots = {}
        _,self._floor_handle=vrep.simxGetObjectHandle(self.clientID,'ResizableFloor_5_25',vrep.simx_opmode_blocking)
        for i,object in enumerate(objects_name):
            assert(type(object) is str), 'Objects and robot names shoud be strings'
            error,handle=vrep.simxGetObjectHandle(self.clientID,object,vrep.simx_opmode_blocking)
            self.objects.update({object:{'handle':handle}})
            error,position=vrep.simxGetObjectPosition(self.clientID,handle,self._floor_handle,vrep.simx_opmode_blocking)
            error,orientation=vrep.simxGetObjectQuaternion(self.clientID,handle,self._floor_handle,vrep.simx_opmode_blocking)
            #error,properties=vrep.simxGetObjectSpecialProperty(self.clientID,handle,vrep.simx_opmode_blocking)
            self.objects[object].update({'position':position,'orientation':orientation})

        for i,robot in enumerate(robots):
            assert(type(object) is str), 'Objects and robot names shoud be strings'
            error,handle=vrep.simxGetObjectHandle(self.clientID,robot,vrep.simx_opmode_blocking)
            self.robots.update({robot:{'handle':handle}})
            error,position=vrep.simxGetObjectPosition(self.clientID,handle,self._floor_handle,vrep.simx_opmode_blocking)
            error,orientation=vrep.simxGetObjectQuaternion(self.clientID,handle,self._floor_handle,vrep.simx_opmode_blocking)
            #error,properties=vrep.simxGetObjectSpecialProperty(self.clientID,handle,vrep.simx_opmode_blocking)
            self.robots[robot].update({'position':position,'orientation':orientation})
        self.request={}
        self.count = 0

    def update_robot_pos(self):
        """
        This method gets the latest robot position using the streaming/buffer operation modes.

        No arguments required.
        """
        for robot in self.robots:
            #First Call for Initialization
            return_code,coordinates = vrep.simxGetObjectPosition(self.clientID, self.robot[robot]['handle'], self.floor_handle, vrep.simx_opmode_streaming)
            #Retreive data from server
            return_code,coordinates = vrep.simxGetObjectPosition(self.clientID, self.robot[robot]['handle'], self.floor_handle, vrep.simx_opmode_buffer)
            #Update position in dictionary
            self.robots[robot]['position'] = coordinates
            #Discontinue server connection
            return_code,coordinates = vrep.simxGetObjectPosition(self.clientID, self.robot[robot]['handle'], self.floor_handle, vrep.simx_opmode_discontinue)

    def in_obstacle():
        return

    def Bounding_Box(self):
        """
        The Bounding_Box method does not require arguments.

        The method will determine the bounding box limits on each robot in the
        environment. The limits are stored in the self.robots nested dictionary
        with the following keys:

            'Bounding Box x'
            'Bounding Box y'

        """

        #Get latest position of robot
        self.update_robot_pos()

        for robot in self.robots:

            #Get the bounding box ranges for x and y
            return_code, minx = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 15, vrep.simx_opmode_streaming)
            return_code, miny = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 16, vrep.simx_opmode_streaming)
            return_code, maxx = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 18, vrep.simx_opmode_streaming)
            return_code, maxy = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 19, vrep.simx_opmode_streaming)

            return_code, minx = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 15, vrep.simx_opmode_buffer)
            return_code, miny = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 16, vrep.simx_opmode_buffer)
            return_code, maxx = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 18, vrep.simx_opmode_buffer)
            return_code, maxy = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 19, vrep.simx_opmode_buffer)

            #Determine the actual bounding box limits relative to the absolute position
            self.robots[robot].update({'Bounding Box x':[(self.robot_c[0]+self.minx), (self.robot_c[0]+self.maxx)]})
            self.robots[robot].update({'Bounding Box y':[(self.robot_c[1]+self.miny), (self.robot_c[1]+self.maxy)]})

            return_code, minx = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 15, vrep.simx_opmode_discontinue)
            return_code, miny = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 16, vrep.simx_opmode_discontinue)
            return_code, maxx = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 18, vrep.simx_opmode_discontinue)
            return_code, maxy = vrep.simxGetObjectFloatParameter(self.clientID, self.robots[robot]['handle'], 19, vrep.simx_opmode_discontinue)

    def request(self, x_rob, y_rob, z_rob, robot):
        """
        Args:

        x_rob: x position of request point
        y_rob: y position of request point
        z_rob: z position of request point
        robot: string input of robot of interest

        The request method takes in the request point or destination co-coordinates
        and assigns the request to the self.request class variable (dictionary)
        """
        request_c = (x_rob, y_rob, z_rob)
        self.request.update({'Request':request_c})

    def isfree(self,x,y):
        """
        The isfree method takes in possible x and y co-ordinates for the robot to move
        to and determines if the spot is available. If the spot is available, a code is
        returned. A value of 0 indicates that the desired position is not free and a
        value of 1 indicates that the desired position is free.

        Args:

        x: x position of node of interest
        y: y position of node of interest

        Returns:

        code: code that indicates if inputted co-ordinates are free of objects.
              If the code returns 1, the position is free.
        """

        for object in self.objects:

            #Initialize Server connection to receive bounding box of obstacles
            return_code, minx = vrep.simxGetObjectFloatParameter(self.clientID, object, 15, vrep.simx_opmode_streaming)
            return_code, miny = vrep.simxGetObjectFloatParameter(self.clientID, object, 16, vrep.simx_opmode_streaming)
            return_code, maxx = vrep.simxGetObjectFloatParameter(self.clientID, object, 18, vrep.simx_opmode_streaming)
            return_code, maxy = vrep.simxGetObjectFloatParameter(self.clientID, object, 19, vrep.simx_opmode_streaming)


            #Get position of obstacles in list
            # return_code, position = vrep.simxGetObjectPosition(self.clientID, object, -1, vrep.simx_opmode_buffer)
            # #Get bounding box co-ordinates
            return_code, minx = vrep.simxGetObjectFloatParameter(self.clientID, object, 15, vrep.simx_opmode_buffer)
            return_code, miny = vrep.simxGetObjectFloatParameter(self.clientID, object, 16, vrep.simx_opmode_buffer)
            return_code, maxx = vrep.simxGetObjectFloatParameter(self.clientID, object, 18, vrep.simx_opmode_buffer)
            return_code, maxy = vrep.simxGetObjectFloatParameter(self.clientID, object, 19, vrep.simx_opmode_buffer)



            #Check if obstacle co-ordinates is within the bounding box limits
            if x<maxx and x>minx:
                if y<maxy and y>miny:
                    code = 0 #If co-ordinates in bounding box, return 0
                    return code
                else:
                    pass
            else:
                pass

            #Discontinue server connection
            return_code, minx = vrep.simxGetObjectFloatParameter(self.clientID, object, 15, vrep.simx_opmode_discontinue)
            return_code, miny = vrep.simxGetObjectFloatParameter(self.clientID, object, 16, vrep.simx_opmode_discontinue)
            return_code, maxx = vrep.simxGetObjectFloatParameter(self.clientID, object, 18, vrep.simx_opmode_discontinue)
            return_code, maxy = vrep.simxGetObjectFloatParameter(self.clientID, object, 19, vrep.simx_opmode_discontinue)


        code = 1 #If nothing fails, return 1, robot is allowed to move to position
        return code


    def set_env(self, x_pos, y_pos, z_pos, size):
        """
        This method can add obstacles to the environment as long as it is connected to the API.
        To carry this method out, the user inputs the co-ordinate positions of where
        they want the dummy object and the size in m of the object. From here VREP will create
        a dummy object of the size indicated and the location inputted.


        Parameters:

        x_pos: x position of where dummy is to be placed
        y_pos: y position of where dummy is to be placed
        z_pos: z position of where dummy is to be placed
        size: size of the dummy in metres (the dummy is a semi-sphere)

        Returns:

        dummy_handle: Handle of new obstacle

        """
        #Create a dummy obstacle for given size and get the handle
        return_code, dummy_handle = vrep.simxCreateDummy(self.clientID, size, None, vrep.simx_opmode_blocking)

        #Set the position of the dummy
        return_code = vrep.simxSetObjectPosition(self.clientID, dummy_handle, -1, [x_pos, y_pos, z_pos], vrep.simx_opmode_oneshot)

        error,orientation=vrep.simxGetObjectQuaternion(self.clientID,dummy_handle,self.floor_handle,vrep.simx_opmode_blocking)

        self.count =+1

        #If the return code is not 0, an error must've occured, inform user otherwise
        #append the new handle to the obstacle list.
        if return_code != 1:
            print('The method was not able to create a dummy\n')
        else:
            self.objects.update({'dummy'+str(self.count):{'handle':dummy_handle,'position':[x_pos, y_pos, z_pos], 'orientation':orientation}})

            return dummy_handle
