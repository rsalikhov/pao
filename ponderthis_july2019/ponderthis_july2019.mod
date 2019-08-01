using CP;

execute ENGINE_SETTINGS {
	cp.param.TimeLimit = 60;
}

// board size
int BOARD_SIZE_X = 8;
int BOARD_SIZE_Y = 5;
range chessBoard = 1..BOARD_SIZE_X*BOARD_SIZE_Y;

// knight's cycle length 
int CYCLE_POINTS = 14;
range cycle = 1..CYCLE_POINTS;

tuple TCoord {
 	int x;
 	int y;  
};
// possible knight's moves from point (i,j) on board BOARD_SIZE_X * BOARD_SIZE_Y
// knight's movement looks like the letter "L"
{TCoord} knightMoves2D[i in 1..BOARD_SIZE_X][j in 1..BOARD_SIZE_Y] =
	{
		<i+2,j+1>, <i+2,j-1>, <i+1,j+2>, <i+1,j-2>,
		<i-2,j+1>, <i-2,j-1>, <i-1,j+2>, <i-1,j-2>
	}
	inter {<x,y> | x in 1..BOARD_SIZE_X, y in 1..BOARD_SIZE_Y};

// convert previous possible knight's moves from 2D matrix to 1D array
// 2D point (i,j) moves to 1D point {(i-1) * BOARD_SIZE_Y + j} 
{int} knightMove[i in chessBoard] = 
	{
		(x-1) * BOARD_SIZE_Y + y | 
		<x,y> in knightMoves2D[(i-1) div BOARD_SIZE_Y + 1][(i-1) % BOARD_SIZE_Y + 1]
	};
	
tuple TPair {
 	int p1;
 	int p2;  
};
// pair of the straight lines connected consecutively visited points (edges of cycle)
// (defined by end points, i.e. p1 - end point of line1, p2 - end point of line2)
// these lines cannot intersect each other (non-intersecting knight's cycle)
{TPair} pairs = 
	{<c1,c2> | c1 in 2..CYCLE_POINTS, c2 in 2..CYCLE_POINTS: c2 > c1 + 1}
	union
	{<1,c> | c in 3..CYCLE_POINTS-1};

// next move from point (i,j)
dvar int move[chessBoard] in chessBoard;
// sequence of moves
dvar int seq[cycle] in chessBoard;

// x-coordinate of move
dvar int moveX[c in cycle] in 1..BOARD_SIZE_X;
// y-coordinate of move 
dvar int moveY[c in cycle] in 1..BOARD_SIZE_Y;
// x-coordinate of previous move
dvar int movePrevX[c in cycle] in 1..BOARD_SIZE_X;
// y-coordinate of previous move
dvar int movePrevY[c in cycle] in 1..BOARD_SIZE_Y;

// numerator of fraction t(a)
dvar int intersectUpA[p in pairs];
// denominator of fraction t(a)
dvar int intersectDownA[p in pairs];
// numerator of fraction t(b)
dvar int intersectUpB[p in pairs];
// denominator of fraction t(b)
dvar int intersectDownB[p in pairs]; 

// 1 - if 0 <= t(a) <= 1, 0 - otherwise
dexpr int isIntersectA[p in pairs] =
	(intersectDownA[p] == 0) ? 0 :
		(intersectUpA[p] * intersectDownA[p] < 0) ? 0 :
			 (abs(intersectUpA[p]) <= abs(intersectDownA[p])) ? 1 : 0;
// 1 - if 0 <= t(b) <= 1, 0 - otherwise
dexpr int isIntersectB[p in pairs] =
	(intersectDownB[p] == 0) ? 0 :
		(intersectUpB[p] * intersectDownB[p] < 0) ? 0 :
			 (abs(intersectUpB[p]) <= abs(intersectDownB[p])) ? 1 : 0;
// 1 - if 0 <= t(a) <= 1 and 0 <= t(b) <= 1, 0 - otherwise
dexpr int border[p in pairs] =
	((isIntersectA[p] == 1) && (isIntersectB[p] == 1)); 

// polygon area of knight's cycles
dexpr float polygonArea = 
	0.5 * abs(sum(c in cycle) (movePrevX[c] * moveY[c] - moveX[c] * movePrevY[c]));
 
maximize polygonArea;
//minimize polygonArea;
	
subject to {
	// restrictions on possible moves
	forall(c in chessBoard) {
    	move[c] in knightMove[c];
    }      
    // knight's cycle must contain consequent moves
    forall(p in 2..CYCLE_POINTS) {
      	seq[p] == move[seq[p-1]];
	}
   	// knight's cycle must be closed 
    move[seq[CYCLE_POINTS]] == seq[1];
    // moves must be unique
   	allDifferent(seq);
   	forall(c in cycle) {
   	   	// compute x-coordinate of move
   	   	moveX[c] == ((seq[c]-1) div BOARD_SIZE_Y + 1);
		// compute y-coordinate of move
		moveY[c] == ((seq[c]-1) % BOARD_SIZE_Y + 1);
		// compute x-coordinate of previous move
		movePrevX[c] == ((c == 1) ? moveX[CYCLE_POINTS] : moveX[c-1]);
		// compute y-coordinate of previous move
		movePrevY[c] == ((c == 1) ? moveY[CYCLE_POINTS] : moveY[c-1]);
   	}	
   	
   	forall(p in pairs) {
   		// compute numerator of fraction t(a)
   		intersectUpA[p] ==
			(movePrevY[p.p2] - moveY[p.p2]) * (movePrevX[p.p1] - movePrevX[p.p2])
				+ 
			(moveX[p.p2] - movePrevX[p.p2]) * (movePrevY[p.p1] - movePrevY[p.p2]);
		// compute denominator of fraction t(a)
		intersectDownA[p] == 
			(moveX[p.p2] - movePrevX[p.p2]) * (movePrevY[p.p1] - moveY[p.p1])
				- 
			(movePrevX[p.p1] - moveX[p.p1]) * (moveY[p.p2] - movePrevY[p.p2]); 
		// compute numerator of fraction t(b)
		intersectUpB[p] ==
			(movePrevY[p.p1] - moveY[p.p1]) * (movePrevX[p.p1] - movePrevX[p.p2])
				+ 
			(moveX[p.p1] - movePrevX[p.p1]) * (movePrevY[p.p1] - movePrevY[p.p2]);
		// compute denominator of fraction t(b)
		intersectDownB[p] == 
			(moveX[p.p2] - movePrevX[p.p2]) * (movePrevY[p.p1] - moveY[p.p1])
				- 
			(movePrevX[p.p1] - moveX[p.p1]) * (moveY[p.p2] - movePrevY[p.p2]);    
		// all lines of knight's cycle must be non-intersecting
		border[p] == 0;	
   	}   	  
};