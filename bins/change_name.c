#include <stdio.h>
#include <string.h>
#include <unistd.h>
#define NEW_NAME "hello_world"

// process run then lunch himself with different name but keep same PID because lunch himself

int main(int argc, char **argv) 
{
  if (strcmp(argv[0], NEW_NAME) != 0) 
  {
    argv[0] = NEW_NAME;
    execv("/Users/ythollet/tm_client/world_hello", argv);
    fputs("exec failed", stderr); 
    return 1;
  }
  while(1)
    ;
}

