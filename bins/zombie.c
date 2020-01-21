#include<stdio.h> 
#include<stdlib.h> 
#include<sys/wait.h> 
#include<unistd.h> 
  
void waitexample() 
{ 
    int stat; 
	int pid;
	int fpid;
  
	pid = getppid();
    // This status 1 is reported by WEXITSTATUS 
    if ((fpid = fork()) == 0) 
        while (1)
   		  ;
    else
        waitpid(WAIT_ANY, &stat, WNOHANG); 
	printf("pid=%d et fpid=%d (zombie)\n", pid, fpid);
} 
  
// Driver code 
int main() 
{ 
    waitexample(); 
    return 0; 
} 

