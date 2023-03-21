#include <stdio.h>
#include <stdlib.h>
#include <time.h> 
#include <GL/glut.h>
#include <math.h>
#ifndef M_PI
	#define M_PI 3.14159265358979323846
#endif
#define C2(x) (x)*(x)
#define C3(x) (x)*C2(x)
#define C4(x) C2(x)*C2(x)

// usage : gcc digital_heart.c -lGL -lGLU -lglut -lm -o digital_heart

unsigned short int a = 400; unsigned short int b = 300;
unsigned short int a1 = 250; unsigned short int b1 = 0;
short int heart_interior[500000]; double points_speed[500000/2]; short int centre_x = 80; double D_max = 0.0;
double TIME = 0.0; double time_incr = 0.09375; short int stroboscopic_frequency = 0;
short int centre_y = -40; short int border_limit = 1000;
short int stroboscopic[5][2000]; int wave_number = 5; int points_number = 2000/2;

void heart_centre(double angle, short int * x, short int * y)
{
	if (tan(angle) == 0)
	{
		*x = 0; *y = -b;
	}
	else
	{
		*x = a*0.95*pow(fabs(tan(angle)),fabs(1/tan(angle)))*cos(angle);
		*y = a*pow(fabs(tan(angle)),fabs(1/tan(angle)))*sin(angle) - b;
	}
}

double heart_texture_interior(double distance, double distance_max, double reduction)
{
	double epaisseur = (a/3.5)*reduction;
	double medium = 0.72;
	double texture_proba = (distance_max-distance<epaisseur) ? medium+(1-medium)*(epaisseur-distance_max+distance)/epaisseur : medium*distance/(distance_max-epaisseur);
	return 0.5*C2(C3(C3(texture_proba)));
}

double heart_texture_centre(double centre, short int centre_max, double distance, double distance_max)
{
	double stretching = 8.0/(1.0+7*pow((centre/centre_max),1.0/8));
	if (centre < 2*centre_max/3) {distance = distance_max - (distance_max-distance)/stretching;}//{distance = ((1.0/stretching)*distance + ((stretching-1)/stretching)*distance_max);}
	double epaisseur = (a/3.5)*0.55;
	double medium = 0.72;
	double factor = pow(1-distance/distance_max, 1.0/32);
	double texture_proba = (distance_max-distance<epaisseur) ? factor*(medium+(1-medium)*(epaisseur-distance_max+distance)/epaisseur) : factor*medium*distance/(distance_max-epaisseur);
	return 0.5*C2(C3(C3(texture_proba)));
}

double movement(double x)
{
	x = ((double) (((int) (100000*x))%((int) (100000*(31.34000 - 0.0612956815428)))))/100000 + 0.0612956815428;
	return ((x < 1.1) ? x/1.1 : 1)*(-(2.262357472976e-11)*C3(C3(x))*C2(x) + (3.866040741191e-9)*C2(x)*C2(C4(x)) - (2.842007143222e-7)*C3(C3(x)) + 0.00001181528564732*C2(C4(x)) - 0.000308374871147*C2(C3(x))*x + 0.005327924402631*C2(C3(x)) - 0.06264445182796*C4(x)*x + 0.4990725373167*C4(x) - 2.512768252657*C3(x) + 6.598265403955*C2(x) - 5.1916010254*x);
}

double D2P(int x1, int y1, int x2, int y2)
{
	return sqrt(C2(x1-x2)+C2(y1-y2));
}

int xINlist(short int x, short int y, short int * list)
{
	for (int k = 0; list[k] != 0 || list[k+1] != 0; k+=2)
	{
		if (list[k] == x && list[k+1] == y) {return 1;}
	}
	if (x==0 && y==0) {return 1;}
	return 0;
}

int x0INlist(short int x, short int y, short int * list)
{
	for (int k = 0; list[k] != 0 || list[k+1] != 0; k+=2)
	{
		if (list[k] == x && list[k+1] == y) {return 1;}
		if (list[k] == 0 && x == 0 && list[k+1]*y > 0) {return 1;}
	}
	if (x==0 && y==0) {return 1;}
	return 0;
}

void LINE2P(short int x1, short int y1, short int x2, short int y2, short int * line)
{
	short int x = x2-x1; short int y = y2-y1; short int max = (fabs(x)>fabs(y)) ? 2*fabs(x) : 2*fabs(y);
	short int x3; short int y3; int incr = 0;
	for (int k = max; k >= 0; k--)
	{
		x3 = k*x/max + x1; y3 = k*y/max + y1;
		if (!(xINlist(x3,y3,line)))
		{
			line[incr] = x3; line[incr+1] = y3; incr+=2;
		}
	}
	line[incr] = 0; line[incr+1] = 0;
}

double gaussian(double x)
{
	return (1/sqrt(2.0*M_PI))*exp(-x*x/2);
}

double dichotomic_search(double y, double borne_inf, double borne_sup) // in this situation
{
	if (y > gaussian(borne_inf)) {return borne_inf;}
	if (y < gaussian(borne_sup)) {return borne_sup;}
	double precision = (borne_sup-borne_inf)/pow(2,10); double middle = 0.0;
	while (borne_sup-borne_inf > precision)
	{
		middle = (borne_sup+borne_inf)/2;
		if (y < gaussian(middle)) {borne_inf = middle;}
		else {borne_sup = middle;}
	}
	return middle;
}

double random_normal_distribution()
{
	double proba = (((double) rand()) / RAND_MAX);
	int test = (proba > 0.5);
	proba = (test) ? (proba-0.5)*gaussian(0.0)/0.5 : proba*gaussian(0.0)/0.5;
	float limit = 4.0;
	double x = dichotomic_search(proba, 0.0, limit);
	x = (test) ? x/limit : -x/limit;
	return x;
}

double stroboscopic_distribution()
{
	double x = random_normal_distribution();
	double max_stretching = 0.3;
	double min_stretching = 1.0;
	double factor = 1.0 + ((x>0) ? max_stretching*x : min_stretching*x);
	return factor;
}

void stroboscopic_effect(short int * x, short int * y)
{
	double angle = (((double) rand()) / RAND_MAX);
	if (angle < 0.001) {angle = 0.09*(angle/0.001)*M_PI;}
	else if (angle > (1-0.001)) {angle = M_PI - 0.09*((1-angle)/0.001)*M_PI;}
	else {angle = M_PI*(0.09+angle*(1-2*0.09));}
	heart_centre(angle, x, y);
	double random_factor_modifier = stroboscopic_distribution();
	*x *= random_factor_modifier; *y *= random_factor_modifier;
}

void heart_interior_creation()
{
	short int heart_edges[4*1920]; short int x; short int y; int heart_incr = 0;
	double angle = 0; double incr = 0.0009765625;
	while (angle < M_PI)
	{
		heart_centre(angle, &x, &y); angle += incr;
		if (!(x0INlist(x,y,heart_edges)))
		{
			heart_edges[heart_incr] = x; heart_edges[heart_incr+1] = y; heart_incr += 2;
		}
	}
	heart_edges[heart_incr] = 0; heart_edges[heart_incr+1] = 0;

	short int centre[2] = {0,0}; heart_incr = 0; short int x2; short int y2; double reduction; double reduction_value = 0.6;
	for (int k = 0; heart_edges[k] != 0 || heart_edges[k+1] != 0; k+=2)
	{
		x = heart_edges[k]; y = heart_edges[k+1]; centre[0] = (x>0) ? centre_x : -centre_x;
		short int new_line[4*1920];
		LINE2P(x, y, centre[0], centre[1], new_line);
		for (int n = 0; new_line[n] != 0 || new_line[n+1] != 0; n+=2)
		{
			x2 = new_line[n]; y2 = new_line[n+1];
			double proba = ((double) rand()) / RAND_MAX;
			reduction = (fabs(x) < centre_x && y>0) ? reduction_value+(1.0-reduction_value)*fabs(x)/centre_x : 1.0;
			if (proba < heart_texture_interior(D2P(x2,y2,centre[0],centre[1]), D2P(x,y,centre[0],centre[1]), reduction))
			{
				heart_interior[heart_incr] = x2; heart_interior[heart_incr+1] = y2; heart_incr+=2;
			}
		}
	}

	short int x1 = 0; short int y1; x2 = 0; double central_fading = 0.75;
	for (int h = 0; h < 1080; h++)
	{
		if (xINlist(x1,h,heart_edges)) {y1 = h;}
		if (xINlist(x1,-h,heart_edges)) {y2 = -h;}
	}
	for (int new_centre_x = -centre_x; new_centre_x<= centre_x; new_centre_x++)
	{
		centre[0] = new_centre_x;
		short int new_line[4*1920];
		LINE2P(x1, y1, centre[0], centre[1], new_line);
		for (int n = 0; new_line[n] != 0 || new_line[n+1] != 0; n+=2)
		{
			x = new_line[n]; y = new_line[n+1];
			double proba = ((double) rand()) / RAND_MAX;
			if (proba < heart_texture_centre(fabs(new_centre_x), centre_x, D2P(x,y,centre[0],centre[1]), D2P(x1,y1,centre[0],centre[1])))
			{
				heart_interior[heart_incr] = x; heart_interior[heart_incr+1] = y; heart_incr+=2;
			}
		}
	}
	for (int new_centre_x = -centre_x; new_centre_x<= centre_x; new_centre_x+=2)
	{
		centre[0] = new_centre_x;
		short int new_line[4*1920];
		LINE2P(x2, y2, centre[0], centre[1], new_line);
		for (int n = 0; new_line[n] != 0 || new_line[n+1] != 0; n+=2)
		{
			x = new_line[n]; y = new_line[n+1];
			double proba = ((double) rand()) / RAND_MAX;
			if (proba < (1-central_fading*(fabs(centre[0])/centre_x))*heart_texture_interior(D2P(x,y,centre[0],centre[1]), D2P(x2,y2,centre[0],centre[1]), 1.0))
			{
				heart_interior[heart_incr] = x; heart_interior[heart_incr+1] = y; heart_incr+=2;
			}
		}
		if (fabs(new_centre_x) < centre_x/2) {new_centre_x+=4;}
	}
	heart_interior[heart_incr] = 0; heart_interior[heart_incr+1] = 0;

}

double point_speed_factor(double distance_max, short x, short y, short x2, short y2)
{
	double distance = D2P(x,y,x2,y2);
	return (distance_max/distance) * (border_limit-distance) / (border_limit-distance_max);
}

double D_max_calculus()
{
	double distance_max = 0.0;
	short int centre[2] = {0,centre_y};
	for (int n = 0; heart_interior[n] != 0 || heart_interior[n+1] != 0; n+=2)
	{
		double distance = D2P(heart_interior[n], heart_interior[n+1], centre[0], centre[1]);
		if (distance > distance_max) {distance_max = distance;}
	}
	return distance_max;
}

void speed_factor()
{
	D_max = D_max_calculus();

	short int centre[2] = {0,centre_y};
	for (int n = 0; heart_interior[n] != 0 || heart_interior[n+1] != 0; n+=2)
	{
		points_speed[n/2] = point_speed_factor(D_max, heart_interior[n], heart_interior[n+1], centre[0], centre[1]);
	}
}

void stroboscopic_preparation()
{
	for (int k = 0; k < wave_number; k++)
	{
		for (int n = 0; n < points_number; n++)
		{
			stroboscopic_effect(&stroboscopic[k][2*n], &stroboscopic[k][2*n+1]);
		}
	}
}

void myInit (void)
{

	glClearColor(0.0, 0.0, 0.0, 1.0);
	glColor3f(1.0f, 0.0f, 0.3f);
	glPointSize(1.0);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluOrtho2D(-960, 960, -540, 540);

	heart_interior_creation();
	speed_factor();
	stroboscopic_preparation();
}

void arret(unsigned char key, int x, int y)
{
	if (key)
	{
		printf("Heart's stopped");
		exit(0);
	}
}

void myDisplay(void)
{
	glClear(GL_COLOR_BUFFER_BIT);
	double mvt = movement(TIME);

	glBegin(GL_POINTS);
	short int x; short int y; double speed_factor; double speed_integral;
	short int centre[2] = {0,centre_y};
	double distension_max = 0.2;
	for (int k = 0; heart_interior[k] != 0 || heart_interior[k+1] != 0; k+=2)
	{
		speed_factor = points_speed[k/2];
		speed_integral = 1.0 + (distension_max*mvt/12.5)*speed_factor;
		x = speed_integral*heart_interior[k]; y = speed_integral*(heart_interior[k+1]-centre[1])+centre[1];
		glVertex2i(x, y);
	}
	glEnd();

	glBegin(GL_POINTS);
	for (int w = 0; w < wave_number; w++)
	{
		for (int k = 0; k < points_number; k+=2)
		{
			speed_integral = 1.0 + (distension_max*mvt/12.5)*point_speed_factor(D_max,stroboscopic[w][k],stroboscopic[w][k+1],centre[0],centre[1]);
			x = speed_integral*stroboscopic[w][k]; y = speed_integral*(stroboscopic[w][k+1]-centre[1])+centre[1];
			glVertex2i(x, y);
			if (w == stroboscopic_frequency) {stroboscopic_effect(&stroboscopic[w][k], &stroboscopic[w][k+1]);}
		}
	}
	glEnd();

	glutSwapBuffers();
	TIME += time_incr;
	stroboscopic_frequency = (stroboscopic_frequency+1)%wave_number;
}

int main (int argc, char** argv)
{
	srand((unsigned int) time(NULL));

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA);
	glutInitWindowSize(1920, 1080);
	glutInitWindowPosition(0, 0);
	glutCreateWindow("H34r7 61V3 4W4Y");

	myInit();
	glutKeyboardFunc(arret);
	glutDisplayFunc(myDisplay);
	glutIdleFunc(myDisplay);
	glutMainLoop();
}
