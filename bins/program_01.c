#include <unistd.h>
#include <stdio.h>

int main(int ac, char **av)
{
    int sec =30;

    while (sec > 0)
    {
        printf("%d\n", sec--);
        sleep(1);
    }
    return (0);
}
