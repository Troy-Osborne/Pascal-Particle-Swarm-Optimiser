program SwarmOptimiser;

uses sysutils;

type
TPosition=array [1..4] of Real;
TVelocity=array [1..4] of double;


//RECORDS and STRUCTS
PSOPoint = record
   position: TPosition;//Number defined from interpreter/transpiler
   velocity: TVelocity;//Current Speed
   bestpos: TPosition;//Current Best Position
   bestscore: real;//Corresponding Score
end;


//CONSTRUCTOR TYPES
OutType =record
    x,y,z:double;
end;





//GLOBAL VARS
var
  SearchMin: TPosition= (-100,-100,-140,-100);
  SearchMax: TPosition =(100,100,140,100);
  SearchDifference: TPosition = (200,200,280,200);
  SearchVolume: Int64;
  SWARMPoints:array [1..10000] of PSOPoint; //POPULATION SIZE
  PopulationSize:integer;
  Dimensions:integer;
  Step:integer;
  Swarm_Optima:real; //The Highest point crossed by any particle
  Swarm_Optima_Pos:TPosition; //The Position of the optima point crossed by
(*function definitions *)

Function Discriminator(Data:OutType):real;//Returns Fitness. Tests the constructed data to quanitify how many of the desired or undesired properties it has.
//The Lower The Number the Better it is
//var
  //Include intermediate values here
begin
       Result:=abs(200+Data.x-(Data.y+8*Data.z));
end;

Function Construction(candidate:integer):OutType; //Mapping Rank-1 Tensor into OutType for Evaluation.
//Random Demo Here. No Application
//var
  ///INTERMEDIATE VARIABLES
begin
//VALS
result.x:=SWARMPoints[candidate].position[1]+SWARMPoints[candidate].position[2];
result.y:=SWARMPoints[candidate].position[3];
result.z:=SWARMPoints[candidate].position[4]-SWARMPoints[candidate].position[1];
end;

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
 SWARMPoints[candidate].bestscore:=99999;
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
    if fitness< SWARMPoints[candidate].bestscore then begin //LOWER FITNESS IS BETTER
    ///IF A PARTICLE IS THE MOST FIT THEN UPDATE THE SWARM OPTIMA
         SWARMPoints[candidate].bestpos:=SWARMPoints[candidate].position;
         SWARMPoints[candidate].bestscore:=fitness;
    end;

  //  if fitness> Swarm_Optima then begin //USE THIS INSTEAD IF HIGHER FITNESS IS BETTER

  if fitness< Swarm_Optima then begin //LOWER FITNESS IS BETTER
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
   Sustain:double=0.8; //How fast should it go after friction
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
writeln('Pos: '+floattostr(SWARMPoints[1].position[1])+' , Velocity:'+floattostr(SWARMPoints[1].velocity[1]));
      writeln('{"Iteration":'+inttostr(iteration)+'"Score":'+ FloatToStr(Swarm_Optima)+'},Values'+PositionToString(Swarm_Optima_Pos));
end;



//MAIN CODE
begin
//define initial search space
//min val for each axis
Randomize;
PopulationSize:=10000;
     Swarm_Optima:=99999;
     Dimensions:=4;
     Step:=0;
     InitializePopulation;
     while Step<1000 do begin
       IteratePopulation;
       Step:=Step+1;
       ReturnResults(Step);
       if Swarm_Optima<0.001 then Break;//IF FITNESS PASSES THRESHOLD RETURN PREMATURELY
     end;

ReturnResults(Step); // PRINT THE RESULTS TO THE TERMINAL FOR THE PYTHON THREAD TO READ AND USE.
//THEN CLOSE
end.
