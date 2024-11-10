def Pascal_Particle_Swarm_Optimiser(OUT_TYPE,CONSTRUCTOR,DISCRIMINATOR,ADDITIONAL_FUNCTIONS_AND_PROCEDURES="",POPULATION=1000,ITERATIONS=2000,DIMENSIONS=4,SEARCH_MIN=-100,SEARCH_MAX=100,THRESHOLD=.0001,DIRECTION="DOWN",FRICTION=0.2):
    ##IF SEARCH_MIN IS A NUMBER THEN MAKE ARRAY OF LENGTH DIMENSIONS
    ##IF SEARCH_MAX IS A NUMBER THEN MAKE ARRAY OF LENGTH DIMENSIONS
    ##WHAT FITNESS NEEDS TO BE REACHED TO RETURN RESULTS PREMATURELY
    ##DOWN IF FITNESS SHOULD BE MINIMIZED, UP IF FITNESS SHOULD BE RAISED
    if DIRECTION=="DOWN":
        COMPARISON="<"
        START_SCORE=999999
        DIRECTION_COMMENT="//LOWER NUMBERS ARE BETTER"
    else:
        COMPARISON=">"
        START_SCORE=-999999
        DIRECTION_COMMENT="//HIGHER NUMBERS ARE BETTER"


    if isinstance(SEARCH_MIN,(list,tuple)):
        SEARCH_MIN_ARRAY=tuple(SEARCH_MIN_ARRAY)
    else:
        SEARCH_MIN_ARRAY=tuple([SEARCH_MIN for i in range(DIMENSIONS)])
    if isinstance(SEARCH_MAX,(list,tuple)):
        SEARCH_MAX_ARRAY=tuple(SEARCH_MAX_ARRAY)
    else:
        SEARCH_MAX_ARRAY=tuple([SEARCH_MAX for i in range(DIMENSIONS)])

    SEARCH_DIFFERENCE_ARRAY=tuple([SEARCH_MAX-SEARCH_MIN for i in range(DIMENSIONS)])

    SUSTAIN=1-FRICTION


    Source=f"""program SwarmOptimiser;

uses sysutils;

type
TPosition=array [1..{DIMENSIONS}] of Real;
TVelocity=array [1..{DIMENSIONS}] of Real;


//RECORDS and STRUCTS
PSOPoint = record
   position: TPosition;//Number defined from interpreter/transpiler
   velocity: TVelocity;//Current Speed
   bestpos: TPosition;//Current Best Position
   bestscore: real;//Corresponding Score
end;


//CONSTRUCTOR TYPES
OutType ={OUT_TYPE}




//GLOBAL VARS
var
  SearchMin: TPosition= {SEARCH_MIN_ARRAY};
  SearchMax: TPosition ={SEARCH_MAX_ARRAY};
  SearchDifference: TPosition = {SEARCH_DIFFERENCE_ARRAY};
  SearchVolume: Int64;
  SWARMPoints:array [1..{POPULATION}] of PSOPoint; //POPULATION SIZE
  PopulationSize:integer;
  Dimensions:integer;
  Step:integer;
  Swarm_Optima:real; //The Highest point crossed by any particle
  Swarm_Optima_Pos:TPosition; //The Position of the optima point crossed by
(*function definitions *)



Function Discriminator(Data:OutType):real;//Returns Fitness. Tests the constructed data to quanitify how many of the desired or undesired properties it has.
{DIRECTION_COMMENT}
{DISCRIMINATOR}



Function Construction(candidate:integer):OutType; //Mapping Rank-1 Tensor into OutType for Evaluation.
{CONSTRUCTOR}

{ADDITIONAL_FUNCTIONS_AND_PROCEDURES}

procedure rand_pos(candidate:integer);
  var
    axis:uint16;
    precision:integer = 1000;
      randfloat:double;
begin
 for axis:= 1 to Dimensions do begin
   randfloat:=random(precision)/precision;
   SWARMPoints[candidate].position[axis]:=SearchMin[axis]+randfloat*SearchDifference[axis];
 end;
 SWARMPoints[candidate].bestscore:={START_SCORE};
end;

procedure rand_speed(candidate:integer);
  var
    axis:uint16;
    precision:integer = 1000;
    randfloat:double;
begin
 for axis:= 1 to Dimensions do begin
   randfloat:=random(precision)/precision;
   SWARMPoints[candidate].velocity[axis]:=(SearchMin[axis]+randfloat*SearchDifference[axis])*0.1;
 end;
end;

function PositionToString(Pos: TPosition): string;
var
  i: Integer;
  ResultStr: string;
begin
  ResultStr := '[';
  for i := 1 to Length(Pos) do
  begin
    ResultStr := ResultStr + FloatToStr(Pos[i]);
    if i < Length(Pos) then
      ResultStr := ResultStr + ', ';
  end;
  Result := ResultStr+']';
end;

function Distance(point1, point2: TPosition): Real;
var
  i: Integer;
  sumOfSquares: Real;
begin
  // Calculate the sum of squared differences
  sumOfSquares := 0.0;
  for i := 1 to Dimensions do
    sumOfSquares := sumOfSquares + Sqr(point1[i] - point2[i]);

  // Return the square root of the sum
  result := Sqrt(sumOfSquares);
end;


procedure InitializePopulation;
var
  candidate:integer;
begin

  for candidate:= 1 to PopulationSize do
  begin
    SWARMPoints:=SWARMPoints;
    rand_pos(candidate);
    rand_speed(candidate);

end
end;

procedure  Move_And_Check_Best;
var
  candidate:integer;
  axis:integer;
  fitness:double;
begin
//With each partical move it based on current velocity, then use the new position as
for candidate:= 1 to PopulationSize do
begin
     for axis:= 1 to Dimensions do
     begin
     SWARMPoints[candidate].position[axis]:=  SWARMPoints[candidate].position[axis]+  SWARMPoints[candidate].velocity[axis];
          end;//ADJUST EACH AXIS BY THE VELOCITY IN THAT DIRECTION
  fitness:=Discriminator(Construction(candidate));
  //ONCE MOVEMENT IS COMPLETE CHECK FITNESS

  //IF A PARTICLE IS ON ITS PERSONAL BEST THEN UPDATE PARTICLE OPTIMA
    if fitness {COMPARISON} SWARMPoints[candidate].bestscore then begin //LOWER FITNESS IS BETTER
    ///IF A PARTICLE IS THE MOST FIT THEN UPDATE THE SWARM OPTIMA
         SWARMPoints[candidate].bestpos:=SWARMPoints[candidate].position;
         SWARMPoints[candidate].bestscore:=fitness;
    end;

  if fitness {COMPARISON} Swarm_Optima then begin //LOWER FITNESS IS BETTER
    ///IF A PARTICLE IS THE MOST FIT THEN UPDATE THE SWARM OPTIMA
         Swarm_Optima_Pos:=SWARMPoints[candidate].position;
         Swarm_Optima:=fitness;
    end;
end




end;

procedure UpdateVelocity(candidate:integer);  //"Acceleration" Change Trajectories (Fast Version)
var
   Extrema_Distance:double;
   Personal_Best_Distance:double;
   Sustain:double={SUSTAIN}; //How fast should it go after friction
   axis:integer;
begin
   ///THERE WILL BE A VARIETY OF ALTERNATIVE WAYS TO DO THIS

  //Extrema_Distance:=Distance(SWARMPoints[candidate].position,Swarm_Optima_Pos);  //UNUSED FOR THIS SIMPLE VERSION
  //Personal_Best_Distance:=Distance(SWARMPoints[candidate].position,SWARMPoints[candidate].bestpos);   //UNUSED FOR THIS SIMPLE VERSION

for axis:= 1 to Dimensions do
 SWARMPoints[candidate].velocity[axis]:=SWARMPoints[candidate].velocity[axis]+(Swarm_Optima_Pos[axis]-SWARMPoints[candidate].position[axis])*0.1; //APPROACH BEST

 //Points far away from best solution race towards it, sweeping large areas, points close will search around it.

end;


procedure IteratePopulation;
var
  candidate:integer;
begin
Move_And_Check_Best;
for candidate:= 1 to PopulationSize do
UpdateVelocity(candidate);

end;



procedure ReturnResults(iteration:integer);
begin
writeln('Pos: '+floattostr(SWARMPoints[1].position[1])+' , Velocity:'+floattostr(SWARMPoints[1].velocity[1]));"""+"""
writeln('{"Iteration":'+inttostr(iteration)+'"Score":'+ FloatToStr(Swarm_Optima)+'},Values'+PositionToString(Swarm_Optima_Pos));"""+f"""
end;



//MAIN CODE
begin
//define initial search space
//min val for each axis
Randomize;
PopulationSize:={POPULATION};
     Swarm_Optima:={START_SCORE};
     Dimensions:={DIMENSIONS};
     Step:=0;
     InitializePopulation;
     while Step<{ITERATIONS} do begin
       IteratePopulation;
       Step:=Step+1;
       ReturnResults(Step);
       if Swarm_Optima{COMPARISON}{THRESHOLD} then Break;//IF FITNESS PASSES THRESHOLD RETURN PREMATURELY
     end;

ReturnResults(Step); // PRINT THE RESULTS TO THE TERMINAL FOR THE PYTHON THREAD TO READ AND USE.
//THEN CLOSE


end.
"""


    return Source

###THE TYPE CREATED FROM THE CONSTRUCTOR AND EVALUATED BY THE DISCRIMINATOR
OUT_TYPE="""record
    x,y,z:double;
end;"""


##THE CONSTRUCTOR TURNS EACH PARTICLE INTO SOME CANDIDATE SOLUTION TO A PROBLEM
CONSTRUCTOR="""begin
//VALS
result.x:=SWARMPoints[candidate].position[1]+SWARMPoints[candidate].position[2];
result.y:=SWARMPoints[candidate].position[3];
result.z:=SWARMPoints[candidate].position[4]-SWARMPoints[candidate].position[1];
end;""" ###EVERYTHING EXCEPT THE HEADER (DECLARATIONS (VARS), BEGIN, BODY, END)


##THE DISCRIMINATOR ASSESSES THE VALIDITY OF EACH SOLUTION
DISCRIMINATOR="""begin
       Result:=abs(200+Data.x-(Data.y+8*Data.z));
end;""" ###EVERYTHING EXCEPT THE HEADER (DECLARATIONS (VARS), BEGIN, BODY, END)


ADDITIONAL_FUNCTIONS_AND_PROCEDURES=""

Source=Pascal_Particle_Swarm_Optimiser(OUT_TYPE,CONSTRUCTOR,DISCRIMINATOR,ADDITIONAL_FUNCTIONS_AND_PROCEDURES)
print(Source)
